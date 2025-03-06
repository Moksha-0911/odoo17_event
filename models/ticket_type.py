from odoo import models,fields

class Tickettype(models.Model):
    _name = 'event.ticket.type'
    _description = 'Event ticket Type'

    name = fields.Char(string="Ticket type",required=True)
    ticket_code = fields.Char(string="Ticket code",required=True)
    price = fields.Integer(string="Price",required=True)
    event_id = fields.Many2one('event.management',string="Events")