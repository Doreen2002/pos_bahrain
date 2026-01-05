# -*- coding: utf-8 -*-
# Copyright (c) 2019, 	9t9it and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from pos_bahrain.doc_events.purchase_receipt import set_or_create_batch
from pos_bahrain.doc_events.sales_invoice import set_cost_center


def before_validate(doc, method):
    set_or_create_batch(doc, method)

       
def before_submit(doc,method):
    settings = frappe.get_single('POS Bahrain Settings')
    if settings.validate_duplicate_supplier_invoice_numbers:
        if frappe.db.exists("Purchase Invoice", {"bill_no": doc.bill_no, "name": ["!=", doc.name]}):
            frappe.throw(
                frappe._("Purchase Invoice with Supplier Invoice No {0} already exists").format(doc.bill_no)
            )


def before_save(doc, method):
    set_cost_center(doc)


