// Copyright (c) 2016, 	9t9it and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['Stock Balance with Prices'] = {
  filters: [
    {
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			width: "80",
			options: "Company",
			default: frappe.defaults.get_default("company"),
		},
    {
      fieldname: 'from_date',
      label: __('From Date'),
      fieldtype: 'Date',
      width: '80',
      reqd: 1,
      default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
    },
    
    {
      fieldname: 'to_date',
      label: __('To Date'),
      fieldtype: 'Date',
      width: '80',
      reqd: 1,
      default: frappe.datetime.get_today(),
    },
    {
      fieldname: 'item_group',
      label: __('Item Group'),
      fieldtype: 'Link',
      width: '80',
      options: 'Item Group',
    },
    {
      fieldname: 'brand',
      label: __('Brand'),
      fieldtype: 'Link',
      options: 'Brand',
    },
    {
			fieldname: "item_code",
			label: __("Items"),
			fieldtype: "MultiSelectList",
			width: "80",
			options: "Item",
			get_data: async function (txt) {
				let item_group = frappe.query_report.get_filter_value("item_group");

				let filters = {
					...(item_group && { item_group }),
					is_stock_item: 1,
				};

				let { message: data } = await frappe.call({
					method: "erpnext.controllers.queries.item_query",
					args: {
						doctype: "Item",
						txt: txt,
						searchfield: "name",
						start: 0,
						page_len: 10,
						filters: filters,
						as_dict: 1,
					},
				});

				data = data.map(({ name, ...rest }) => {
					return {
						value: name,
						description: Object.values(rest),
					};
				});

				return data || [];
			},
		},
		{
			fieldname: "warehouse",
			label: __("Warehouses"),
			fieldtype: "MultiSelectList",
			width: "80",
			options: "Warehouse",
			get_data: (txt) => {
				let warehouse_type = frappe.query_report.get_filter_value("warehouse_type");
				let company = frappe.query_report.get_filter_value("company");

				let filters = {
					...(warehouse_type && { warehouse_type }),
					...(company && { company }),
				};

				return frappe.db.get_link_options("Warehouse", txt, filters);
			},
		},
    {
      fieldname: 'supplier',
      label: __('Supplier'),
      fieldtype: 'Link',
      width: '80',
      options: 'Supplier',
    },
    {
      fieldname: 'include_uom',
      label: __('Include UOM'),
      fieldtype: 'Link',
      options: 'UOM',
    },
    {
      fieldname: 'show_variant_attributes',
      label: __('Show Variant Attributes'),
      fieldtype: 'Check',
    },
  ],
};
