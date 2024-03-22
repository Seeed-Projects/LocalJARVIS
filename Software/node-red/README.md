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

---

Congratulations! 🎉 You're all set to explore and customize your Magic Mirror Dashboard. Feel free to experiment with different Node-RED flows to add new features or tweak the existing setup. Happy tinkering!



