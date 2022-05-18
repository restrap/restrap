# -*- coding: utf-8 -*-
{
    "name": "Restrap Module",
    "version": "15.0.1",
    "author": "Smart IT Ltd",
    "category": "Other",
    "summary": "Restrap Smart IT Developments",
    'description': "Custom module for Restrap developed by Smart IT Ltd",
    'maintainer': "Smart IT Ltd",
    'website': 'smart-ltd.co.uk',
    "depends": ['base', 'mrp_workorder', 'sale_management', 'delivery'],
    "data": [
        'security/mrp_security.xml',
        'security/ir.model.access.csv',
        'wizard/sale_order_merge_wizard.xml',
        'wizard/split_mo_wizard.xml',
        'views/res_config_settings_view.xml',
        'views/mrp_production_views.xml',
        'views/mrp_workorder_views.xml',
        'views/sale_order_views.xml',
        'views/mrp_bom_views.xml',
        'views/product_views.xml',
        'report/mrp_production_templates.xml',
        'views/product_views.xml',
        'views/mrp_routing_workcenter_views.xml',
        'views/res_company_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'restrap/static/src/js/field_utils.js',
            ]
    },
    'license': 'LGPL-3',
}