---
description: Export project data (tasks, reports, metrics) in multiple formats (CSV, JSON, Markdown, Text) for sharing and analysis.
handoffs: []
scripts: {}
---

## User Input

```text
$ARGUMENTS
```

## Outline

The `/goalkit.export` command exports project data in various formats with several subcommands:

### `goalkit export tasks`
Export project tasks in specified format:
- Formats: csv, json, markdown, text
- Use `--format`, `-f` to specify format
- Use `--output`, `-o` to specify output file (prints to stdout if omitted)

### `goalkit export report`
Export project report in specified format:
- Formats: csv, json, markdown, text
- Generates comprehensive summary report
- Use `--output`, `-o` to save to file

### `goalkit export metrics`
Export project metrics in specified format:
- Formats: csv, json, markdown, text
- Reads metrics from `.goalkit/metrics_history.json`
- Use `--output`, `-o` to save to file

### `goalkit export all`
Export complete project data (tasks, report, and metrics):
- Formats: json, markdown
- Combines all project data into a single export
- Use `--output`, `-o` to save to file

### `goalkit export formats`
Show available export formats and their best use cases.

## When to Use

- **Sharing progress**: Export reports for stakeholders
- **Data analysis**: Export tasks/metrics as CSV for spreadsheet analysis
- **Documentation**: Export as Markdown for project documentation
- **Archives**: Export complete project snapshot as JSON
- **Integration**: Feed exported data into other tools
