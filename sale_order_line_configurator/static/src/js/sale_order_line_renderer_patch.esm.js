/** @odoo-module **/

import {ProductLabelSectionAndNoteListRender} from "@account/components/product_label_section_and_note_field/product_label_section_and_note_field_o2m";
import {SaleOrderLineListRenderer} from "@sale/js/sale_order_line_field/sale_order_line_field";
import {patch} from "@web/core/utils/patch";

patch(SaleOrderLineListRenderer.prototype, {
  getActiveColumns() {
    // Keep upstream (and any other patch of this method) active: it hides
    // the template column as soon as the variant column is enabled, so we
    // add the template column back afterwards.
    const activeColumns = super.getActiveColumns();
    if (activeColumns.some((col) => col.name === "product_template_id")) {
      return activeColumns;
    }
    const parentColumns =
      ProductLabelSectionAndNoteListRender.prototype.getActiveColumns.call(this);
    const templateColumn = parentColumns.find(
      (col) => col.name === "product_template_id"
    );
    if (!templateColumn) {
      return activeColumns;
    }
    const columns = [...activeColumns];
    const productIndex = columns.findIndex((col) => col.name === "product_id");
    columns.splice(
      productIndex === -1 ? columns.length : productIndex + 1,
      0,
      templateColumn
    );
    return columns;
  },
});
