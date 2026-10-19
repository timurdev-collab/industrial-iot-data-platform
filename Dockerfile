FROM python:3.11-slim
WORKDIR /app
COPY pipeline ./pipeline
COPY scripts ./scripts
RUN mkdir -p /app/data
CMD ["sh","-c","python -m pipeline.generate --out data/events.jsonl --count 2000 && python -m pipeline.load --input data/events.jsonl --db data/telemetry.db && python -m pipeline.report --db data/telemetry.db"]
