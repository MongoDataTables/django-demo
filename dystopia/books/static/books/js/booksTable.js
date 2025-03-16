$(function () {
    // Check if Editor is available
    var editorAvailable = typeof $.fn.dataTable.Editor !== 'undefined';
    var editor;
    
    // Only initialize Editor if it's available
    if (editorAvailable) {
        console.log('DataTables Editor is available - initializing Editor functionality');
        
        // Log form submission data
        $(document).on('click', '.DTE_Form_Buttons button', function() {
            // This will run when any form button is clicked
            console.log('Editor form data:', editor.get());
        });

        // Initialize Editor
        editor = new $.fn.dataTable.Editor({
            ajax: function(method, url, data, success, error) {
                // Prepare the URL based on the action
                var action = data.action;
                var ajaxUrl = '/editor/books';
                var ids = [];

                // Process dates before sending to server
                if (action === 'create' || action === 'edit') {
                    // Loop through data objects
                    $.each(data.data, function(key, values) {
                        // Format the date if it exists and isn't already formatted
                        if (values['PublisherInfo.Date'] && values['PublisherInfo.Date'].includes('T')) {
                            // Convert ISO format to YYYY-MM-DD
                            values['PublisherInfo.Date'] = values['PublisherInfo.Date'].split('T')[0];
                        }
                    });
                }

                if (action === 'remove') {
                    // For remove, extract IDs from the data.id array
                    if (data.id && data.id.length > 0) {
                        ids = data.id;
                        console.log("Remove IDs:", ids);
                    } else if (data.data) {
                        // Alternative way to get IDs from selected rows
                        for (var id in data.data) {
                            if (data.data.hasOwnProperty(id)) {
                                ids.push(id);
                            }
                        }
                        console.log("Remove IDs from data:", ids);
                    }

                    if (ids.length > 0) {
                        ajaxUrl += '?id=' + ids.join(',');
                    } else {
                        console.error("No IDs found for remove operation");
                    }
                } else if (action === 'edit') {
                    // For edit, extract IDs from the data.data object keys
                    for (var id in data.data) {
                        if (data.data.hasOwnProperty(id)) {
                            ids.push(id);
                        }
                    }
                    if (ids.length > 0) {
                        ajaxUrl += '?id=' + ids.join(',');
                    }
                }

                // Log what we're sending (for debugging)
                console.log('Editor ' + action + ' request:');
                console.log('URL: ' + ajaxUrl);
                console.log('Data:', data);

                // Make the AJAX request
                $.ajax({
                    url: ajaxUrl,
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function(json) {
                        console.log('Success response:', json);
                        success(json);

                        // Reload the table to show the updated data
                        table.ajax.reload();
                    },
                    error: function(xhr, status, err) {
                        console.error('Error response:', xhr.responseText);
                        error(xhr, status, err);
                    }
                });
            },
            table: '#novels_table',
            fields: [
                {
                    label: "Title",
                    name: "Title",
                    type: "text"
                },
                {
                    label: "Author",
                    name: "Author",
                    type: "text"
                },
                {
                    label: "Publication Date",
                    name: "PublisherInfo.Date", // Use correct field path
                    type: "datetime", // Use datetime type with specific formatting
                    format: "YYYY-MM-DD",
                    attr: {
                        placeholder: "YYYY-MM-DD"
                    }
                },
                {
                    label: "Pages",
                    name: "Pages",
                    type: "text",
                    attr: {
                        type: "number"
                    }
                },
                {
                    label: "Themes",
                    name: "Themes",
                    type: "select",
                    multiple: true,
                    options: [
                        "Environmental collapse", "Surveillance state", "Artificial intelligence takeover",
                        "Post-apocalyptic survival", "Totalitarian government", "Corporate control",
                        "Biological warfare aftermath", "Digital consciousness", "Class warfare",
                        "Genetic engineering", "Mind control", "Resource depletion", "Technological dependence",
                        "Social media dystopia", "Reality manipulation", "Memory erasure", "Pandemic aftermath",
                        "Climate disaster", "Robotic revolution", "Virtual reality imprisonment"
                    ]
                },
                {
                    label: "Rating",
                    name: "Rating",
                    type: "select",
                    options: [
                        { label: "★★½ (2.5)", value: "2.5" },  // use strings otherwise
                        { label: "★★★ (3.0)", value: "3.0" },
                        { label: "★★★½ (3.5)", value: "3.5" },
                        { label: "★★★★ (4.0)", value: "4.0" },
                        { label: "★★★★½ (4.5)", value: "4.5" },
                        { label: "★★★★★ (5.0)", value: "5.0" }
                    ]
                },
                {
                    label: "Description",
                    name: "Description",
                    type: "textarea"
                }
            ]
        });

        // Handle edit form initialization to format dates
        editor.on('initEdit', function(e, node, data) {
            // Process the date field after the form is initialized
            if (data && data.PublisherInfo && data.PublisherInfo.Date) {
                var dateVal = data.PublisherInfo.Date;

                // Format the date if it's an ISO string or other format
                if (typeof dateVal === 'string') {
                    // Try to parse the date and format it
                    var date = new Date(dateVal);
                    var formattedDate = date.toISOString().split('T')[0]; // YYYY-MM-DD format

                    // Update the field value
                    editor.field('PublisherInfo.Date').val(formattedDate);

                    console.log('Formatted date field to:', formattedDate);
                }
            }
        });

        // Also handle preSubmit to ensure we have clean dates
        editor.on('preSubmit', function(e, data, action) {
            // Make sure dates are properly formatted before submission
            if (data.data) {
                Object.keys(data.data).forEach(function(id) {
                    var rowData = data.data[id];
                    if (rowData['PublisherInfo.Date']) {
                        // Ensure date is in YYYY-MM-DD format
                        if (rowData['PublisherInfo.Date'].includes('T')) {
                            rowData['PublisherInfo.Date'] = rowData['PublisherInfo.Date'].split('T')[0];
                        }
                    }
                });
            }
        });
    } else {
        console.log('DataTables Editor not available - using read-only mode');
    }

    // Initialize DataTable with configuration based on Editor availability
    var tableConfig = {
        dom: 'Bfrtip',
        serverSide: true,
        processing: true,
        pageLength: 10,
        select: true,
        rowId: 'DT_RowId',
        buttons: editorAvailable ? [
            { extend: 'create', editor: editor },
            { extend: 'edit', editor: editor },
            { extend: 'remove', editor: editor }
        ] : [
            'copy', 'excel', 'pdf', 'print'
        ],
        ajax: {
            url: '/datatables/books',
            type: 'POST',
            contentType: 'application/json',
            data: function (d) {
                return JSON.stringify(d);
            }
        },
        columns: [
            { data: 'Title' },
            { data: 'Author' },
            {
                data: 'PublisherInfo.Date',
                className: 'dt-center',
                render: function(data) {
                    if (!data) return '';

                    try {
                        var date = new Date(data);
                        return date.toLocaleDateString('en-US', {
                            year: 'numeric',
                            day: 'numeric',
                            month: 'long'
                        });
                    } catch (e) {
                        return data;
                    }
                }
            },
            {
                data: 'Themes',
                render: function(data) {
                    if (!data) return '';
                    return Array.isArray(data) ? data.join(', ') : data;
                }
            },
            { data: 'Pages' },
            { data: 'Rating' },
            { 
                data: 'Description',
                visible: false
            }
        ]
    };

    // Set up the table with the configuration
    var table = $('#novels_table').DataTable(tableConfig);
    
    // Add event listeners for editor if available
    if (editorAvailable) {
        editor
            .on('submitSuccess', function() {
                // Force table reload after successful edit or delete
                table.ajax.reload();
            })
            .on('submitComplete', function() {
                // Another way to ensure table data is refreshed
                table.ajax.reload();
            })

            //DEBUG
            .on('postSubmit', function(e, json, data, action) {
                console.log('Editor postSubmit event');
                console.log('Response from server:', JSON.stringify(json, null, 2));
            })
            .on('preSubmit', function(e, data, action) {
                console.log('Editor preSubmit event');
                console.log('Action:', action);
                console.log('Data being submitted:', JSON.stringify(data, null, 2));

                // Specifically examine rating values
                if (data.data) {
                    Object.keys(data.data).forEach(function(key) {
                        if (data.data[key].Rating !== undefined) {
                            console.log('Rating value:', data.data[key].Rating);
                            console.log('Rating type:', typeof data.data[key].Rating);
                        }
                    });
                }
            });
    } else {
        // Add a note at the bottom of the table about Editor functionality
        $('#novels_table').after(
            '<div class="alert alert-info mt-3">' +
            '<strong>Note:</strong> Editing functionality is currently disabled in this demo. ' +
            'To enable editing, download Editor and uncomment the Editor imports in index.html.' +
            '</div>'
        );
    }
});