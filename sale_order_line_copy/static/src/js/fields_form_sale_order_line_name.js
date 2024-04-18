odoo.define("sale_order_line_copy.fields_form", function (require) {
    "use strict";

    var core = require("web.core");
    var FieldRegistry = require("web.field_registry");
    var FieldText = require("web.basic_fields").FieldText;

    var _t = core._t;

    var SaleOrderLineSectionName = FieldText.extend({
        // --------------------------------------------------------------------------
        // Widget API
        // --------------------------------------------------------------------------

        /**
         * For SO lines that are sections, show an additional
         * duplication button
         *
         * @private
         * @override
         */
        _renderReadonly: function () {
            var def = this._super.apply(this, arguments);

            var buttonTitle = _t("Duplicate");

            if (this.record.data.display_type === "line_section") {
                this.$el.addClass("col");
                var $inputGroup = $('<div class="input-group">');
                this.$el = $inputGroup.append(this.$el);
                var $button = $(
                    `<div class="input-group-append">\
                        <button type="button" title="${buttonTitle}" class="btn o_icon_button">\
                            <i class="fa fa-fw o_button_icon fa-clone"/>\
                        </button>\
                    </div>`
                );
                this.$el = this.$el.append($button);
                $button.on("click", this._onClickDuplicateSection.bind(this));
            }

            return def;
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * Send duplication request to backend
         * @private
         * @param {Event} ev
         */
        _onClickDuplicateSection: function (ev) {
            ev.stopPropagation();

            var id = this.record.data.id;

            if (id) {
                this._rpc({
                    model: "sale.order.line",
                    method: "action_sale_order_section_copy",
                    args: [id],
                }).then(() => {
                    this.trigger_up("reload");
                });
            }
        },
    });

    FieldRegistry.add("sale_order_line_section_name", SaleOrderLineSectionName);
});
