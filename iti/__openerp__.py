{
    'name' : 'iti',
    'version' : '1.0',
    'author' : 'doaa',
    #'category' : 'Accounting & Finance',
    'depends': ['base_setup','mail', 'resource', 'board','report_webkit'],
    'description' : """iti module""",
    'data': [
        'iti_view.xml',
        'employee_view.xml',
        'store_view.xml',
        'product_view.xml',
        'product_workflow.xml',
        'search_view.xml',
        'category_view.xml',
        'security/iti_security.xml',
        'security/ir.model.access.csv',
        'report/stock.xml'
    ],
    'installable': True,
    'auto_install': False,
}
