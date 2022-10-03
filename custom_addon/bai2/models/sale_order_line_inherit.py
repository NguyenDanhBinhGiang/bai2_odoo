from odoo import models, fields, api


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    warrant_discount_amount = fields.Monetary('Warrant discount amount', default=0)
    warrant_length = fields.Integer("Warrant length in year", related='product_id.warrant_year')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        super(SaleOrderLineInherit, self)._compute_amount()
        for line in self:
            line.warrant_discount_amount = line.price_subtotal * (line.product_id.warrant_discount/100)
            line.price_subtotal -= line.warrant_discount_amount
