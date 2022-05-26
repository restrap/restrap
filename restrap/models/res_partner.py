from odoo import fields, models, api

class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    def create(self, vals_list):
        # BUG for ticket 28510.
        # FIX: can save new contacts.
        for vals in vals_list:
            vals['company_id'] = self.env.company.id
        return super(ResPartner, self).create(vals_list)
