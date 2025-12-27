// Copyright (c) 2016, 	9t9it and contributors
// For license information, please see license.txt
/* eslint-disable */


frappe.query_reports["Sales Register with Employee"] = {
  "filters": [],
  "onload": async function (report) {
      const source_report = "Sales Register";
      if (!frappe.query_reports[source_report]) {
          const base = new frappe.views.QueryReport();
          base.report_name = source_report;
          await base.get_report_doc();
          await base.get_report_settings();
      }
      const custom_filters = [
          {
              fieldname: 'sales_employee',
              label: __('Sales Employee'),
              fieldtype: 'Link',
              options: 'Employee',
          },
          {
              fieldname: 'commission_rate',
              label: __('Commission Rate (%)'),
              fieldtype: 'Float',
          }
      ];
      const original_filters = frappe.query_reports[source_report].filters || [];
      report.report_settings.filters = [...original_filters, ...custom_filters];
      report.setup_filters();
  }
};
