from odoo import models,fields,api
class Event(models.Model):
    _name = 'event.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Events'

    name = fields.Char(string='Event name',required=True)
    event_date = fields.Date(string='Event date',required=True)
    description= fields.Text(string='Description',required=True)
    category_id = fields.Many2one('event.category',string='Event category')
    attendee_ids = fields.One2many('event.attendee','event_id',string="Event attendee")
    attendee_count = fields.Integer(string="Attendee Count", compute="_compute_attendee_count")
    state = fields.Selection(
        selection=[
            ('pre-booked','Pre-booked'),
            ('confirmed','Confirmed'),
            ('done','Done'),
            ('canceled','Canceled')

        ],
        string="State",
        default="pre-booked"
    )

    def action_event(self):
        # This method is called when the button is clicked
        # You can add any logic here before redirecting
        # After the logic, we redirect to the /redirect_to_events route
        return {
            'type': 'ir.actions.act_url',
            'url': '/redirect_to_events',
            'target': 'new',  # Opens the URL in the new window
        }


    def custom_create_event(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Event',
            'view_mode': 'form',
            'res_model': 'event.management',
            'view_type': 'form',
            'target': 'current',
            'context': {
                'default_some_field': self.id
            }
        }

    def action_prebook(self):
        """Set state to Pre-Booked"""
        self.write({'state': 'pre-booked'})

    def action_confirm(self):
        """Set state to Confirmed"""
        self.write({'state': 'confirmed'})

    def action_done(self):
        """Set state to Done"""
        self.write({'state': 'done'})

    def action_cancel(self):
        """Set state to Canceled"""
        self.write({'state': 'canceled'})
    #creating function for the smart button that stores the information of event attendees

    def action_redirect_to_events(self):
        #Redirects to the website's Event Page
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        event_page_url = f"{base_url}/events" # events page of the website

        return {
            'type': 'ir.actions.act_url',
            'url': event_page_url,
            'target': 'new',
        }
    # def action_open_event_form(self):
    #      #Opens the form view of event.management
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Add New',
    #         'res_model': 'event.management',
    #         'view_mode': 'form',
    #         'view_id': False,  # Uses the default form view
    #         'target': 'new',
    #     }

    @api.depends('attendee_ids')
    def _compute_attendee_count(self):
        #counts the number of attendees for each event
        for event in self:
            event.attendee_count = len(event.attendee_ids)

    def action_view_attendees(self):
        self.ensure_one()
        #opens the list of attendees for this event
        return {
            'name': 'Attendees',
            'type': 'ir.actions.act_window',
            'res_model': 'event.attendee',
            'view_mode': 'tree,form',
            'domain': [('event_id', '=', self.id)],
            'context': {'default_event_id': self.id},
        }

