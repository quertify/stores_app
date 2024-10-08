FROM python:3.12-slim

# Set environment variables
ENV FLASK_APP=run.py

# Set to 0 or comment for production
ENV FLASK_DEBUG=1  


# Set the working directory
WORKDIR /stores_app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run Unit Tests
RUN pytest --maxfail=1 --disable-warnings -q

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
