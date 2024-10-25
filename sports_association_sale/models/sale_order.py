from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sport_ticket_ids = fields.One2many('sport.ticket', 'sale_order_id', string='Sport Tickets')