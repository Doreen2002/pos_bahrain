import frappe
import json
from frappe import _
from collections import  defaultdict

def get_batch_qty(
	batch_no=None,
	warehouse=None,
	item_code=None,
	creation=None,
	posting_date=None,
	posting_time=None,
	ignore_voucher_nos=None,
	for_stock_levels=False,
	consider_negative_batches=False,
	do_not_check_future_batches=False,
	ignore_reserved_stock=False,
):
	"""Returns batch actual qty if warehouse is passed,
	        or returns dict of qty by warehouse if warehouse is None

	The user must pass either batch_no or batch_no + warehouse or item_code + warehouse

	:param batch_no: Optional - give qty for this batch no
	:param warehouse: Optional - give qty for this warehouse
	:param item_code: Optional - give qty for this item
	:param for_stock_levels: True consider expired batches"""

	from erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle import (
		get_auto_batch_nos,
	)

	batchwise_qty = defaultdict(float)
	kwargs = frappe._dict(
		{
			"item_code": item_code,
			"warehouse": warehouse,
			"creation": creation,
			"posting_date": posting_date,
			"posting_time": posting_time,
			"batch_no": batch_no,
			"based_on": frappe.get_single_value("Stock Settings", "pick_serial_and_batch_based_on"),
			"ignore_voucher_nos": ignore_voucher_nos,
			"for_stock_levels": for_stock_levels,
			"consider_negative_batches": consider_negative_batches,
			"do_not_check_future_batches": do_not_check_future_batches,
			"ignore_reserved_stock": ignore_reserved_stock,
		}
	)

	batches = get_auto_batch_nos(kwargs)

	if not (batch_no and warehouse):
		return batches

	for batch in batches:
		batchwise_qty[batch.get("batch_no")] += batch.get("qty")

	return batchwise_qty[batch_no]

def recalculate_batch_qty(self):
    batches = get_batch_qty(
        batch_no=self.name,
        item_code=self.item,
        for_stock_levels=True,
        consider_negative_batches=True,
        ignore_reserved_stock=True,
    )

    batch_qty = 0.0
    if batches:
        for row in batches:
            batch_qty += row.get("qty")

    if self.batch_qty != batch_qty:
        self.db_set("batch_qty", batch_qty)

    frappe.msgprint(_("Batch Qty updated to {0}").format(batch_qty), alert=True)


@frappe.whitelist()
def recalculate_batch_quantities(doc):
    doc = json.loads(doc)
    batch_doc = frappe.get_doc("Batch", doc.get("name"))
    recalculate_batch_qty(batch_doc)
    frappe.db.commit()
    batch_doc.reload()
    return batch_doc
    

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def batch_query(doctype, txt, searchfield, start, page_len, filters):
    query = """
        SELECT
            b.name,
            b.item,
            i.item_name,
            b.expiry_date
        FROM `tabBatch` AS b
        JOIN `tabItem` AS i ON i.name = b.item
        WHERE b.name LIKE {txt}
        OR b.item LIKE {txt}
        OR i.item_name LIKE {txt}
        OR b.expiry_date LIKE {txt}
        LIMIT {start}, {page_len}
    """.format(
        txt=frappe.db.escape("%{0}%".format(txt)),
        start=start,
        page_len=page_len,
    )

    return frappe.db.sql(query)
