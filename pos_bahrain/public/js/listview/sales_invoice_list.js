 

const original_before_render = frappe.listview_settings['Sales Invoice']["before_render"];

frappe.listview_settings['Sales Invoice']["before_render"] =  async function (listview) {
  if(original_before_render)
  {
     original_before_render(listview);
  }
    await frappe.db
      .get_doc('Report', 'Daily Cash with Payment')
      .then((r) => {
        console.log(r);
        const allowed_roles = r.roles;
        const user_roles = frappe.user_roles;
        if (r.roles.length > 0) {
          const has_access = allowed_roles.some((role) =>
            user_roles.includes(role.role)
          );

          if (!has_access) {
            if (frappe.get_route()[2] === 'Report') {
              frappe.msgprint(
                __('You are not permitted to view the Report view.')
              );
              frappe.set_route('List', 'Sales Invoice/List');
            }
          }
        } else {
          if (frappe.get_route()[2] === 'Report') {
            frappe.msgprint(
              __('You are not permitted to view the Report view.')
            );
            frappe.set_route('List', 'Sales Invoice/List');
          }
        }
      })
      .catch((e) => console.log(e));
  };

  
