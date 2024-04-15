odoo.define("sale_order_line_copy.fields_form", function (require) {
    "use strict";

    var FieldRegistry = require("web.field_registry");
    var FieldChar = require("web.basic_fields").FieldChar;

    var SaleOrderLineSectionName = FieldChar.extend({
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

            if (this.record.data.display_type === "line_section") {
                this.$el.addClass("col");
                var $inputGroup = $('<div class="input-group">');
                this.$el = $inputGroup.append(this.$el);
                var $button = $(
                    `<div class="input-group-append">\
                        <button type="button" title="Duplicate" class="btn o_icon_button">\
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
