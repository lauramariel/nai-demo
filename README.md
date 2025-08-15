Nutanix AI Demo Application

This is a demo application for Nutanix AI. Follow the instructions below to set up and run the application on your system.

## Running locally on macOS

### macOS Requirements

- Install Rancher Desktop. Follow the installation guide [here](https://docs.rancherdesktop.io/getting-started/installation/).

### macOS Instructions

1. Open your terminal.
2. Clone the repository:
   ```bash
   git clone https://github.com/lauramariel/nai-demo.git
   ```
3. Navigate to the project directory:
   ```bash
   cd nai-demo
   ```
4. (Optional) Update sample.env with your API key. Copy this file to `.env`

   ```bash
   cp sample.env .env
   ```

5. Build the Docker containers and start the application:
   ```bash
   bash start.sh local
   ```

6. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```
   This will open the demo application interface.
7.  To stop the application, press `Control + C`.

## Running on Linux

### Linux Requirements (Ubuntu)

- Install Docker using the following commands:
  ```bash
  sudo apt -y install apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt update
  sudo apt -y install docker-ce
  sudo usermod -aG docker ${USER}
  ```

### Linux Requirements (Rocky)
```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### Linux Instructions

- Follow the [macOS instructions](#macos-instructions) to run the application.

## Running on Windows

### Windows Requirements

- Install Windows Subsystem for Linux (WSL). Follow the installation guide [here](https://learn.microsoft.com/en-us/windows/wsl/install).

### Windows Instructions

1.	Install WSL from an admin command/Powershell prompt by running wsl –install
2.	Once installed and rebooted, open WSL and follow the instructions for [installing Docker on Linux.](#linux-requirements)
3.	Exit WSL to allow the group change to take effect. 
4.	Open WSL and continue with the [macOS instructions](#macos-instructions) to run the application.

## Running on a VM

To run this on a VM with SSL and certificates:

1. Update nginx.conf with your hostname
2. Update .env with your path to certificates
3. Run the start script

   ```bash
   bash start.sh prod
   ```

## Stop the application

To stop the application run

```bash
bash stop.sh [local|prod]
```
