FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
WORKDIR /app
COPY requirements.txt /app/platform/requirements.txt
RUN pip install --no-cache-dir -r /app/platform/requirements.txt
COPY . /app/platform
EXPOSE 8000
CMD ["uvicorn", "platform.main:app", "--host", "0.0.0.0", "--port", "8000"]
