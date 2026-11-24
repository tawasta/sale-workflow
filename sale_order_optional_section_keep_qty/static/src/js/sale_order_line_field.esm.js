import {SaleOrderLineListRenderer} from "@sale/js/sale_order_line_field/sale_order_line_field";
import {getSectionRecords} from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";
import {patch} from "@web/core/utils/patch";
import {registry} from "@web/core/registry";
import {x2ManyCommands} from "@web/core/orm_service";

// The optional lines keep their quantities: the server leaves them out of the total.
// Each method below replaces a place where sale_management sets the quantity to 0.
patch(SaleOrderLineListRenderer.prototype, {
  /**
   * Toggles the optional state of a section without changing the quantities.
   * The super call is not made, as it sets the quantities to 0; its reset of the
   * hidden prices and composition of the subsections is kept.
   */
  async toggleIsOptional(record) {
    const setOptional = !record.data.is_optional;
    const commands = [
      x2ManyCommands.update(record.resId || record._virtualId, {
        is_optional: setOptional,
      }),
    ];
    const proms = [];
    for (const sectionRecord of getSectionRecords(this.props.list, record)) {
      if (setOptional && this.isSubSection(sectionRecord)) {
        commands.push(
          x2ManyCommands.update(sectionRecord.resId || sectionRecord._virtualId, {
            collapse_composition: false,
            collapse_prices: false,
          })
        );
      } else if (
        !setOptional &&
        !sectionRecord.data.display_type &&
        !sectionRecord.data.product_uom_qty
      ) {
        // Lines from a quotation template come with quantity 0, as in core.
        proms.push(sectionRecord._update({product_uom_qty: 1}));
      }
    }
    await this.props.list.applyCommands(commands, {sort: true});
    await Promise.all(proms);
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

  /**
   * The total of a regular section leaves out the lines of its optional
   * subsections, as the order total does.
   */
  getFormattedValue(column, record) {
    if (
      !this.isTopSection(record) ||
      record.data.is_optional ||
      !this.props.aggregatedFields.includes(column.name)
    ) {
      return super.getFormattedValue(column, record);
    }
    const total = getSectionRecords(this.props.list, record)
      .filter(
        (line) => !this.isSection(line) && !this.shouldCollapse(line, "is_optional")
      )
      .reduce((sum, line) => sum + line.data[column.name], 0);
    const formatter = registry
      .category("formatters")
      .get(column.fieldType, (value) => value);
    return formatter(total, {
      ...formatter.extractOptions?.(column),
      data: record.data,
      field: record.fields[column.name],
    });
  },

  async moveCombo(record, direction) {
    const quantity = record.data.product_uom_qty;
    await super.moveCombo(record, direction);
    if (record.data.product_uom_qty !== quantity) {
      await record.update({product_uom_qty: quantity});
    }
  },
});
