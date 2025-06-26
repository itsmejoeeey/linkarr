FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

# Copy source code
COPY src/linkarr /app/linkarr

# Set default command (can override config file at runtime)
ENTRYPOINT ["python", "-m", "linkarr.main"]
CMD ["/config/config.json"]
