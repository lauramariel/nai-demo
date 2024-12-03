# Nutanix AI Demo Application

This is a demo application for Nutanix AI. Follow the instructions below to set up and run the application on your system.

## Running on macOS

### Requirements

- Install Rancher Desktop. Follow the installation guide [here](https://docs.rancherdesktop.io/getting-started/installation/).

### Instructions

1. Open your terminal.
2. Clone the repository:
   ```bash
   git clone https://github.com/halsayed/nai-demo.git
   ```
3. Navigate to the project directory:
   ```bash
   cd nai-demo
   ```
4. Build the Docker containers:
   ```bash
   docker compose build
   ```
5. Start the application:
   ```bash
   docker compose up
   ```
6. To stop the application, press `Control + C`.

## Running on Linux (Ubuntu)

### Requirements

- Install Docker using the following commands:
  ```bash
  sudo apt -y install apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt update
  sudo apt -y install docker-ce
  sudo usermod -aG docker ${USER}
  ```

### Instructions

- Follow the same instructions as for macOS to run the application.

## Running on Windows

**Note:** Instructions for Windows are a work in progress. Please check back later for updates.
