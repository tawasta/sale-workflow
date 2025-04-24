/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { onMounted } from "@odoo/owl";
import { ListRenderer } from "@web/views/list/list_renderer";
import { evaluateExpr } from "@web/core/py_js/py";

patch(ListRenderer.prototype, {
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
                
                // this.rpc eikä this._rpc eikä this.env.rpc toimi. Tämä pitää korjata jotenkin.
                this.rpc({
                    model: "ir.model.data",
                    method: "xmlid_to_res_id",
                    kwargs: {
                        xmlid: "sale_product_configurator.sale_product_configurator_view_form",
                    },
                }).then((res_id) => {
                    this.do_action(
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
                            on_close: (products) => {
                                if (products && products !== "special") {
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
    }
});