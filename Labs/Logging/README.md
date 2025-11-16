# Logging Lab

## Overview

This lab demonstrates a **logging system** with:

* Custom logging configuration via YAML
* Decorators for function-level logging
* An end-to-end ETL-style workflow (API ingestion → transform → validation → save)
* Error handling and debug tracing

---

## Structure

```
logging-lab/
│
├── app.py               # Main application with decorated pipeline functions
├── logger.py            # YAML + dictConfig logging setup
├── utils.py             # Custom decorator for function-level logging
├── config.yaml          # Logging configuration (console/file handlers)
├── data/                # Output data directory (created automatically)
│   └── processed.json
└── logs/                # Log output directory (auto-created)
    ├── stream_rotating.log
```

---

# Key features

## **1. Dual Logging Output (Console + Files)**
- **Console Handler**
  - Level: INFO+
  - Format: `LEVEL: message`
  - Stream: `sys.stdout`
- **File Handlers**
  - `stream_logging.log` → DEBUG+ (detailed)
  - Format:
    ```
    timestamp | level | logger | file:line | message
    ```
- Logs are streamed simultaneously to console and file outputs.

---

## **2. YAML-Based Logging Configuration**
- Centralized configuration in `config.yaml`.
- Defines all formatters, handlers, log levels, and logger hierarchy.
- Handler-specific log levels allow independent verbosity control.

---

## **3. Decorator-Based Function Tracing**
- `@log_function(logger)` adds:
  - Function entry logs (DEBUG)
  - Function exit logs (DEBUG)
  - Exception logs with full traceback (ERROR)

---

## **4. ETL Pipeline Instrumentation**
Each pipeline stage logs:
- API fetch attempts, retries, failures (INFO / WARNING / ERROR)
- Transformation steps (DEBUG)
- Validation filtering (DEBUG)
- Output save confirmation (INFO)
- End-to-end pipeline execution state

---

## **5. Structured Log Formats**
**Console (simple format):**
INFO: Fetching data...
ERROR: Division by zero

**File logs (detailed format):**

2025-01-01 12:00:00 | DEBUG | appLogger | app.py:42 | Entering transform_data()

2025-01-01 12:00:01 | ERROR | appLogger | app.py:87 | Error in divide: division by zero


---

## **6. Streaming & Real-Time Log Behavior**
- Console logs stream directly to stdout in real time.
- File handlers write immediately and roatate to new file once reached file size of 5MB.

---
