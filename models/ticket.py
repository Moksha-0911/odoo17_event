from odoo import models, fields, api

class EventTicket(models.Model):
    _name = 'event.ticket'
    _description = 'Event ticket'
    #
    # name = fields.Char(string="Ticket Type", required=True)
    # price = fields.Float(string="Price", required=True)
    event_id = fields.Many2one('event.management', string="Events",compute="_compute_event",store=True,readonly=True)
    available_tickets = fields.Integer(string="Available Tickets", default=0)
    ticket_type_id = fields.Many2one('event.ticket.type',string='Ticket type')
    price = fields.Integer(string='Price',compute="_compute_price",store=True,readonly=True)

    @api.depends('ticket_type_id')
    def _compute_price(self):
        for record in self:
            record.price = record.ticket_type_id.price if record.ticket_type_id else 0

    #name = fields.Char(string='Events',compute="_compute_event",store=True,readonly=True)

    @api.depends('ticket_type_id')
    def _compute_event(self):
        for record in self:
            record.event_id = record.ticket_type_id.id if record.ticket_type_id else False