# Gunakan image Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy semua file ke container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port yang sama dengan app.py
EXPOSE 8080

# Jalankan aplikasi
CMD ["python", "app.py"]