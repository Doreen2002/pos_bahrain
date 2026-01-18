import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def after_install():
    fields = [
    {
        "label": _("Series"),
        "fieldname": "naming_series",
        "fieldtype": "Select",
        "options":"[Select]",
        "reqd":1,
        "in_list_view":1,
        "insert_after": "company",
    },
    {"custom_field_name":"POS Profile-custom_pos_opening_series_",
    "fieldname": "custom_pos_opening_series_",
    "label": "POS Opening Series ",
    "fieldtype": "Select",
    "reqd": 1,
    "insert_after": "naming_series",
    "options": ""
    },
    {"custom_field_name":"POS Profile-custom_pos_closing_series_",
    "fieldname": "custom_pos_closing_series_",
    "label": "POS Closing Series",
    "fieldtype": "Select",
    "reqd": 1,
    "insert_after": "custom_pos_opening_series_",
    "options": ""
    }

    ]
    for field in fields:
        if not frappe.db.exists("Custom Field", field.get("custom_field_name")):
            create_custom_field("POS Profile", {
            "fieldname": field.get("fieldname"),
            "label": field.get("label"),
            "fieldtype": field.get("fieldtype"),
            "reqd": field.get('reqd'),
            "insert_after": field.get("insert_after"),
            "options": field.get("options"),
            "is_system_generated":0,
            "module": "pos",
            })
    frappe.db.commit()
