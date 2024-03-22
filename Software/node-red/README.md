# Magic Mirror Dashboard Setup with Node-RED 🪄🖥️

This guide leads you through creating a dynamic Magic Mirror Dashboard using Node-RED on your Jetson device. It details steps for setting up the dashboard's main interface and integrating advanced features with a Grove Vision AI V2 Camera.

## What's Inside 📦

- **`main_flow.json`**: Acts as the foundation of the Magic Mirror Dashboard setup. This file outlines the primary features and appearance of the dashboard.

- **`grove_vision_ai_flows.json`**: Augments your dashboard by incorporating an overlay for the Grove Vision AI V2 Camera, facilitating the counting of people and monitoring of area zones.

### Dashboard Preview 🖼️

- **Magic Mirror Dashboard**: A sleek and interactive interface for your mirror.
- **Grove Vision AI Overlay**: Introduces intelligent vision capabilities to your dashboard.

---

## Getting Started on Jetson 🚀

Follow these instructions to install Node-RED and configure the necessary environment for your Magic Mirror Dashboard.

### 1. Install Node-RED 🧰

**Create a dedicated folder for Node-RED data:**

```bash
mkdir /home/nvidia/node_red_data/
```

**Adjust the folder's ownership:**

```bash
sudo chown 1000 /home/nvidia/node_red_data/
```

**Launch Node-RED using Docker, naming the container "localJarvis-dashboard":**

```bash
docker run --restart always -d -p 1880:1880 -v /home/nvidia/node_red_data:/data --name localJarvis-dashboard nodered/node-red:3.1
```

### 2. Host Static Data 📂

**Establish a directory for static data:**

```bash
mkdir node-red-static
```

**Modify `settings.js` to utilize the new static data folder:**

```bash
sed -i "s|//httpStatic: '/home/nol/node-red-static/'|httpStatic: '/data/node-red-static/'|g" settings.js
```

### 3. Install Node-RED Package Dependency 📌

**Access the Node-RED editor by navigating to your Jetson's IP address with port 1880.**

To install Node-RED dependencies, enter the manage palette settings panel:

<p align="center">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/import_flow.png" width="300">
</p>

Then, select "install":

<p align="center">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/select_install.png" width="300">
</p>

**In the search bar, install the following packages:**

- node-red-dashboard
  <p align="center">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/dashboard_nodes.png" style="width: 20%;height: 20%;">
</p>
- node-red-contrib-home-assistant-websocket
    <p align="center">
        <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/home_assistant_ws.png" style="width: 20%;height: 20%;">
    </p>

### 4. Import Node-RED Flow 🔄

To import the flow, please follow the steps shown below:

<p align="center">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/import_flow.png" width="300">
</p>

<p align="center">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/import_local_flow_file.png" width="300">
</p>

<p align="center">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/node_red_flows.png" width="300">
</p>

Finally, click "Deploy" to apply your changes.

<p align="center">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/deploy_flow.png" width="300">
</p>

### 5. Dashboard Settings (Work in Progress) 🔧

- **Home Assistant Server address**: Specify your Home Assistant server address; for example: 192.168.100.100:8123
- **MQTT server address and topics**: Provide your MQTT broker address; for example: 192.168.100.100:1883

**MQTT Topics:**

- `/human` "This is the TTS from human user voice input"
- `/seeebot` "This is the AI response"
- `/wakeup` "This signals the wakeup word."

---

To access your dashboard, open a web browser and navigate to the IP address of your Jetson device, appending port 1880 followed by "/ui".

The complete URL will appear as follows: "ip-address:1880/ui". For instance, in my scenario, it's "192.168.100.100:1880/ui".

<p align="center">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/dashboard.png" width="300">
</p>

Congratulations! 🎉 You are now ready to delve into and personalize your Magic Mirror Dashboard. Don't hesitate to try out different Node-RED flows to introduce new functionalities or refine the current setup. Enjoy your creative journey!