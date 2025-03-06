from datetime import datetime
import re
from odoo import http
from odoo.http import request, Response

class AttendeeApi(http.Controller):
    @http.route('/api/attendee/search', type='json', auth='public', methods=['POST'], csrf=False)
    def search_attendee(self,name, email, phone,attendee_line_id, **kwargs):
        search_domain = []
        try:

        #validating email
            if email:
                email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                if not re.match(email_regex, email):
                    return {"status": "error", "message": "Invalid email format."}
                search_domain.append(("email", "=", email))

            if name:
                search_domain.append(("name", "ilike",name))
            if not name:
                return {"status":"error","message": "Name is required!!"}
            if not name:
                return {"status":"error","message": "Name should not be in integer!!"}

            if phone:
                search_domain.append(("phone","=",phone))
            if not phone:
                return {"status":"error","message":"Phone number must contain 10 digits and is required!!"}
            if not phone:
                return {"status":"error","message":"Phone number must be in digits!!"}
            if not search_domain:
                return {"status": "error", "message": "Please provide at least one search parameter (name, email, or phone)."}
            attendees = request.env["event.attendee"].sudo().search(search_domain)

            if not attendees:
                return {"status": "error", "message": "No attendee found with the given details."}

            #     # Create attendee record
            attendee_record = request.env['event.attendee'].sudo().browse(attendee_line_id)
            if attendee_record:
                attendee_record.write({
                    'cancel_uid': request.env.user.id,
                    'cancellation_date': datetime.now(),
                    'state': 'active'
                })
            # if not attendee_record:
            #     attendee_record.write({
            #         'cancel_uid':request.env.user.id,
            #         'cancellation_date': datetime.now(),
            #         'state': 'inactive'
            #     })

            attendee_list = []
            for attendee in attendees:
                attendee_list.append({
                'name': attendee.name,
                "email": attendee.email,
                "phone": attendee.phone,
                "cancel_uid": {
                    'id': attendee_record.cancel_uid.id,
                    'name': attendee_record.cancel_uid.name
                },
                "cancellation_date": attendee_record.cancellation_date,
                "state": attendee_record.state,
                "event_id":{
                    'id':attendee.event_id.id,
                    'name':attendee.event_id.name
                    }
                })
                return {
                    "status": "success",
                    "message": "Attendee(s) found successfully",
                    "attendees": attendee_list
                }

        except Exception as e:
            return {"status": "error", "message": str(e)}


