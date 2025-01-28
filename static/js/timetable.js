document.addEventListener('DOMContentLoaded', function() {
  const subjects = [
      "Mathematics", "Science", "History", "Geography", "English", "Physics", "Chemistry", "Biology"
  ];
  const timings = [
      "08:00 AM - 09:00 AM", "09:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", 
      "11:00 AM - 12:00 PM", "12:00 PM - 01:00 PM", "01:00 PM - 02:00 PM", 
      "02:00 PM - 03:00 PM", "03:00 PM - 04:00 PM"
  ];
  const rooms = ["Room 101", "Room 102", "Room 103", "Room 104"];
  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

  function populateSelect(elementId, options) {
      const select = document.getElementById(elementId);
      select.innerHTML = options.map(option => `<option value="${option}">${option}</option>`).join('');
  }

  populateSelect('subjectSelect', subjects);
  populateSelect('timingSelect', timings);
  populateSelect('roomSelect', rooms);
  populateSelect('daySelect', days);

  document.getElementById('seeDetailsButton').addEventListener('click', function () {
      const subjectSelect = document.getElementById('subjectSelect').value;
      const timingSelect = document.getElementById('timingSelect').value;
      const roomSelect = document.getElementById('roomSelect').value;
      const daySelect = document.getElementById('daySelect').value;

      const tableBody = document.getElementById('dataEntryTableBody');
      tableBody.innerHTML = `
          <tr>
              <td>${subjectSelect}</td>
              <td>${timingSelect}</td>
              <td>${roomSelect}</td>
              <td>${daySelect}</td>
          </tr>
      `;

      $('#dataEntryModal').modal('show');
  });
});

const button = document.getElementById('seeDetailsButton');
button.addEventListener('mouseover', function() {
  button.style.backgroundColor = 'rgb(0,102,204)';
  button.style.color = 'white';
});
button.addEventListener('mouseout', function() {
  button.style.backgroundColor = '';
  button.style.color = '';
});
