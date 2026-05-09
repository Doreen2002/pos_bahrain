# Copyright (c) 2026, 9T9IT and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	
	columns = [
		{
			"fieldname": "supplier",
			"label": "Supplier",
			"fieldtype": "Link",
			"options": "Supplier",
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname": "item_name",
			"label": "Item Name",
			"fieldtype": "Data",
		},
		{
			"fieldname": "purchase_qty",
			"label": "Purchase Quantity",
			"fieldtype": "Int",
		},
		{
			"fieldname": "sold_qty",
			"label": "Sold Quantity",
			"fieldtype": "Int",
		},
		{
			"fieldname": "out_qty",
			"label": "Out Quantity",
			"fieldtype": "Int",
		},
		{
			"fieldname": "expired_qty",
			"label": "Expired Quantity",
			"fieldtype": "Int",
		},
		{
			"fieldname": "current_stock",
			"label": "Current Stock",
			"fieldtype": "Int",
		}


	]

	query = frappe.db.sql(
    """
    SELECT 
        sp.name AS supplier,
        i.item_code,
        i.item_name,

        COALESCE(SUM(
            CASE 
                WHEN sle.voucher_type = 'Purchase Receipt' 
                THEN ABS(sle.actual_qty)
                ELSE 0 
            END
        ), 0) AS purchase_qty,

        COALESCE(SUM(
           CASE 
                WHEN sle.voucher_type = 'Sales Invoice' or sle.voucher_type = 'Delivery Note'
                THEN ABS(sle.actual_qty)
                ELSE 0
            END
        ), 0) AS sold_qty,

        COALESCE(SUM(
            CASE 
                WHEN sle.voucher_type = 'Stock Entry' 
                THEN ABS(sle.actual_qty)
                ELSE 0 
            END
        ), 0) AS out_qty,

        0 AS expired_qty,

        COALESCE(SUM(ABS(sle.actual_qty)), 0) AS current_stock

    FROM `tabSupplier` sp

    JOIN `tabItem Default` id 
        ON id.default_supplier = sp.name

    LEFT JOIN `tabItem` i 
        ON i.name = id.parent

    LEFT JOIN `tabStock Ledger Entry` sle 
        ON sle.item_code = i.item_code

	WHERE sle.posting_date BETWEEN %(startdate)s AND %(end_date)s

    GROUP BY 
        sp.name, i.item_code, i.item_name
    """,
    {
        "startdate": filters.get("start_date"),
        "end_date": filters.get("end_date")
    },
    as_dict=True,
)

	data = query
	return columns, data
