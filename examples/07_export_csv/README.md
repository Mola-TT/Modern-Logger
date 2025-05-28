# Export CSV Example

This example demonstrates how to export log records to CSV format for analysis in Excel, Google Sheets, or other spreadsheet applications.

## What it shows

- Exporting logs to CSV format with headers
- CSV structure with all log record fields
- Filtering exports by log level
- Excel-compatible CSV format

## How to run

```bash
cd examples/07_export_csv
python example.py
```

## Expected output

```
📊 Export CSV Example
==============================

📝 Generating sample logs...
[2025-05-28 15:12:30] [INFO]     User login: admin
[2025-05-28 15:12:30] [WARNING]  Failed login attempt: user123
[2025-05-28 15:12:30] [ERROR]    Database connection timeout
[2025-05-28 15:12:30] [CRITICAL] System overload detected
[2025-05-28 15:12:30] [INFO]     User logout: admin

💾 Exporting to CSV format...
   ✅ CSV export: Success
   🚨 Errors CSV: Success

📖 CSV file contents:
   1: Timestamp,Level,Level_Name,Logger_Name,Message
   2: 2025-05-28T15:12:30.123456,20,INFO,MultiLogger,User login: admin
   3: 2025-05-28T15:12:30.234567,30,WARNING,MultiLogger,Failed login attempt: user123
   4: 2025-05-28T15:12:30.345678,40,ERROR,MultiLogger,Database connection timeout
   5: 2025-05-28T15:12:30.456789,50,CRITICAL,MultiLogger,System overload detected
   6: 2025-05-28T15:12:30.567890,20,INFO,MultiLogger,User logout: admin

💡 Tip: Open the CSV file in Excel or any spreadsheet application!
✅ CSV export example completed!
```

## Files created

- `logs_export.csv` - All logs in CSV format
- `errors_only.csv` - Only ERROR and CRITICAL logs

## CSV structure

The CSV format includes these columns:
- **Timestamp**: ISO format timestamp
- **Level**: Numeric log level (10, 20, 30, 40, 50)
- **Level_Name**: Text log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Logger_Name**: Name of the logger that created the record
- **Message**: The actual log message

## Key benefits

- **Spreadsheet Compatible**: Opens directly in Excel, Google Sheets, etc.
- **Sortable**: Easy to sort by timestamp, level, or message
- **Filterable**: Use spreadsheet filters to find specific records
- **Analyzable**: Perfect for creating charts and statistics

## Analysis examples

Once opened in a spreadsheet, you can:
- Sort by timestamp to see chronological order
- Filter by Level_Name to see only errors
- Create charts showing log level distribution
- Use formulas to count errors per time period

## Next steps

- Try [JSON Export](../09_export_json/) for API integration
- Explore [XML Export](../08_export_xml/) for structured data
- Learn about [Level Filtering](../11_level_filtering/) for advanced filtering 