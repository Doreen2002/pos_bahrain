import frappe
from erpnext.accounts.doctype.loyalty_program.loyalty_program import get_loyalty_program_details,get_loyalty_details

@frappe.whitelist(allow_guest=True)
def get_loyalty_program_details_with_points(
	customer,
	loyalty_program=None,
	expiry_date=None,
	company=None,
	silent=False,
	include_expired_entry=False,
	current_transaction_amount=0,
):
	lp_details = get_loyalty_program_details(customer, loyalty_program, company=company, silent=silent)
	loyalty_program = frappe.get_doc("Loyalty Program", loyalty_program)
	lp_details.update(
		get_loyalty_details(customer, loyalty_program.name, expiry_date, company, include_expired_entry)
	)

	tier_spent_level = sorted(
		[d.as_dict() for d in loyalty_program.collection_rules],
		key=lambda rule: rule.min_spent,
		reverse=True,
	)
	for i, d in enumerate(tier_spent_level):
		if (lp_details.total_spent + current_transaction_amount) >= d.min_spent:
			lp_details.tier_name = d.tier_name
			lp_details.collection_factor = d.collection_factor
		else:
			break

	return lp_details