FROM python:3.12-slim-bullseye
 
ENV HOST=0.0.0.0
ENV LISTEN_PORT 8080
EXPOSE 8080

# Set the working directory in the container
WORKDIR /app

# Install any necessary dependencies, including Streamlit
RUN pip install --no-cache-dir langchain-community langchain-openai streamlit python-decouple

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port", "8080"]