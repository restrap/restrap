from odoo import fields, models, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    total_weight = fields.Float(string='Total Weight', compute="get_total_weight")

    @api.depends('product_id')
    def get_total_weight(self):
        for line in self:
            if line.product_id:
                line.total_weight = line.product_id.weight * line.qty_done
            else:
                line.total_weight = 0

