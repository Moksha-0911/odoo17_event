from datetime import datetime
from odoo import http
from odoo.http import request, Response

class AttendeeApi(http.Controller):
    @http.route('/api/attendee/delete', type='json', auth='public', methods=['POST'], csrf=False)
    def delete_attendee(self,attendee_line_id,**kwargs):
        try:
            if not attendee_line_id:
                return {"status": "error", "message": "Student not found"}

            # Create attendee record
            attendee_record = request.env['event.attendee'].sudo().browse(attendee_line_id)
            if attendee_record:
                attendee_record.write({
                    'cancel_uid': request.env.user.id,
                    'cancellation_date': datetime.now(),
                    'state': 'inactive'
                })

            return {
                "status": "success",
                "message": "Attendee(s) deleted successfully",
                "student": {
                    "name": attendee_record.name,
                    "email": attendee_record.email,
                    "phone": attendee_record.phone,
                    "cancel_uid": {
                        'id': attendee_record.cancel_uid.id,
                        'name': attendee_record.cancel_uid.name
                    },
                    "cancellation_date": attendee_record.cancellation_date,
                    "state": attendee_record.state
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

