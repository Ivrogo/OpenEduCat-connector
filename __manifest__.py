{
    'name': 'OpenEduCat Moodle Connector',
    'version': '1.0',
    'summary': 'Integration between OpenEduCat and Moodle',
    'category': 'Education',
    'author': 'Your Name',
    'depends': ['base', 'openeducat_core'],
    'data': [
        'data/moodle_data.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}