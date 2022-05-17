# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import logging
from odoo import http, _
from odoo.http import request
import odoo
from odoo.addons.auth_signup.controllers.main import AuthSignupHome as Home
from odoo.addons.web.controllers.main import Home as WebHome , ensure_db

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# Controller
#----------------------------------------------------------
class ShWebLogin(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
            # Redirect if already logged in and redirect param is present
            return request.redirect(request.params.get('redirect'))

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                draft_user = request.env['res.users'].sudo().search(
                [('login', '=', request.params['login']), ('sh_user_from_signup', '=', True), ('status', '=', 'draft')])
                rejected_user = request.env['res.users'].sudo().search(
                [('login', '=', request.params['login']), ('sh_user_from_signup', '=', True), ('status', '=', 'rejected')])
                if draft_user:
                    values['error'] = "Your account already registered! Please wait for account approval."
                    request.params['login_success'] = False
                elif rejected_user:
                    values['error'] = "Your account rejected by administrator."
                    request.params['login_success'] = False
                else:
                    uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
                    request.params['login_success'] = True
                    return request.redirect(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        response.qcontext.update(self.get_auth_signup_config())
        return response
