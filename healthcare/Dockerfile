FROM python:3.10-slim-bullseye
 
ENV HOST=0.0.0.0
ENV LISTEN_PORT=8080
EXPOSE 8080

# Set the working directory in the container
WORKDIR /app

# Install any necessary dependencies, including Streamlit
RUN apt-get update && apt-get install -y gcc build-essential
RUN pip install --no-cache-dir streamlit python-decouple frontend tools requests pymupdf

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run the Streamlit app
WORKDIR /app/src
CMD ["streamlit", "run", "main.py", "--server.port", "8080"]