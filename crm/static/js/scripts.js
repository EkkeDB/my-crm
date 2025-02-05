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

    $.ajax({
        url: url,
        method: "GET",
        success: function(response) {
            const data = response.data;
            console.log("Data received:", data);  // Check data structure

            if (data && data.length > 0) {
                let tableHtml = '<table width=100% id="dataTable" class="display table table-striped">';
                tableHtml += '<thead><tr><th>ID</th><th>Name</th></tr></thead><tbody>';

                data.forEach(item => {
                    let id, name;

                    // Dynamically assign id and name based on inputName
                    switch(inputName) {
                        case 'sociedad':
                            id = item['id_sociedad'];
                            name = item['sociedad_name'];
                            break;
                        case 'counterparty':
                            id = item['id_counterparty'];
                            name = item['counterparty_name'];
                            break;
                        case 'commodity':
                            id = item['id_commodity'];
                            name = item['commodity_name_short'];
                            break;
                        case 'commodity_group':
                            id = item['id_commodity_group'];
                            name = item['commodity_group_name'];
                            break;
                        case 'commodity_type':
                            id = item['id_commodity_type'];
                            name = item['commodity_type_name'];
                            break;
                        case 'trader':
                            id = item['id_trader'];
                            name = item['trader_name'];
                            break;
                        case 'broker':
                            id = item['id_broker'];
                            name = item['broker_name'];
                            break;
                        case 'currency':
                            id = item['id_currency'];
                            name = item['currency_name'];
                            break;
                        case 'icoterm':
                            id = item['id_icoterm'];
                            name = item['icoterm_name'];
                            break;
                        case 'trade_operation_type':
                            id = item['id_trade_operation_type'];
                            name = item['trade_operation_type_name'];
                            break;
                        case 'delivery_format':
                                id = item['id_delivery_format'];
                                name = item['delivery_format_name'];
                                break;
                        case 'additive':
                                    id = item['id_additive'];
                                    name = item['additive_name'];
                                    break;
                        case 'contract':
                            id = item['id_contract'];
                            name = item['contract_name'];
                            break;
                        default:
                            id = null;
                            name = null;
                    }

                    tableHtml += `<tr data-id="${id}" data-name="${name}">`;
                    tableHtml += `<td>${id}</td><td>${name}</td></tr>`;
                });

                tableHtml += '</tbody></table>';
                $('#modalContent').html(tableHtml);

                // Attach event listener to the table (delegation)
                $('#dataTable tbody').on('click', 'tr', function() {
                    const id = $(this).data('id');
                    const name = $(this).data('name');
                    selectRow(id, name, inputName);
                });

                $('#dataTable').DataTable();  // Initialize DataTable
            } else {
                $('#modalContent').html('<p>No data available</p>');
            }

            $('#myModal').modal('show');
        },
        error: function(xhr, status, error) {
            console.error("Error fetching data:", error);
        }
    });
}

function selectRow(id, name, inputName) {
    // Mapping of input names to field IDs
    const fieldMapping = {
        'sociedad': { id: 'id_sociedad', name: 'sociedad_name' },
        'counterparty': { id: 'id_counterparty', name: 'counterparty_name' },
        'commodity': { id: 'id_commodity', name: 'commodity_name_short' },
        'commodity_group': { id: 'id_commodity_group', name: 'commodity_group_name' },
        'commodity_type': { id: 'id_commodity_type', name: 'commodity_type_name' },
        'trader': { id: 'id_trader', name: 'trader_name' },
        'broker': { id: 'id_broker', name: 'broker_name' },
        'currency': { id: 'id_currency', name: 'currency_name' },
        'icoterm': { id: 'id_icoterm', name: 'icoterm_name' },
        'trade_operation_type': { id: 'id_trade_operation_type', name: 'trade_operation_type_name' },
        'delivery_format': { id: 'id_delivery_format', name: 'delivery_format_name' },
        'additive': { id: 'id_additive', name: 'additive_name' },
        'contract': { id: 'id_contract', name: 'contract_name' }
    };

    // Get the field IDs based on the inputName
    const fields = fieldMapping[inputName];

    // If fields exist for the given inputName, update the form fields
    if (fields) {
        document.getElementById(fields.id).value = id;
        document.getElementById(fields.name).value = name;
    }

    // Close the modal
    $('#myModal').modal('hide');
}
