
from odoo import http
from odoo.http import request

class AttendeeApi(http.Controller):


    @http.route('/api/attendee/update', type='json', auth='public', methods=['POST'], csrf=False)
    def update_attendee(self, attendee_line_id, update_str, **kwargs):
        try:
            if not attendee_line_id:
                return {"status":"error","message": "Attendee not found"}
            if not update_str:
                return {"status":"error","message":"Updated dict not found"}


            #create attendee record
            attendee_record = request.env['event.attendee'].sudo().browse(attendee_line_id)

            if attendee_record:
                attendee_record.write({
                    'name': update_str.get('name') and update_str.get('name') or attendee_record.name,
                    'email': update_str.get('email')
                })
                return{
                    "status":"success",
                    "message":"Attendee(s) updated successfully",
                    "attendee":{
                        "attendee_line_id": attendee_record.id,
                        "email": attendee_record.email,
                        "phone": attendee_record.phone
                    }
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}