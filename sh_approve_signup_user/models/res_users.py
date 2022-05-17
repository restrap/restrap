# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, _
from ast import literal_eval
from odoo.tools.misc import ustr

from odoo.addons.auth_signup.models.res_partner import SignupError


class ShUsers(models.Model):
    _inherit = 'res.users'

    sh_user_from_signup = fields.Boolean('User From Signup ?')
    sh_portal_users = fields.Boolean(
        "portal Users", compute='_compute_portal_user', store=True)

    status = fields.Selection([('draft', 'Need Approval'), ('approved', 'Approved'), (
        'rejected', 'Rejected')], string="State ", default='draft')

    def _compute_portal_user(self):
        if self:
            for rec in self:
                if rec.has_group('base.group_portal'):
                    rec.sh_portal_users = True
                else:
                    rec.sh_portal_users = False

    def action_approve_user(self):
        template = self.env.ref(
            'sh_approve_signup_user.sh_signup_user_approve', raise_if_not_found=False)
        if template:
            template.sudo().send_mail(self.id, force_send=True,
                                      notif_layout='mail.mail_notification_light')
        self.write({'status': 'approved'})

    def action_reject_user(self):
        template = self.env.ref(
            'sh_approve_signup_user.sh_signup_user_reject', raise_if_not_found=False)
        if template:
            template.sudo().send_mail(self.id, force_send=True,
                                      notif_layout='mail.mail_notification_light')
        self.write({'status': 'rejected'})

    def action_draft_user(self):
        self.write({'status': 'draft'})

    def _create_user_from_template(self, values):
        template_user_id = literal_eval(self.env['ir.config_parameter'].sudo(
        ).get_param('base.template_portal_user_id', 'False'))
        template_user = self.browse(template_user_id)
        if not template_user.exists():
            raise ValueError(_('Signup: invalid template user'))

        if not values.get('login'):
            raise ValueError(_('Signup: no login given for new user'))
        if not values.get('partner_id') and not values.get('name'):
            raise ValueError(
                _('Signup: no name or partner given for new user'))

        # create a copy of the template user (attached to a specific partner_id if given)
        values['active'] = True
        values['sh_user_from_signup'] = True
        values['status'] = 'draft'
        try:
            with self.env.cr.savepoint():
                return template_user.with_context(no_reset_password=True).copy(values)
        except Exception as e:
            # copy may failed if asked login is not available.
            raise SignupError(ustr(e))
