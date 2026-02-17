FROM python:3.10-slim-bullseye
 
ENV HOST=0.0.0.0
ENV LISTEN_PORT=8080
EXPOSE 8080

# Set the working directory in the container
WORKDIR /app

# Install any necessary dependencies, including Streamlit
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "8080", "--server.address=0.0.0.0", "--server.baseUrlPath=flight"]