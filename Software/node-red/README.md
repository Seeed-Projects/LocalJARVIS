# Magic Mirror Dashboard Setup with Node-RED 🪄🖥️

This guide walks you through the process of creating a dynamic Magic Mirror Dashboard using Node-RED on your Jetson device. It includes steps for setting up the dashboard's main interface and integrating advanced features using a Grove Vision AI V2 Camera.

## What's Inside 📦

- **`main_flow.json`**: The backbone of the Magic Mirror Dashboard setup. This file configures the dashboard's main features and appearance.

- **`grove_vision_ai_flows.json`**: Enhances your dashboard by adding an overlay for the Grove Vision AI V2 Camera, enabling people and area zone counting functionalities.

### Dashboard Preview 🖼️

- **Magic Mirror Dashboard**: A sleek and interactive interface for your mirror.
- **Grove Vision AI Overlay**: Adds smart vision capabilities to your dashboard.

---

## Getting Started on Jetson 🚀

Follow these steps to install Node-RED and set up the necessary environment for your Magic Mirror Dashboard.

### 1. Install Node-RED 🧰

Create a dedicated folder for Node-RED data:

```bash
mkdir /home/nvidia/node_red_data/
```

Adjust the folder's ownership:

```bash
sudo chown 1000 /home/nvidia/node_red_data/
```

Deploy Node-RED using Docker with the container named "localJarvis-dashboard":

```bash
docker run --restart always -d -p 1880:1880 -v /home/nvidia/node_red_data:/data --name localJarvis-dashboard nodered/node-red:3.1
```

### 2. Host Static Data 📂

Create a directory for static data:

```bash
mkdir node-red-static
```

Configure `settings.js` to use the new static data folder:

```bash
sed -i "s|//httpStatic: '/home/nol/node-red-static/'|httpStatic: '/home/nvidia/node_red_data/node-red-static/'|g" settings.js
```

### 3. Install Node-RED Package Dependency 

Open the Node-RED editor with the ip address of your Jetson with port 1880 

To Install Node-RED Dependency, you will need to open the mange palette setting panel:

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/import_flow.png" width="300" align="center">
</p>

Then select install:

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/select_install.png" width="300" align="center">
</p>

In the search bar please search and install the following packages:

* node-red-dashboard
* node-red-contrib-home-assistant-websocket

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/dashboard_nodes.png" width="300" align="center">
</p>

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/home_assistant_ws.png" width="300" align="center">
</p>

### 4. Import Node-RED Flow

To import the flow please follow the steps shown in the image below:

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/import_flow.png" width="300" align="center">
</p>

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/import_local_flow_file.png" width="300" align="center">
</p>

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/node_red_flows.png" width="300" align="center">
</p>


Then Clcik Deploy to Deploy

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/deploy_flow.png" width="300" align="center">
</p>



5. Dashboard settings WIP:

The Home Assistant Server address: Your Home Assistant server address in my case: 192.168.100.100:8123

The Mqtt server address and topics: Your Mqtt broker address in my case: 192.168.100.100:1883

MQTT Topics:

/human "This is the TTS from human user voice input"
/seeebot "This is the AI response"
/wakeup "This is the wakeup word"

---

Open your web browser and type in ip address of your Jetson and followed by the port 1880 and then add "/ui"

the complete url should look like: "ip-address:1880/ui" eg in my case "192.168.100.100:1880/ui"

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/dashboard.png" width="300" align="center">
</p>



Congratulations! 🎉 You're all set to explore and customize your Magic Mirror Dashboard. Feel free to experiment with different Node-RED flows to add new features or tweak the existing setup. Happy tinkering!



