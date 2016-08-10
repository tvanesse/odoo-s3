# -*- coding: utf-8 -*-
{
    'name': "Odoo-S3",

    'summary': """
        Allows you to use an AWS S3 bucket for file storage.""",

    'description': """
        Binary files such as attachments and pictures are stored by default in the file system of
        the host running Odoo. In some cases you may want to decrease the overall response time
        by delegating static file storage to a specialized instance such as an S3 bucket.
        This module allows you to configure Odoo so that an S3 bucket is
        used instead of the file system for binary files storage.
    """,

    'author': "Thomas Vanesse",
    'website': "http://www.creo2.org",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    'external_dependencies': {
        'python': ['boto'],
    },

    'installable': True
}