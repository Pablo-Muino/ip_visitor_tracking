{
    'name': 'Ip Visitor Tracking',
    'version': '1.0',
    'summary': 'Integración con la API de IpGeolocation',
    'description': 'Obtención de datos meteorológicos en tiempo real.',
    'author': 'Pablo Muiño',
    'category': 'Website',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ip_visitor_tracking_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'icon': '/ip_visitor_tracking/static/description/icon58.png'
}