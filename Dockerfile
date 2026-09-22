FROM python:3.12-slim

WORKDIR /app

# Dependencies zuerst: Docker cached diesen Layer, solange sich
# requirements.txt nicht aendert. Code-Aenderungen rebuilden dann nur den
# letzten Layer statt alles neu zu installieren.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY pyproject.toml .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
