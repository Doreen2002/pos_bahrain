# Copyright (c) 2025, 	9t9it and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    static_columns = get_static_columns()
    static_data = get_static_data(filters)

    item_codes = [item['item_code'] for item in static_data]
    dynamic_columns = get_dynamic_columns(filters, item_codes)

    columns = static_columns + dynamic_columns
    dynamic_data = get_dynamic_data(filters, dynamic_columns)

    data = merge_data(static_data, dynamic_data, dynamic_columns, filters)

    return columns, data

def get_static_columns():
    return [
        {"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 100},
        {"label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 100},
        {"label": _("Item Group"), "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 100},
        {"label": _("Default Supplier"), "fieldname": "default_supplier", "fieldtype": "Link", "options": "Supplier", "width": 100},
        {"label": _("Qty"), "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": _("Standard Selling Price"), "fieldname": "selling_price", "fieldtype": "Currency", "width": 100},
        {"label": _("Standard Buying Price"), "fieldname": "buying_price", "fieldtype": "Currency", "width": 100},
        {"label": _("WholeSale Price"), "fieldname": "wholesale_price", "fieldtype": "Currency", "width": 100},
        {"label": _("Landed Cost"), "fieldname": "landed_cost", "fieldtype": "Currency", "width": 100},
        {"label": _("Valuation Rate"), "fieldname": "valuation_rate", "fieldtype": "Currency", "width": 100},
        {"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 100},
        {"label": _("WH1 Retail Price"), "fieldname": "wh1_retail_price", "fieldtype": "Currency", "width": 100},
        {"label": _("WH1 Profit"), "fieldname": "wh1_profit", "fieldtype": "Currency", "width": 100},
        {"label": _("WH1 Profit %"), "fieldname": "wh1_profit_per", "fieldtype": "Data", "width": 100},
        {"label": _("WH2 Retail Price"), "fieldname": "wh2_retail_price", "fieldtype": "Currency", "width": 100},
        {"label": _("WH2 Profit"), "fieldname": "wh2_profit", "fieldtype": "Currency", "width": 100},
        {"label": _("WH2 Profit %"), "fieldname": "wh2_profit_per", "fieldtype": "Data", "width": 100},
    ]

def get_dynamic_columns(filters, item_codes):
    dynamic_columns = []
    settings = frappe.get_single("POS Bahrain Settings")
    
    price_list = settings.apply_offer_pricelist
    
    if price_list:
        for price_list in price_list:
            dynamic_column_name = price_list.price_list.lower().replace(" ", "_")
            if item_prices_exist(price_list.price_list, item_codes):
                column = {"label": _(price_list.price_list), "fieldname": dynamic_column_name, "fieldtype": "Currency", "width": 100}
                dynamic_columns.append(column)
    return dynamic_columns

def item_prices_exist(price_list_name, item_codes):
    return frappe.db.exists('Item Price', {
        'price_list': price_list_name,
        'item_code': ['in', item_codes]
    })

def get_where_clause(filters):
    where_clause = ""
    if filters.get('item'):
        where_clause += "AND ti.name = '{}' ".format(filters.get('item'))
    if filters.get('item_group'):
        where_clause += "AND ti.item_group = '{}' ".format(filters.get('item_group'))
    if filters.get('warehouse'):
        where_clause += "AND tw.name = '{}' ".format(filters.get('warehouse'))
    if not filters.get('show_item_in_stock'):
        where_clause += """AND IFNULL((SELECT tsle.qty_after_transaction 
                                       FROM `tabStock Ledger Entry` tsle 
                                       WHERE tsle.item_code = ti.name 
                                       AND tsle.warehouse = tw.name 
                                       AND tsle.posting_date BETWEEN '{}' AND '{}' 
                                       ORDER BY tsle.posting_date DESC 
                                       LIMIT 1), 0) = 0 """.format(filters.get('from_date'), filters.get('date'))
    if filters.get('show_item_in_stock'):
        where_clause += """AND IFNULL((SELECT tsle.qty_after_transaction 
                                       FROM `tabStock Ledger Entry` tsle 
                                       WHERE tsle.item_code = ti.name 
                                       AND tsle.warehouse = tw.name 
                                       AND tsle.posting_date BETWEEN '{}' AND '{}' 
                                       ORDER BY tsle.posting_date DESC 
                                       LIMIT 1), 0) > 0 """.format(filters.get('from_date'), filters.get('date'))
    return where_clause


def get_static_data(filters):
    where_clause = get_where_clause(filters)

    sql_query = """
        SELECT 
            ti.name AS item_code,
            ti.item_name AS item_name,
            ti.item_group AS item_group,
            IFNULL(id.default_supplier, '') AS default_supplier,
            IFNULL((SELECT tsle.qty_after_transaction 
                FROM `tabStock Ledger Entry` tsle 
                WHERE tsle.item_code = ti.name 
                AND tsle.warehouse = tw.name 
                AND tsle.posting_date BETWEEN %(from_date)s AND %(date)s 
                ORDER BY tsle.posting_date DESC LIMIT 1),0) AS qty,
                 IFNULL((SELECT tsle.valuation_rate 
                FROM `tabStock Ledger Entry` tsle 
                WHERE tsle.item_code = ti.name 
                AND tsle.warehouse = tw.name 
                AND tsle.posting_date BETWEEN %(from_date)s AND %(date)s 
                ORDER BY tsle.posting_date DESC LIMIT 1), 0) AS landed_cost, 
            CASE 
                WHEN %(use_manual_price)s = 1 THEN 
                    IFNULL((SELECT price_list_rate 
                    FROM `tabItem Price` 
                    WHERE item_code = ti.name  AND uom = ti.stock_uom
                    AND price_list = 'WholeSale Price' ORDER BY creation DESC LIMIT 1), 0)    
                ELSE 
                    IFNULL((
                            SELECT tsle.incoming_rate 
                            FROM `tabStock Ledger Entry` tsle 
                            WHERE tsle.item_code = ti.name 
                            AND tsle.warehouse = tw.name 
                            AND tsle.posting_date BETWEEN %(from_date)s AND %(date)s 
                            ORDER BY tsle.posting_date DESC, tsle.creation DESC 
                            LIMIT 1
                        ), 0)   
            END AS wholesale_price, 
            IFNULL((SELECT tsle.valuation_rate 
                FROM `tabStock Ledger Entry` tsle 
                WHERE tsle.item_code = ti.name 
                AND tsle.warehouse = tw.name 
                AND tsle.posting_date BETWEEN %(from_date)s AND %(date)s 
                ORDER BY tsle.posting_date DESC LIMIT 1),0) AS valuation_rate,
            tw.name as warehouse, 
            IF(selling_price.price_list = 'Standard Selling', selling_price.price_list_rate, NULL) AS selling_price,
            IF(buying_price.price_list = 'Standard Buying', buying_price.price_list_rate, NULL) AS buying_price
        FROM 
            tabItem AS ti
        CROSS JOIN 
            tabWarehouse tw
        INNER JOIN
            `tabItem Default` id ON ti.name = id.parent
        LEFT JOIN
            (SELECT item_code, price_list_rate, price_list FROM `tabItem Price` WHERE price_list = 'Standard Selling') AS selling_price
            ON selling_price.item_code = ti.name
        LEFT JOIN
            (SELECT item_code, price_list_rate, price_list FROM `tabItem Price` WHERE price_list = 'Standard Buying') AS buying_price
            ON buying_price.item_code = ti.name
        WHERE 
            ti.disabled = 0 
            AND ti.is_stock_item = 1
            {where_clause}
        LIMIT 10000
    """.format(where_clause=where_clause) 
    
    data = frappe.db.sql(sql_query, 
                         values = {"from_date": filters.get('from_date'), "date": filters.get('date'), 'use_manual_price': filters.get('use_manual_price')}, 
                         as_dict=True)
    return data

def get_dynamic_data(filters, dynamic_columns):
    dynamic_data = {}
    for column in dynamic_columns:
        price_list_name = column['label']
        fieldname = column['fieldname']
        price_data = frappe.db.sql("""
            SELECT 
                item_code, 
                price_list_rate 
            FROM 
                `tabItem Price`
            WHERE 
                price_list = %s
        """, price_list_name, as_dict=True)
        
        for item in price_data:
            if item.item_code not in dynamic_data:
                dynamic_data[item.item_code] = {}
            dynamic_data[item.item_code][fieldname] = item.price_list_rate

    return dynamic_data

def merge_data(static_data, dynamic_data, dynamic_columns, filters):
    for item in static_data:
        item_code = item['item_code']
        if item_code in dynamic_data:
            item.update(dynamic_data[item_code])
        else:
            for column in dynamic_columns:
                item[column['fieldname']] = None
        item['wh1_retail_price'] = item.get('selling_price') * ((100 - filters.get('wh1_margin', 0)) / 100) if item.get('selling_price') is not None else None
        item['wh2_retail_price'] = item.get('selling_price') * ((100 - filters.get('wh2_margin', 0)) / 100) if item.get('selling_price') is not None else None
        item['wh1_profit'] =  item['wh1_retail_price'] -  item['landed_cost']  if item.get('wh1_retail_price') is not None else None
        item['wh2_profit'] =  item['wh2_retail_price'] - item['landed_cost']   if item.get('wh2_retail_price') is not None else None
        item['wh1_profit_per'] =f"{item['wh1_profit']/item['landed_cost'] * 100 if item['landed_cost'] != 0 else 0} %" if item['wh1_profit'] is not None else '0 %'
        item['wh2_profit_per'] =f"{item['wh2_profit']/item['landed_cost'] * 100 if item['landed_cost'] != 0 else 0} %" if item['wh2_profit'] is not None else '0 %'

    return static_data
