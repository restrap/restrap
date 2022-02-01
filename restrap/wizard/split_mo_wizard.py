from odoo import api, fields, models


class MrpSplitConfirmationWizard(models.TransientModel):
    _name = 'mrp.production.split.wizard'

    def action_confirm(self):
        active_ids = self._context.get('active_ids', [])
        production_id = self.env['mrp.production'].browse(active_ids)
        production_id.action_spilt()
