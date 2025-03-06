from odoo import http
from odoo.http import request

class WebLoginApi(http.Controller):
    @http.route('/web/login/api', type='json', auth='none', methods=['POST'], csrf=False)
    def login(self, password, email):
        try:
            if not email or not password:
                return {"status":"error","message":"Email and password required"}
                #  Authenticate the student using Odoo's authentication method
            db_name = request.env.cr.dbname
            uid = request.env['res.users']._login(db_name, email, password, request.httprequest.environ)

            if not uid:
                return {"status":"error","message":"Invalid email or password"}
            return{
                "status":"success",
                "message":"Login successful!!",
            }
        except Exception as e:
            return {"status":"error","message":str(e)}
                    