from odoo import models, fields

class EventSponsor(models.Model):
    _name = 'event.sponsor'
    _description = 'Event sponsor'

    name = fields.Char(string="Sponsor Name", required=True)
    contribution = fields.Float(string="Contribution Amount")
    event_ids = fields.Many2many('event.management', string="Events")
