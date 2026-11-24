from odoo.exceptions import AccessError, MissingError
from odoo.http import request, route

from odoo.addons.sale.controllers import portal


class CustomerPortal(portal.CustomerPortal):
    @route()
    def portal_quote_accept(
        self, order_id, access_token=None, name=None, signature=None
    ):
        # The signing dialog shows only the errors returned as a result, not raised
        # ones, so the alternatives are checked before the signature is saved.
        access_token = access_token or request.httprequest.args.get("access_token")
        try:
            order_sudo = self._document_check_access(
                "sale.order", order_id, access_token=access_token
            )
        except (AccessError, MissingError):
            order_sudo = None
        if (
            order_sudo
            and order_sudo._has_optional_section()
            and order_sudo._has_to_be_signed()
        ):
            return {"error": order_sudo._confirmation_error_message()}
        return super().portal_quote_accept(
            order_id, access_token=access_token, name=name, signature=signature
        )
