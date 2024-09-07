let DataTableManager = (() => {
    let initializeDataTables = () => {
        // Loop through each table with the 'datatable' class and apply DataTables
        $('.datatable').each(function() {
            if ($.fn.DataTable.isDataTable($(this))) {
                $(this).DataTable().destroy();
            }

            $(this).DataTable({
                "paging": true,     // Enable pagination
                "searching": false,  // Enable search/filter
                "info": true,       // Show table information
                "ordering": true,   // Enable column ordering
                "pageLength": 10,    // Set the number of rows per page
                "lengthMenu": [5, 10, 25, 50] // Optional: Change pagination size options
            });
        });
    };

    return {
        init: () => {
            initializeDataTables();
        }
    };
})();
