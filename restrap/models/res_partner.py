from odoo import fields, models, api

class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    def create(self, vals_list):
        vals_list['company_id'] = self.env.company.id
        return super(ResPartner, self).create(vals_list)
