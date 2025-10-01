FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /djangoapp

# Copy the content from the local djangoapp directory to the container
COPY . .

# Install the required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run fastapi when the container launches
# CMD ["python", "api/manage.py", "runserver", "0.0.0.0:8000"]