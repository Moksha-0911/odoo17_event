import re
import io
from twilio.rest import Client
import xlsxwriter
import base64
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError

class EventAttendee(models.Model):
    _name = 'event.attendee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Event attendee'

    name = fields.Char(string="Attendee name",required=True)
    email = fields.Char(string="Email",required=True)
    phone = fields.Char(string="Phone number",required=True)
    event_id = fields.Many2one('event.management',string="Events")
    ticket_type_id = fields.Many2one('event.ticket.type',string="Ticket Type")
    email_sent = fields.Boolean(string="Email sent",default=False)
    state = fields.Selection(
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive')
        ],
        string='State',
        default='active'
    )
    cancel_uid = fields.Many2one('res.users', string="Cancel User")
    cancellation_date = fields.Datetime(string="Cancel Date")
    attendee_event_code = fields.Char(string="Attendee Code", readonly=True, copy=False)

    def search_attendees(self, start_date, end_date):
        return self.search([('event_id.event_date', '>=', start_date), ('event_id.event_date', '<=', end_date)])

    def send_sms(self):
        TWILIO_ACCOUNT_SID = 'ACc904510735f73d4a1e8f64a92a4464cf'
        TWILIO_AUTH_TOKEN = '9e982a02ef81d841639978aa216a65c3'
        TWILIO_PHONE_NUMBER = '+18507880460'
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            # Constructing message with attendee's name and event name
            message_body = (
                f"Hello {self.name},\n"
                f"You are successfully registered for the event '{self.event_id.name}'.\n"
                "We look forward to your participation!\n\n"
                "Best regards,\n"
                "Event Management Team"
            )

            message = client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to=f'+91{self.phone}'
            )

        except Exception as e:
            print(f"Error sending Message: {e}")  # Log the error
    #verifying email
    @api.constrains('email')
    def _check_valid_email(self):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        for record in self:
            if record.email:
                # Validate email format using regex
                if not re.match(email_regex, record.email):
                    raise ValidationError("Invalid email format. Please enter a valid email (e.g., example@mail.com).")


    @api.constrains('phone')
    def _check_valid_phone(self):
        phone_regex = r'^\d{10}$'  # Ensures a 10-digit phone number format
        for record in self:
            if record.phone:
                # Validate phone format using regex
                if not re.match(phone_regex, record.phone):
                    raise ValidationError("Invalid phone number format. Please enter a 10-digit number (e.g., 9876543210).")
    #creating method for the server actions
    def toggle_attendee_state(self):
        for record in self:
            record.state = 'inactive' if record.state == 'active' else 'active'

    def _send_registration_emails(self):
        #Send confirmation emails to newly registered attendees.
        template = self.env.ref('Event_management.email_template_attendee_confirmation', raise_if_not_found=False)
        for attendee in self:
            if template and not attendee.email_sent:  # Ensure email is only sent once
                template.send_mail(attendee.id, force_send=True)
                attendee.email_sent = True

    def action_send_registration_email(self):
        #Manually triggers the attendee confirmation email
        self._send_registration_emails()


    @api.model
    def create(self, vals):
        # Generate unique attendee event code if not provided
        if not vals.get('attendee_event_code'):
            vals['attendee_event_code'] = self.env['ir.sequence'].next_by_code('event.attendee.sequence') or 'Moksha'

        # Create the attendee record
        attendee = super(EventAttendee, self).create(vals)

        # Load the email template
        template = self.env.ref('Event_management.email_template_attendee_confirmation', raise_if_not_found=False)

        if template:
            # Send the email
            template.send_mail(attendee.id, force_send=True)

            # Mark email as sent
            attendee.email_sent = True

            # Log the email in the chatter
            attendee.message_post(
                body=f"Confirmation email sent to {attendee.email}.",
                subject="Registration Confirmation Email",
                message_type='comment',
                subtype_xmlid='mail.mt_comment'  # Logs as a normal comment
            )

        return attendee

    #creating link to the attendee registration form in website!

    def action_attendee_registration(self):
            # This method is called when the button is clicked
            # You can add any logic here before redirecting
            # After the logic, we redirect to the /redirect_to_events route
        return {
            'type': 'ir.actions.act_url',
            'url': '/redirect_to_attendee_registration',
            'target': 'new',  # Opens the URL in the new window
        }
        #creating function to generate PDF for the event attendees

    def action_print_attendee_pdf(self):
        return self.env.ref('Event_management.action_report_attendee_details').report_action(self)

    def action_print_attendee_xlsx(self):
        self.ensure_one()#it will generate report of the selected student only

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Invoices")
        bold = workbook.add_format({'bold': True})

        headers = ['Attendee Name', 'Attendee Email', 'Attendee Contact', 'Attendee Event',]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, bold)

        row = 1
        for attendee in self:
            sheet.write(row, 0, attendee.name)
            sheet.write(row, 1, attendee.email)
            sheet.write(row, 2, attendee.phone)
            sheet.write(row, 3, attendee.event_id.name)
            row += 1

            workbook.close()
            output.seek(0)
            datas = base64.b64encode(output.read())

            attachment = self.env['ir.attachment'].create({
                'name': 'Attendee Report.xlsx',
                'datas': datas,
                'res_model': self._name,
                'res_id': self.id,
                'type': 'binary',
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            })

            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/%s?download=true' % attachment.id,
                'target': 'new',
            }