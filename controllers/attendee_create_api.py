import re
from odoo import http
from odoo.http import request, Response


class AttendeeApi(http.Controller):

    @http.route('/api/attendee/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_attendee(self, name, email, phone, event_id, **kwargs):
        try:
            # Validate email
            if email:
                email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                if not re.match(email_regex, email):
                    return {"status": "error", "message": "Invalid email format and it is required!!."}
                if not name:
                    return {"status": "error", "message":"Name is required!!"}
                if not name:
                    return {"status":"error", "message":"Name should not be in integer!!"}
                if not phone:
                    return {"status": "error", "message":"Phone number must be in digits and it is required!!"}

                    # validating event_id if provided
                event_record = None
                if event_id:
                    event_record = request.env["event.management"].sudo().browse(int(event_id))
                    if not event_record:
                        return {"status": "error",
                                "message": "Event related to your search criteria is not found."}
                    # Create attendee record
                    new_attendee = request.env["event.attendee"].sudo().create({
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "event_id": event_record.id if event_record else False
                    })
                    return {
                        "status": "success",
                        "message": "Attendee(s) created successfully",
                        "student": {
                            "name": new_attendee.name,
                            "email": new_attendee.email,
                            "phone": new_attendee.phone,
                            "event_id": {
                                "id": new_attendee.event_id.id if new_attendee.event_id else False,
                                "name": new_attendee.event_id.name if new_attendee.event_id else False
                            }
                        }
                    }
        except Exception as e:
            return {"status": "error", "message": str(e)}
