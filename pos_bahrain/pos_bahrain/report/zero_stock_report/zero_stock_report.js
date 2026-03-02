// Copyright (c) 2025, 	9t9it and contributors
// For license information, please see license.txt

frappe.query_reports["Zero Stock Report"] = {
	"filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -120),
            "reqd": 1
        },
		{
            "fieldname": "date",
            "label": __("Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "item",
            "label": __("Item"),
            "fieldtype": "Link",
            "options":"Item",
        },
		{
            "fieldname": "item_group",
            "label": __("Item Group"),
            "fieldtype": "Link",
            "options":"Item Group",
        },
		{
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options":"Warehouse",
        },
		{
            "fieldname": "show_item_in_stock",
            "label": __("Show item in stock"),
            "fieldtype": "Check",
        },
        {
            "fieldname": "wh1_margin",
            "label": __("WH1 Margin"),
            "fieldtype": "Float",
            'default': 0.0,
        },
        {
            "fieldname": "wh2_margin",
            "label": __("WH2 Margin"),
            "fieldtype": "Float",
            'default': 0.0,
        },
        {
            "fieldname": "use_manual_price",
            "label": __("Use Manual Price"),
            "fieldtype": "Check",
        },

	],
    onload: function(report) {
        if (!frappe.user.has_role("Accounts Manager")) {
            report.get_filter("wh1_margin").toggle(false);
            report.get_filter("wh2_margin").toggle(false);
        }
    }
};
