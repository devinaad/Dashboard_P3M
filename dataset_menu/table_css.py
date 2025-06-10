custom_style = """
<style>
    /* Essential text wrapping rules */
    .wrapped-column {
        white-space: normal !important;
        word-wrap: break-word !important;
        word-break: break-word !important;
        overflow-wrap: break-word !important;
    }

    /* Remove nowrap from table */
    table.dataTable.display td.wrapped-column {
        white-space: normal !important;
    }

    /* Other styling */
    .dataTables_wrapper {
        font-family: 'Arial', sans-serif;
    }

    table.dataTable {
        width: 100% !important;
        border-collapse: collapse;
    }

    table.dataTable th {
        background-color: #38519c;
        color: white;
        padding: 10px;
        border: 1px solid #ddd;
        white-space: nowrap; /* Keep headers on single line */
    }

    table.dataTable td {
        padding: 8px;
        border: 1px solid #ddd;
        vertical-align: top;
    }

    /* Set background color for all table rows except the first */
    table.dataTable tbody tr:not(:first-child) {
        background-color: white;
    }

    /* Optional: if you want to give a different color to the first row (not header) */
    table.dataTable tbody tr:first-child {
        background-color: #f5f5f5;
    }

    /* Add horizontal scrolling for the table if needed */
    .dataTables_wrapper .dataTables_scroll {
        clear: both;
    }

    .dataTables_wrapper .dataTables_scrollBody {
        overflow-x: auto;
        overflow-y: auto;
    }

    .dataTables_info, .dataTables_length, .dataTables_filter {
        margin-bottom: 15px;
    }

    .dataTables_paginate .paginate_button {
        padding: 5px 10px;
        margin: 0 2px;
        border: 1px solid #ddd;
        border-radius: 3px;
        cursor: pointer;
    }

    .dataTables_paginate .paginate_button.current {
        background-color: #323b4f;
        color: white !important;
    }
</style>
"""
