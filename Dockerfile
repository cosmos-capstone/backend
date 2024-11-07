FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . /app/

# Run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi"]
