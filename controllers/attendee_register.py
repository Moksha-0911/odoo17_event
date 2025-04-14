from odoo import http
from odoo.http import request

class AttendeeRegistration(http.Controller):
    @http.route('/redirect_to_attendee_registration', auth='user', type='http', methods=['GET'], website=True)
    def redirect_to_attendee_registration(self):
        # This method will handle the redirection
        return request.redirect('/attendee/register')
