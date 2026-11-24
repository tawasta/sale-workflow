import {SaleOrderLineProductField} from "@sale/js/sale_product_field";
import {patch} from "@web/core/utils/patch";

// Sale_management sets the quantity of products added to an optional section to 0
// and hides their quantity and price in the configurator; the quantities are kept.
patch(SaleOrderLineProductField.prototype, {
  _getAdditionalDialogProps() {
    const props = super._getAdditionalDialogProps();
    delete props.options;
    return props;
  },

  _prepareNewLineData(line, product) {
    const quantity = product.quantity;
    const data = super._prepareNewLineData(line, product);
    data.quantity = quantity;
    return data;
  },
});
