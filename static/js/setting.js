document.getElementById('settingsButton').addEventListener('click', function() {
    // Fetch settings.html content
    fetch('settings.html')
        .then(response => response.text())
        .then(data => {
            // Hide the current main layout content
            document.getElementById('mainLayout').style.display = 'none';
            // Create a new div to insert the settings.html content
            const settingsContainer = document.createElement('div');
            settingsContainer.innerHTML = data;
            // Insert the settings.html content into the main layout
            document.body.appendChild(settingsContainer);
        })
        .catch(error => console.error('Error loading settings.html:', error));
});
