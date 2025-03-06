from odoo import http
from odoo.http import request

class EventRegistration(http.Controller):
    @http.route('/redirect_to_events', auth='user', type='http', methods=['GET'], website=True)
    def redirect_to_events(self):
        # This method will handle the redirection
        return request.redirect('/events')

