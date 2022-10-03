import datetime
from dateutil.relativedelta import relativedelta
import odoo.exceptions
from odoo import models, fields, api

WARRANT_CODE_DATE_FORMAT = '%d%m%y'


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    warrant_code = fields.Char("Warranty code",
                               compute='_compute_warrant_code',
                               inverse='_set_warrant_code')
    date_from = fields.Date("Warrant From")
    date_to = fields.Date("Warrant To")
    warrant_discount = fields.Integer("Warrant Discount", compute='_compute_warrant_discount', store=True)
    warrant_year = fields.Integer("Warrant length in year", compute='_compute_warrant_length')

    def _set_warrant_code(self):
        for product in self:
            if product.has_valid_warrant_code():
                code = str(product.warrant_code).split('/')
                product.date_from = datetime.datetime.strptime(code[1], WARRANT_CODE_DATE_FORMAT)
                product.date_to = datetime.datetime.strptime(code[2], WARRANT_CODE_DATE_FORMAT)

    def has_valid_warrant_code(self):
        self.ensure_one()
        try:
            code = str(self.warrant_code).split('/')
            date_from = datetime.datetime.strptime(code[1], WARRANT_CODE_DATE_FORMAT)
            date_to = datetime.datetime.strptime(code[2], WARRANT_CODE_DATE_FORMAT)
            assert date_from < date_to
            return True
        except (ValueError, IndexError, AssertionError):
            return False

    def create(self, vals_list):
        for record in self:
            if self.user_has_groups('bai2.advanced_sale'):
                if any(x in ('warrant_code', 'date_from', 'date_to') for x in record):
                    raise odoo.exceptions.UserError("You don't have permission!")

        return super(ProductTemplateInherit, self).create(vals_list)

    def write(self, vals):
        for record in self:
            if self.user_has_groups('bai2.advanced_sale'):
                if any(x in ('warrant_code', 'date_from', 'date_to') for x in record):
                    raise odoo.exceptions.UserError("You don't have permission!")

        return super(ProductTemplateInherit, self).write(vals)

    @api.constrains('warrant_code')
    def _check_warrant_code(self):
        for record in self:
            if not record.has_valid_warrant_code():
                raise odoo.exceptions.UserError('Incorrectly formatted warrant code!')

    @api.depends('date_from', 'date_to')
    def _compute_warrant_code(self):
        for product in self:
            if product.date_from and product.date_to:
                product.warrant_code = fr"PWR/{product.date_from.strftime(WARRANT_CODE_DATE_FORMAT)}/{product.date_to.strftime(WARRANT_CODE_DATE_FORMAT)}"
            else:
                product.warrant_code = False

    @api.depends('date_from', 'date_to')
    def _compute_warrant_discount(self):
        today = fields.Date.today()
        for product in self:
            if not (product.date_from and product.date_to):
                product.warrant_discount = 10
            else:
                if product.date_from < today < product.date_to:
                    product.warrant_discount = 0
                else:
                    product.warrant_discount = 10

    @api.depends('date_from', 'date_to')
    def _compute_warrant_length(self):
        for product in self:
            if product.date_from and product.date_to:
                product.warrant_year = relativedelta(product.date_to, product.date_from).years
            else:
                product.warrant_year = 0

    def mass_update_warranty_code(self):
        """Called by the action in xml, return the wizard form"""
        ids = [x.id for x in self]
        view_id = self.env.ref('bai2.mass_update_product_warranty_code_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update warranty code',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'product.wizard',
            'target': 'new',
            'context': {
                'default_product_id': [(6, 0, ids)],
            }
        }
