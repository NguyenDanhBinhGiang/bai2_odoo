from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    warranty_discount_amount = fields.Monetary("Total warrant discount amount",
                                               compute='_compute_total_warrant_discount')

    @api.depends('order_line.warrant_discount_amount')
    def _compute_total_warrant_discount(self):
        for order in self:
            discount = 0
            for line in order.order_line:
                discount += line.warrant_discount_amount
            order.warranty_discount_amount = discount
