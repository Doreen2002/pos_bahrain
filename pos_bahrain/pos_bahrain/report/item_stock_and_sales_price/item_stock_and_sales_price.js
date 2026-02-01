// Copyright (c) 2026, 	9t9it and contributors
// For license information, please see license.txt

frappe.query_reports["Item Stock and Sales Price"] = {
	"filters": [
		{
			fieldname: 'company',
			label: __('Company'),
			fieldtype: 'Link',
			options: 'Company',
			reqd: 1,
			default: frappe.defaults.get_default('company'),
			on_change:function()
			{
				frappe.query_report.set_filter_value('warehouse', "");
			}
		},
		{
			fieldname: 'warehouse',
			label: __('Warehouse'),
			fieldtype: 'Link',
			options: 'Warehouse',
			reqd: 1,
			get_query:function()
			{
				return{
					filters:{
						'company':frappe.query_report.filters[0].value
					}
				}
			}
			
		},
		{
			fieldname: 'from_date',
			label: __('From Date'),
			fieldtype: 'Date',
			reqd: 1,
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: 'to_date',
			label: __('To Date'),
			fieldtype: 'Date',
			reqd: 1,
			default: frappe.datetime.get_today(),
		},
		{
			label: __('Hide Zero Stock Items'),
			fieldname: 'hide_zero_stock_items',
			fieldtype: 'Check',
			default: 0
		}

	],
	
};
