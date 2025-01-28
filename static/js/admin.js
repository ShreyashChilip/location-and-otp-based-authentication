// Graph
var ctx = document.getElementById("myChart");

var myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ],
    datasets: [
      {
        data: [30,45,50,70,65,60,30],
        lineTension: 0,
        backgroundColor: "transparent",
        borderColor: "#007bff",
        borderWidth: 4,
        pointBackgroundColor: "#007bff",
      },
    ],
  },
  options: {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: false,
            min: 20,
            max: 70,
          },
        },
      ],
    },
    legend: {
      display: false,
    },
  },
});

// timetable.js

document.addEventListener('DOMContentLoaded', function() {
  const timetableData = [
      { day: "Monday", subjects: "Mathematics", totalStudents: 30, attendance: 28, percentage: 93.33 },
      { day: "Tuesday", subjects: "Science", totalStudents: 30, attendance: 27, percentage: 90.00 },
      { day: "Wednesday", subjects: "History", totalStudents: 30, attendance: 29, percentage: 96.67 },
      { day: "Thursday", subjects: "Geography", totalStudents: 30, attendance: 26, percentage: 86.67 },
      { day: "Friday", subjects: "English", totalStudents: 30, attendance: 30, percentage: 100.00 },
      { day: "Saturday", subjects: "Physics", totalStudents: 30, attendance: 25, percentage: 83.33 }
  ];

  const tbody = document.querySelector('table tbody');

  timetableData.forEach(data => {
      const row = document.createElement('tr');

      row.innerHTML = `
          <th scope="row">${data.day}</th>
          <td>${data.subjects}</td>
          <td>${data.totalStudents}</td>
          <td>${data.attendance}</td>
          <td>${data.percentage.toFixed(2)}</td>
      `;

      tbody.appendChild(row);
  });
});

