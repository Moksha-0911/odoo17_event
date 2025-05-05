from odoo import models, fields

class EventVenue(models.Model):
    _name = 'event.venue'
    _description = 'Event Venue'

    name = fields.Char(string="Venue Name", required=True)
    address = fields.Text(string="Address")
    capacity = fields.Integer(string="Capacity")
    event_id = fields.Many2one('event.management', string="Events")
