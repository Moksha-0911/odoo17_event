from odoo import http
from odoo.http import request

class EventPayment(http.Controller):

    @http.route('/attendee/payment/success', type='http', auth="public", website=True)
    def payment_success(self, attendee_id, **kwargs):
        """ Update attendee payment status after successful payment """

        attendee = request.env['event.attendee'].sudo().browse(int(attendee_id))
        if attendee:
            attendee.sudo().write({'payment_status': 'paid'})

        return request.render("Event_management.payment_success_page", {
            'name': attendee.name,
            'event_name': attendee.event_id.name,
            'ticket_price': attendee.ticket_price,
        })
