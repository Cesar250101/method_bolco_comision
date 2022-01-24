# -*- coding: utf-8 -*-
{
    'name': "method_bolco_comision",

    'summary': """
        Calculo de comisiones Bolco""",

    'description': """
        Cálculo comisiones bolco, el resueltado del proceso es
        que inserta un haber en la nomina
    """,

    'author': "Method ERP",
    'website': "https://www.method.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','hr_payroll','l10n_cl_hr','stock',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        #'report/comisiones_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}