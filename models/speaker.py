from odoo import models, fields

class EventSpeaker(models.Model):
    _name = 'event.speaker'
    _description = 'Event speaker'

    name = fields.Char(string="Speaker Name", required=True)
    topic = fields.Char(string="Topic")
    event_ids = fields.Many2many('event.management', string="Speaking At")
