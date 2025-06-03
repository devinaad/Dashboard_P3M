# Function to calculate appropriate column widths based on column names
def get_column_widths(df):
    column_widths = {}
    
    for col in df.columns:
        # Base width on column name length with some additional padding
        # Short names (< 5 chars): 80px minimum
        # Medium names (5-10 chars): proportional width
        # Long names (> 10 chars): special handling
        col_len = len(str(col))
        
        if col.lower() in ["judul", "title", "description", "deskripsi", "abstrak", "abstract"]:
            # Special handling for known text-heavy columns
            column_widths[col] = "250px"  # Give text-heavy columns more space
        elif col_len < 5:
            column_widths[col] = "80px"   # Minimum width for short column names
        elif col_len < 10:
            column_widths[col] = f"{70 + col_len * 8}px"  # Proportional widths
        else:
            column_widths[col] = f"{150}px"  # Cap for very long column names
            
    return column_widths

# Generate columnDefs for DataTables based on calculated widths
def generate_column_defs(df):
    column_widths = get_column_widths(df)
    column_defs = []
    
    for i, col in enumerate(df.columns):
        column_def = {
            "targets": i,
            "width": column_widths[col]
        }
        
        # Add text wrapping only for certain columns
        if col.lower() in ["judul", "title", "description", "deskripsi", "abstrak", "abstract"]:
            column_def["className"] = "wrapped-column"
        
        column_defs.append(column_def)
    
    return column_defs

# Updated DataTables options with dynamic column definitions
def get_datatable_options(df):
    return {
        "pageLength": 10,
        "searching": True,
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "ordering": True,
        "autoWidth": False,  # Disable auto width calculation
        "scrollX": True,     # Enable horizontal scrolling if needed
        "columnDefs": generate_column_defs(df),
        "initComplete": """
            function() {
                // Additional customization after table initialization
                $('.wrapped-column').css({
                    'white-space': 'normal',
                    'word-break': 'break-word'
                });
            }
        """
    }

