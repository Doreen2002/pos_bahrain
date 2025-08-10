# Copyright (c) 2025, 	9t9it and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, flt
from pos_bahrain.utils.report import make_column, with_report_generation_time


from frappe.utils import flt
from collections import defaultdict

def execute(filters=None):
	columns = [
		make_column("item_code", "Item Code", "Link", 120, options="Item"),
		make_column("description", "Description", "Data", 200),
		make_column("qty", "Quantity", "Float", 80),
		make_column("net_amount", "Net Amount", "Currency", 100, precision=2),
		make_column("tax_amount", "Tax Amount", "Currency", 100, precision=2),
		make_column("gross_amount", "Gross Amount", "Currency", 100, precision=2)
	]

	all_items = frappe.get_all(
		"Item",
		fields=["item_code", "description"]
	)


	item_sales = defaultdict(lambda: {
		"qty": 0.0,
		"net_amount": 0.0,
		"tax_amount": 0.0,
		"gross_amount": 0.0
	})

	invoices = frappe.get_all(
		"Sales Invoice",
		fields=["name"],
		filters={
			"docstatus": 1,
			"posting_date": ["between", [filters.get("from_date"), filters.get("to_date")]],
			"company": filters.get("company"),
		}
	)

	for invoice in invoices:
		doc = frappe.get_doc("Sales Invoice", invoice.name)
		for item in doc.items:
			tax_type = ""
			tax_rate = 0.0
			entry = item_sales[item.item_code]
			entry["qty"] += flt(item.qty)
			entry["net_amount"] += flt(item.net_amount)
			entry["tax_amount"] += (get_tax_rate( item) or 0)
			entry["gross_amount"] += flt(item.net_amount + (get_tax_rate( item) or 0))

	
	data = []
	for item in all_items:
		sales = item_sales.get(item.item_code, {
			"qty": 0.0,
			"net_amount": 0.0,
			"tax_amount": 0.0,
			"gross_amount": 0.0
		})
		data.append({
			"item_code": item.item_code,
			"description": item.description,
			"qty": sales["qty"],
			"net_amount": sales["net_amount"],
			"tax_amount": sales["tax_amount"],
			"gross_amount": sales["gross_amount"]
		})

	return columns, data



def get_tax_rate(item):
	if item.item_tax_template:
		try:
			return frappe.db.get_all("Item Tax Template Detail",
			filters={
				"parent": item.item_tax_template,
			},
			fields=["tax_rate"])[0].tax_rate
		except Exception:
			pass
