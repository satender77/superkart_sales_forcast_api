FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the backend directory to /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the port
EXPOSE 7860

# Define the command to start Gunicorn
# We bind to 0.0.0.0 to allow external connections from the frontend container
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_sales_forcast_api"]
