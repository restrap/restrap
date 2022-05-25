odoo.define('restrap.field_utils', function (require) {
    "use strict";

var core = require('web.core');
var field_utils = require('web.field_utils');
var utils = require('web.utils');
var session = require('web.session');

function formatFloat(value, field, options) {
    options = options || {};
    if (value === false) {
        return "";
    }
    if (options.humanReadable && options.humanReadable(value)) {
        return utils.human_number(value, options.decimals, options.minDigits, options.formatterCallback);
    }
    var l10n = core._t.database.parameters;
    var precision;
    if (options.digits) {
        precision = options.digits[1];
    } else if (field && field.digits) {
        precision = field.digits[1];
    } else {
        precision = 2;
    }
    var formatted = _.str.sprintf('%.' + precision + 'f', value || 0).split('.');
    formatted[0] = utils.insert_thousand_seps(formatted[0]);

    if (field){
        if (field.name == 'product_uom_qty' || field.name == 'qty_delivered' || field.name == 'qty_invoiced'
            || field.name == 'qty_to_invoice' || field.name == 'product_qty' || field.name == 'quantity'){
            return formatted.join(l10n.decimal_point).replace(/0+$/g, "").replace(/[.]$/,"");
        }
        else {
            return formatted.join(l10n.decimal_point);
        }
    }

}

field_utils.format.float = formatFloat;

});
