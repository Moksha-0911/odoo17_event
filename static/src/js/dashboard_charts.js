odoo.define('Event_management.dashboard_charts', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.EventDashboardCharts = publicWidget.Widget.extend({
        selector: '.event_dashboard_container',  // Target your dashboard div
        start: function () {
            this._renderCharts();
        },
        _renderCharts: function () {
            var ctx = document.getElementById("eventChart").getContext("2d");
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ["Event 1", "Event 2", "Event 3"],
                    datasets: [{
                        label: "Attendees",
                        data: [12, 19, 3],
                        backgroundColor: ["#3498db", "#e74c3c", "#2ecc71"]
                    }]
                }
            });
        }
    });
});
