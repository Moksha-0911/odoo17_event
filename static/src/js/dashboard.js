//
//    document.addEventListener("DOMContentLoaded", function () {
//        var ctx = document.getElementById("eventLineChart").getContext("2d");
//
//        var eventData = {
//            labels: ["January", "February", "March", "April", "May", "June", "July"],  // Replace with dynamic months
//            datasets: [{
//                label: "Total Events",
//                data: [5, 8, 3, 9, 6, 7, 4],  // Replace with dynamic event counts
//                borderColor: "blue",
//                backgroundColor: "rgba(0, 0, 255, 0.2)",
//                borderWidth: 2,
//                fill: true
//            }]
//        };
//
//        new Chart(ctx, {
//            type: "line",
//            data: eventData,
//            options: {
//                responsive: true,
//                maintainAspectRatio: false,
//                scales: {
//                    y: {
//                        beginAtZero: true
//                    }
//                }
//            }
//        });
//    });
document.addEventListener("DOMContentLoaded", function () {
    var chartData = JSON.parse(document.getElementById("chart_data").textContent);

    var ctx1 = document.getElementById("barChart").getContext("2d");
    new Chart(ctx1, {
        type: "bar",
        data: {
            labels: chartData.labels,
            datasets: [{
                label: "Attendees",
                data: chartData.attendees,
                backgroundColor: "rgba(54, 162, 235, 0.5)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1
            }]
        }
    });

    var ctx2 = document.getElementById("pieChart").getContext("2d");
    new Chart(ctx2, {
        type: "pie",
        data: {
            labels: chartData.labels,
            datasets: [{
                data: chartData.attendees,
                backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0", "#9966ff"],
            }]
        }
    });

    var ctx3 = document.getElementById("lineChart").getContext("2d");
    new Chart(ctx3, {
        type: "line",
        data: {
            labels: chartData.labels,
            datasets: [{
                label: "Attendees",
                data: chartData.attendees,
                borderColor: "#ff6384",
                fill: false
            }]
        }
    });
});
