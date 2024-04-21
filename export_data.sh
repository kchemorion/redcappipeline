#!/bin/bash

DB_PATH="HOLOA_off_line_FINAL.accdb"

# Get list of tables, excluding temporary tables
tables=$(mdb-tables -1 $DB_PATH | grep -v '^~')

# Export each table to CSV, handling names properly, including headers
for table in $tables; do
    echo "Attempting to export $table..."
    # Temporarily store output to check if the export is successful
    output=$(mdb-export "$DB_PATH" "$table" 2>&1)
    if [[ $? -eq 0 ]]; then
        echo "Exporting $table to CSV with headers..."
        echo "$output" > "${table// /_}.csv"
    else
        echo "Failed to export $table: $output"
    fi
done

echo "Export complete."
