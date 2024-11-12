/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('search-results');

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();
        if (query.length > 0) {
            fetch(`/live_search/?query=${query}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                    // Add CSRF token if needed
                    // 'X-CSRFToken': csrfToken,
                },
            })
            .then(response => response.json())
            .then(data => {
                // Update UI with search results
                resultsContainer.innerHTML = '';
                data.forEach(item => {
                    const resultItem = document.createElement('div');
                    resultItem.textContent = item.name;
                    resultsContainer.appendChild(resultItem);
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            resultsContainer.innerHTML = '';
        }
    });
});

<!-- MODAL LIVE SEARCH -->



function openModal(inputName) {
    const url = fetchDataBaseUrl + inputName + '/';

    // Clear previous table data
    $('#dataTable').DataTable().clear().destroy();
    $('#modalContent').empty();

    $.ajax({
        url: url,
        method: "GET",
        success: function(response) {
            let data = response.data;

            if (data.length > 0) {
                let headers = Object.keys(data[0]);

                // Create table structure
                let tableHtml = '<table id="dataTable" class="display table table-striped">';
                tableHtml += '<thead><tr>';

                headers.forEach(header => {
                    tableHtml += `<th>${header.charAt(0).toUpperCase() + header.slice(1)}</th>`;
                });
                tableHtml += '</tr></thead><tbody>';

                data.forEach(item => {
                    tableHtml += `<tr onclick="selectRow('${item[headers[0]]}', '${inputName}')">`;
                    headers.forEach(header => {
                        tableHtml += `<td>${item[header]}</td>`;
                    });
                    tableHtml += '</tr>';
                });

                tableHtml += '</tbody></table>';

                $('#modalContent').append(tableHtml);
                $('#dataTable').DataTable();

            } else {
                $('#modalContent').append('<p>No data available</p>');
            }

            // Show the modal
            $('#myModal').modal('show');
        },
        error: function() {
            alert("Error loading data");
        }
    });
}

// Function to handle row selection
function selectRow(value, inputName) {
    document.getElementById(inputName).value = value;
    closeModal();
}

// Function to close the modal
function closeModal() {
    $('#myModal').modal('hide');
}
