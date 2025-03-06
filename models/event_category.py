from odoo import models,fields
class EventCategory(models.Model):
    _name = 'event.category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Event category'

    name= fields.Char(string="Category name",required=True)





