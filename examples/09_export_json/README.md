# Export JSON Example

This example demonstrates how to export log records to JSON format for API integration, data processing, and modern applications.

## What it shows

- Exporting logs to structured JSON format
- JSON structure with metadata and log array
- ISO timestamp formatting
- Pretty-printed, readable JSON output

## How to run

```bash
cd examples/09_export_json
python example.py
```

## JSON structure

The exported JSON includes:
- **metadata**: Export information (timestamp, count, logger name)
- **logs**: Array of log records with full details

## Key benefits

- **API Ready**: Perfect for REST APIs and web services
- **Parseable**: Easy to parse in any programming language
- **Structured**: Clear hierarchy and data types
- **Modern**: Standard format for modern applications

## Use cases

JSON format is perfect for:
- **API Integration**: Send logs to monitoring services
- **Data Processing**: Analyze logs with data tools
- **Web Applications**: Display logs in web interfaces
- **Microservices**: Exchange log data between services

## Next steps

- Learn about [Level Filtering](../11_level_filtering/) for selective exports
- Try [GUI Logging](../10_gui_logging/) for visual log management 