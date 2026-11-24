import {SaleOrderTemplateLineListRenderer} from "@sale_management/fields/sale_order_template_line_field/sale_order_template_line_field";
import {getSectionRecords} from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";
import {patch} from "@web/core/utils/patch";
import {x2ManyCommands} from "@web/core/orm_service";

// The optional lines of a quotation template keep their quantities, so that the
// quotations created from the template show them. Each method below replaces a
// place where sale_management sets the quantity to 0.
patch(SaleOrderTemplateLineListRenderer.prototype, {
  /**
   * Toggles the optional state of a section without changing the quantities.
   * The super call is not made, as it sets the quantities to 0; lines left at 0
   * by it get the quantity 1 when the section is no longer optional, as in core.
   */
  async toggleIsOptional(record) {
    const setOptional = !record.data.is_optional;
    const commands = [
      x2ManyCommands.update(record.resId || record._virtualId, {
        is_optional: setOptional,
      }),
    ];
    if (!setOptional) {
      for (const sectionRecord of getSectionRecords(this.props.list, record)) {
        if (!sectionRecord.data.display_type && !sectionRecord.data.product_uom_qty) {
          commands.push(
            x2ManyCommands.update(sectionRecord.resId || sectionRecord._virtualId, {
              product_uom_qty: 1,
            })
          );
        }
      }
    }
    await this.props.list.applyCommands(commands, {sort: true});
  },

  getCreateContext(params) {
    return params.context;
  },

  getInsertLineContext(record, addSubSection) {
    const context = {...super.getInsertLineContext(record, addSubSection)};
    delete context.default_product_uom_qty;
    return context;
  },

  /**
   * Moving a line into an optional section keeps its quantity; a line at 0 that
   * leaves an optional section gets the quantity 1, as in core.
   */
  async _handleQuantityAdjustment(recordMap) {
    const commands = [];
    for (const [recordId, wasOptional] of recordMap.entries()) {
      const record = this.props.list.records.find((line) => line.id === recordId);
      if (
        wasOptional &&
        !this.shouldCollapse(record, "is_optional") &&
        !record.data.product_uom_qty
      ) {
        commands.push(
          x2ManyCommands.update(record.resId || record._virtualId, {
            product_uom_qty: 1,
          })
        );
      }
    }
    if (commands.length) {
      await this.props.list.applyCommands(commands, {sort: true});
    }
  },
});
