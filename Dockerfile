FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (default for Streamlit, but let Coolify override)
EXPOSE 8501

# Copy start script
COPY start.sh .
RUN chmod +x start.sh

# Use shell script as entrypoint
CMD ["./start.sh"]
