from odoo import models, fields


class ProductWizard(models.TransientModel):
    _name = 'product.wizard'

    product_id = fields.Many2many('product.template')
    new_date_from = fields.Date("Date from")
    new_date_to = fields.Date("Date to")

    def update_product(self):
        for wiz in self:
            for product in wiz.product_id:
                product.date_from = wiz.new_date_from
                product.date_to = wiz.new_date_to
