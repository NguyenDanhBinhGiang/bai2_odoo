# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Bai 2",
    'summary': "A test add-on",
    'author': "me",
    'category': 'Administration',
    'depends': ['sale', 'base', 'website_sale'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/product_template_inherit_view.xml',
        'views/oder_line_inherit.xml',
        'views/order_inherit.xml',
    ],
}
