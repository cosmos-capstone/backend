FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project files
COPY . /app/

# Run the Django development server
CMD ["gunicorn", "mysite.wsgi"]