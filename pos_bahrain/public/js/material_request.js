frappe.ui.form.on("Material Request", {
  refresh: function (frm) {
    _make_custom_buttons(frm);
  },
});


function _make_custom_buttons(frm) {
  if (frm.doc.docstatus !== 1) {
    return;
  }
  if (frm.doc.material_request_type === "Material Transfer" && frappe.user.has_role("Stock Manager")) {
    frm.add_custom_button(__("Stock Transfer"), () => _make_stock_transfer(frm));
  }
}


function _make_stock_transfer(frm) {
  frappe.model.open_mapped_doc({
      method: "pos_bahrain.api.material_request.make_stock_entry",
      frm: frm
  });
}