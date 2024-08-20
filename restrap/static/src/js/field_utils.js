/** @odoo-module **/

import { registry } from "@web/core/registry";
import { formatFloat as originalFormatFloat, humanNumber, insertThousandSeparators } from "@web/core/utils/numbers";
import { FloatField } from "@web/views/fields/float/float_field";
import { patch } from "@web/core/utils/patch";

function formatFloat(value, field, options) {
    options = options || {};
    if (value === false) {
        return "";
    }
    if (options.humanReadable && options.humanReadable(value)) {
        return humanNumber(value, options.decimals, options.minDigits, options.formatterCallback);
    }
    const l10n = registry.category("database.parameters").current;
    let precision;
    if (options.digits) {
        precision = options.digits[1];
    } else if (field && field.digits) {
        precision = field.digits[1];
    } else {
        precision = 2;
    }
    const formatted = _.str.sprintf('%.' + precision + 'f', value || 0).split('.');
    formatted[0] = insertThousandSeparators(formatted[0]);

    if (field) {
        if (['product_uom_qty', 'qty_delivered', 'qty_invoiced', 'qty_to_invoice', 'product_qty', 'quantity'].includes(field.name)) {
            return formatted.join(l10n.decimal_point).replace(/0+$/g, "").replace(/[.]$/, "");
        } else {
            return formatted.join(l10n.decimal_point);
        }
    }
}

patch(FloatField.prototype, {
    formatFloat: formatFloat
});

export { formatFloat };
