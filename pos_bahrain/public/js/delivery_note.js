frappe.provide('pos_bahrain.scripts.extensions');

frappe.ui.form.on('Delivery Note', {
  refresh: function (frm) {
    pos_bahrain.scripts.extensions.hide_sales_return('Sales Return', 'Create');
  },
});
