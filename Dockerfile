FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LLMQ_PROJECT_ROOT=/app

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY config ./config
COPY datasets ./datasets
RUN pip install --no-cache-dir .

EXPOSE 8000
USER 65532:65532
CMD ["uvicorn", "llm_quality_harness.api:app", "--host", "0.0.0.0", "--port", "8000"]

