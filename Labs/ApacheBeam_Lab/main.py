from pathlib import Path
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from datetime import datetime
import re


# ----------------------------
# CONFIG
# ----------------------------
inputs_pattern = str(Path('./data/*.logs').resolve())
outputs_prefix = str(Path('./output/log_summary').resolve())
window_duration = 600  # seconds (10-minute windows)


# ----------------------------
# PARSE AIRFLOW LOGS
# ----------------------------
class ParseLogFn(beam.DoFn):
    def process(self, element):
        """
        Example log line:
        [2025-10-28T12:54:24.486+0000] {logging_mixin.py:188} INFO - message text
        """
        pattern = re.compile(
            r'^\[(?P<timestamp>[0-9T:\.\+\-]+)\]\s+\{[^}]+\}\s+(?P<level>[A-Z]+)\s*-\s*(?P<message>.*)$'
        )

        match = pattern.match(element)
        if not match:
            return []

        level = match.group('level')
        time_str = match.group('timestamp')

        try:
            log_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            return []

        yield beam.window.TimestampedValue((level, 1), log_time.timestamp())


# ----------------------------
# FORMAT RESULTS WITH WINDOW INFO
# ----------------------------
class FormatGroupedResultsFn(beam.DoFn):
    def process(self, element, window=beam.DoFn.WindowParam):
        """
        element: ((level), count)
        window: Beam window param, contains start and end times
        """
        level, count = element
        start = window.start.to_utc_datetime()
        end = window.end.to_utc_datetime()
        yield f"Window: {start} - {end} | Level: {level} | Count: {count}"


# ----------------------------
# MAIN PIPELINE
# ----------------------------
options = PipelineOptions(streaming=False)

with beam.Pipeline(options=options) as pipeline:
    (
        pipeline
        | 'Read logs' >> beam.io.ReadFromText(inputs_pattern)
        | 'Parse logs' >> beam.ParDo(ParseLogFn())
        | 'Filter levels' >> beam.Filter(lambda kv: kv[0] in ['INFO', 'WARNING', 'ERROR'])
        | 'Window into 10-min fixed' >> beam.WindowInto(beam.window.FixedWindows(window_duration))
        | 'Count per level per window' >> beam.CombinePerKey(sum)
        | 'Format output' >> beam.ParDo(FormatGroupedResultsFn())
        | 'Write results' >> beam.io.WriteToText(outputs_prefix)
    )

print(f"Check '{outputs_prefix}-*' for per-window log summaries.")
