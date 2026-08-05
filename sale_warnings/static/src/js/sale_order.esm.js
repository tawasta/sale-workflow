import {
  Many2OneField,
  buildM2OFieldDescription,
} from "@web/views/fields/many2one/many2one_field";
import {onMounted, onWillUpdateProps, useState} from "@odoo/owl";
import {WarningDialog} from "@web/core/errors/error_dialogs";
import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

export class Many2OneWarn extends Many2OneField {
  static template = "sale_warnings.partner_id";
  static props = {
    ...super.props,
  };
  setup() {
    super.setup();
    this.dialogService = useService("dialog");
    this.state = useState({warning: ""});
    onMounted(() => {
      this.fillWarning(this.props);
    });
    onWillUpdateProps(async (newProps) => {
      this.fillWarning(newProps);
    });
  }
  async fillWarning(props) {
    console.log("Props: ");
    console.log(props);
    var result = await props.record.model.orm.webSearchRead(
      this.m2oProps.relation,
      [["id", "=", props.record.data[this.props.name].id]],
      {specification: {sale_warn_level: {}, sale_warn_msg: {}}}
    );
    console.log("Result: ");
    console.log(result);
    result.records.forEach((record) => {
      if (record.sale_warn_msg) {
        this.state.warning = record.sale_warn_msg;
      } else {
        this.state.warning = "";
      }
      if (
        props.record.dirty &&
        record.sale_warn_level == "popup_warning" &&
        this.state.warning !== ""
      ) {
        this.dialogService.add(WarningDialog, {
          title: _t("Warning: new field value has warning attached!"),
          message: this.state.warning,
        });
      }
    });
  }
}

registry.category("fields").add("Many2OneWarn", {
  ...buildM2OFieldDescription(Many2OneWarn),
});
