# Level Filtering Example

This example demonstrates how to filter log exports by log level to extract only the logs you need for analysis.

## What it shows

- Filtering stored logs by minimum level
- Counting logs at different levels
- Exporting filtered logs to various formats
- Practical use cases for level filtering

## How to run

```bash
cd examples/11_level_filtering
python example.py
```

## Key features demonstrated

- **Level Statistics**: Count logs at each level
- **Filtered Exports**: Export only logs above a certain level
- **Multiple Formats**: Apply filtering to any export format
- **Practical Filtering**: Real-world scenarios for log filtering

## Common filtering patterns

```python
# Get only errors and critical
errors = logger.get_records(level_filter=Logger.ERROR)

# Export warnings and above
logger.export_log("important.log", "log", level_filter=Logger.WARNING)

# Export only critical issues
logger.export_log("critical.json", "json", level_filter=Logger.CRITICAL)
```

## Use cases

- **Error Analysis**: Export only errors for debugging
- **Production Monitoring**: Focus on warnings and above
- **Debug Cleanup**: Remove debug logs from production exports
- **Alert Systems**: Process only critical and error logs

## Filtering levels

| Filter Level | Includes |
|-------------|----------|
| DEBUG | All logs (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| INFO | INFO, WARNING, ERROR, CRITICAL |
| WARNING | WARNING, ERROR, CRITICAL |
| ERROR | ERROR, CRITICAL |
| CRITICAL | CRITICAL only |

## Next steps

- Try [Memory Management](../12_memory_management/) for handling large log volumes
- Combine with export formats like [JSON](../09_export_json/) or [CSV](../07_export_csv/) 