# Copyright (c) 2026, 	9t9it and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = [
		{"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150},
		{"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
		{"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 150},
		{"label": "Barcode", "fieldname": "barcode", "fieldtype": "Data",  "width": 150},
		{"label": "Warehouse Quantity", "fieldname": "warehouse_quantity", "fieldtype": "Float", "width": 120},
		{"label": "Selling Price", "fieldname": "selling_price", "fieldtype": "Currency", "width": 120},
		
	]
	
	if "Accounts Manager" in  frappe.get_roles(frappe.session.user):
		columns.append(
			{"label": "Valuation Rate", "fieldname": "valuation_rate", "fieldtype": "Currency", "width": 150}
		)
	data = frappe.db.sql("""
		SELECT
		i.name,
		i.item_code as item_code,
		i.item_name as item_name,
		i.item_group as item_group,
		id.default_price_list,
		 ib.barcode as barcode,
		(SELECT SUM(actual_qty) FROM `tabBin` WHERE `tabBin`.item_code = i.name AND `tabBin`.warehouse = %(warehouse)s) as warehouse_quantity,
		(SELECT price_list_rate FROM `tabItem Price` WHERE `tabItem Price`.item_code = i.name AND `tabItem Price`.price_list = id.default_price_list LIMIT 1) as selling_price,
		(SELECT valuation_rate FROM `tabStock Ledger Entry` WHERE `tabStock Ledger Entry`.item_code = i.name AND `tabStock Ledger Entry`.warehouse = %(warehouse)s AND `tabStock Ledger Entry`.voucher_type = 'Sales Invoice' ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC, `tabStock Ledger Entry`.creation DESC LIMIT 1) as valuation_rate
		FROM `tabItem` as i
		LEFT JOIN `tabItem Barcode` as ib ON i.name = ib.parent
		LEFT JOIN `tabItem Default` as id ON  i.name = id.parent AND id.company = %(company)s
		WHERE disabled = 0
			""", as_dict=1, values={'warehouse':filters.get('warehouse'), 'company':filters.get('company')})
		 
	return columns, data
