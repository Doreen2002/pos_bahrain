# Copyright (c) 2026, 	9t9it and contributors
# For license information, please see license.txt

import frappe
from erpnext.stock.report.stock_ledger.stock_ledger import execute as stock_ledger_execute

def execute(filters=None):
	columns, data = [], []
	keys_remove = ['incoming_rate', 'valuation_rate', 'in_out_rate', 'stock_value']
	stock_ledger_columns, stock_ledger_data = stock_ledger_execute(filters)
	columns = [v for v in stock_ledger_columns if v.get('fieldname') not in keys_remove]
	data = stock_ledger_data
	return columns, data
