# -*- coding: utf-8 -*-

from odoo import api, fields, models


class WebsiteMenu(models.Model):
    _inherit = "website"

    allow_out_of_stock_order = fields.Boolean(
        string='Continue selling when out-of-stock',
        default=False)
    website_suffix = fields.Char(
        string='Suffix',)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        # Check if the order is created from the website
        if  'website_id' in vals:
            website = self.env['website'].search([("id","=",vals['website_id'])])
            if website.website_suffix:
                suffix = website.website_suffix  # Define your suffix here
                # Get the next order sequence number
                seq = self.env['ir.sequence'].next_by_code('sale.order')
                # Create the order name with suffix
                vals['name'] = f"{seq}{suffix}"
            else:
                seq = self.env['ir.sequence'].next_by_code('sale.order')


        # Call the super method to create the record
        return super(SaleOrder, self).create(vals)