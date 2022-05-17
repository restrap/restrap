# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'User Approval',
    'author': 'Softhealer Technologies',
    'website': 'http://www.softhealer.com',
    "support": "support@softhealer.com",
    'category': 'Website',
    'summary': "Approve Signup Users,Signup User Approval, Manage Signup Users,User Reverification App, User Rejection By Admin, Mass User Approve Module, Multiple Users Approve, Bulk User Reject Odoo",
    'description': """Approve Signup Users module manage user signup approval process, the admin can approve or reject the account request of the user. This module provides approval or rejects functionality for all new users after sign up. This module provides security to avoid fake user so the first verified user and then activated that account. Once the account is approved or rejects the user gets an email notification. Only approved users can log in into the website & restricted users can't log in.""",
    'version': '15.0.1',
    'depends': [
        'web',
        'auth_signup',
        'portal'
    ],
    'application': True,
    'data': [
        'data/sh_approve_user_email_template.xml',
        'views/user_signup_approve_view.xml',
        'views/user_signup_template.xml',
    ],
    'images': ['static/description/background.png', ],
    "live_test_url": "https://youtu.be/7GseqDnUodI",
    "license": "OPL-1",
    'auto_install': False,
    'installable': True,
    "price": 35,
    "currency": "EUR"
}
