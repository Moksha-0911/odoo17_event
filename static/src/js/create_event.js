/** @odoo-module **/
odoo.define('Event_management.custom_button', function (require) {
    "use strict";

    // Import necessary Odoo modules
    const ListView = require('web.ListView');
    const { action_manager } = require('web.core');

    ListView.include({
        events: {
            ...ListView.prototype.events, // Preserve existing events
            'click .o_list_button_add': 'openEventForm',  // Custom handler for Add button click
        },

        /**
         * This function is triggered when the 'Add New' button is clicked.
         */
        openEventForm: function (ev) {
            ev.preventDefault();  // Prevent the default action



            // Trigger an action to open the form view in a modal
            this.do_action({
                type: 'ir.actions.act_window',
                name: 'Create Event',  // Name for the window
                res_model: 'event.management',   // Model for the form view
                views: [[false, 'form']], // Open in form view
                target: 'new',  // Open in a modal window
            });
        },
    });
});

