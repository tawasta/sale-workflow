/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { onMounted } from "@odoo/owl";
import { ListRenderer } from "@web/views/list/list_renderer";
import { evaluateExpr } from "@web/core/py_js/py";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

patch(ListRenderer.prototype, {
    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.action = useService("action");
    },

    // Funktio joka käsittelee add line napin painamisen One2many kentässä
    add(params) {
        console.log("PARAMS:");
        console.log(params);
        console.log("Props:", this.props);
        console.log("this.props.list:", this.props.list)
        console.log("this.props.list.model:", this.props.list.model);
        console.log("this.props.list.model.root:", this.props.list.model.root);
        if (params.context) {
            // Otetaan context string jossa on tieto siitä
            // onko configure nappia painettu
            const contextString = params.context;
            console.log("Context string:", contextString);
            const is_configuration = evaluateExpr(contextString);
            console.log("Is Conf:", is_configuration);
            if (is_configuration) {
                // Käyttäjä painoi cofigure product nappia
                console.log("OPEN PROD CONF");
                const pricelistId = this._getPricelistId();
                console.log("this.rpc:", this.rpc);
                // Kutsutaan omaa controlleria, koska odoon coressa ei ilmeisesti enään ole
                // metodia xmlid_to_res_id
                this.rpc("/sale_order_line_configurator/xmlid_to_res_id", {
                    xmlid: "sale_order_line_configurator.sale_product_configurator_view_form",
                }).then((res_id) => {
                    this.action.doAction(
                        {
                            name: _t("Configure a product"),
                            type: "ir.actions.act_window",
                            res_model: "sale.product.configurator",
                            views: [[res_id, "form"]],
                            target: "new",
                            context: {
                                default_pricelist_id: pricelistId,
                            },
                        },
                        {
                            onClose: (products) => {
                                console.log("ON CLOSE!");
                                console.log("products:", products);
                                if (products && products !== "special" && !products.special) {
                                    this.trigger_up("add_record", {
                                        context: this._productsToRecords(products),
                                        forceEditable: "bottom",
                                        allowWarning: true,
                                        onSuccess: () => {
                                            console.log("Success");
                                        },
                                    });
                                }
                            },
                        }
                    );
                });
            } else {
                // Palautetaan add metodin default toiminnallisuus
                if (this.canCreate) {
                    this.props.onAdd(params);
                }
            }
        } else {
            // Palautetaan add metodin default toiminnallisuus
            if (this.canCreate) {
                this.props.onAdd(params);
            }
        }
    },

    _getPricelistId: function () {
        // Hateaan pricelist_id
        const saleOrderRoot = this.props.list?.model?.root;
        const pricelistId = saleOrderRoot?.data?.pricelist_id?.[0];
        console.log("priceListId:", pricelistId);
        return pricelistId || null;
    },

    _productsToRecords: function (products) {
        var records = [];
    
        products.forEach(function (product) {
            var record = {
                default_product_id: product.product_id,
                default_product_uom_qty: product.quantity,
            };
    
            if (product.no_variant_attribute_values) {
                var default_product_no_variant_attribute_values = [];
                product.no_variant_attribute_values.forEach(function (attribute_value) {
                    default_product_no_variant_attribute_values.push([
                        4,
                        parseInt(attribute_value.value),
                    ]);
                });
                record.default_product_no_variant_attribute_value_ids =
                    default_product_no_variant_attribute_values;
            }
    
            if (product.product_custom_attribute_values) {
                var default_custom_attribute_values = [];
                product.product_custom_attribute_values.forEach(function (attribute_value) {
                    default_custom_attribute_values.push([
                        0,
                        0,
                        {
                            attribute_value_id: attribute_value.attribute_value_id,
                            custom_value: attribute_value.custom_value,
                        },
                    ]);
                });
                record.default_product_custom_attribute_value_ids =
                    default_custom_attribute_values;
            }

            records.push(record);
        });
    
        return records;
    },
});