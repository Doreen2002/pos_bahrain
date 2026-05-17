// Copyright (c) 2026, 9T9IT and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Movement Summary"] = {
	"filters": [
		{
			"fieldname": "start_date",
			"label": "Start Date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -30)
		},
		{
			"fieldname": "end_date",
			"label": "End Date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "supplier",
			"label": "Supplier",
			"fieldtype": "MultiSelectList",
			"options": "Supplier",
			get_data: function(txt) {
				return frappe.db.get_link_options('Supplier', txt);
					}
		},
		{
			"fieldname": "warehouse",
			"label": "Warehouse",
			"fieldtype": "Link",
			"options": "Warehouse"
		}
	]
	
};
