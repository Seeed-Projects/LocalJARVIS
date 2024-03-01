# LocalJARVIS Project (🚧WIP🚧)

This project takes off with the Application Engineers at Seeed Studio embarking on a journey to leverage the advanced capabilities of the Jetson Orin AGX. Our mission is to deploy it for the operation of a Local Large Language Model (LLM) embedded with a Langchain agent. The objective is to evolve our office environment into a cutting-edge, GenAI-infused AIoT workspace, further enhanced by the integration of automation with the Home Assistant project. The goal is to establish an open-source framework based on RAG for building a local LLM that interacts with Home Assistant API. This endeavor seeks not only to elevate the workplace atmosphere but also to decrease energy consumption, aligning with Sustainable Development Goals (SDG).

This comprehensive project is divided into several crucial segments, each indispensable for the effective real-world deployment of this groundbreaking upgrade.

Here is the flowchart of the whole system:

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/flowchart.png" width="700" align="center">
</p>

1. Voice Input: Users engage with the system by initiating conversations via ReSpeaker.
2. Voice Processing: The ReSpeaker sends these commands to NVIDIA® Riva software component that recognizes speech (ASR - Automatic Speech Recognition), NVIDIA® Riva is the speech multilingual speech and translation AI software development kit developed by Nvidia, this Nvidia Riva service is running locally on the Nvidia Jetson devices, in this case we are uing a powerfull Orin AGX . After recognizing the speech and Riva turns it into input prompts for further processing.
3. Local Processing or Cloud Processing: The input can be processed locally using a server called Jetson Orin AGX, or it can be sent to the cloud through OpenAI's API for language understanding and response generation(to be noted: We maintain the use of OpenAI API for its significantly better performance and accuracy over the locally-run llama-2-7b models. Nonetheless, our ultimate aim is to transition to a fully local setup. We are confident in our ability to enhance the performance of local LLMs to achieve this objective.)
4. Decision Making:
   * If the input requires controlling tools, it goes to through a LangChain process, which decides if an action needs to be taken (like turning on a light).</br>
    For example:</br>
        User: Hi Javis!</br> 
        Agent: bla bla bla</br>
    
   * If no action is needed, it proceeds to generate a response directly.
5. Home Automation Interaction: If an action is needed, LangChain agent communicates with Home Assistant through Home Assistant API to control and  perform the task on smart appliances (These are the devices being controlled by the system, like lights, thermostats, or any other connected smart home devices, the action will for example be turn on off the lights, control the smart thermostat, set a to-do task, or even orders things from the online shop(amazon, aliexpress) and etc
6. Feedback: The system provides feedback of the states of the executes a control action.
7. Display Information: Display the information via Node-RED, like the current state of home entities (like temperature sensors), time, or weather reports, etc.

## Hardware List:

* [Seeed Studio AGX Orin™](https://www.seeedstudio.com/NVIDIArJetson-AGX-Orintm-64GB-Developer-Kit-p-5641.html)
* [15.6inch Monitor](https://www.seeedstudio.com/15-6-Inch-IPS-Portable-Monitor-p-5757.html)
* [Home Assistant Green](https://www.seeedstudio.com/Home-Assistant-Green-p-5792.html)

## Setup Guide

### NVIDIA® Riva

The instruction on how to setup could found [here](https://wiki.seeedstudio.com/Local_Voice_Chatbot/)

### LocalLLM

The instruction on setup Local LLM and the LangChain agent are listed [here](https://github.com/Seeed-Projects/LocalJARVIS/tree/main/Software/llm)

Here is an example of the LangChain action:

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/agent_example.png" width="300" align="center">
</p>

### Dashboard

<p style="text-align: center;">
    <img src="https://github.com/Seeed-Projects/LocalJARVIS/blob/main/Resource/dashboard.png" width="300" align="center">
</p>

The instruction on how to setup could found [here](https://github.com/Seeed-Projects/LocalJARVIS/tree/main/Software/node-red)

### Home Assistant

the instruction on how to setup could found [here]() --comming soon 🚧

## To-Do/Wish list 🚧

### Project To-Do
- [ ]FIX Project README under construction part
- [ ]Collect Ideas

### Wish List

-- [ ]Implement RAG 

## Contribution 

Join Us in Shaping this LocalJARVIS project! 🌟

Hello, Open Source and Local llm Enthusiasts!

We're excited to invite you to contribute to this project, As we navigate through the journey of building something impactful, your expertise, passion, and creativity can make a significant difference.

Why Contribute to LocalJARVIS?

Learn and Grow: Dive deep into [technology stack, e.g., Local LLM, Nvidia Riva, LangChain, Home Assistant, Python, Node-RED,JavaScript, etc.] and best practices in software development. Whether you're a seasoned developer or just starting, there's always something new to learn.
Community and Collaboration: Join a vibrant community of like-minded individuals. Collaborate, share ideas, and get feedback. It's a great way to network and grow together.
Make an Impact: Your contributions directly help in making [Project Name] better and more useful for everyone. It's an opportunity to contribute to something that you and many others will benefit from.
Recognition: All contributors will be recognized for their efforts. We celebrate contributions of all sizes and acknowledge the hard work of our community members.
How Can You Contribute?

We welcome contributions of all kinds, from code improvements, bug fixes, documentation updates, to feature suggestions and more. Here's how you can get started:

Check Out the Issues: Browse through our [issues tab](https://github.com/Seeed-Projects/LocalJARVIS/issues) to find something that interests you. We tag issues with 'good first issue' for newcomers!
Propose Your Idea: Have an idea or a feature request? Open a new issue and let's discuss how it can fit into the project.
Submit a Pull Request: Ready to get your hands dirty? Fork the repository, make your changes, and submit a pull request. Don't forget to follow our contribution guidelines!
Getting Started

Contribution Guidelines: [link to CONTRIBUTING.md]() -- Comming soon 🚧

Need Help?

We understand that contributing to an open-source project can be daunting for newcomers. We encourage you to reach out if you have any questions or need guidance. Join our [Discord/Community Channel]/ Our team and community members are here to help!

Thank you for considering contributing. Your support is what drives the success of this project. We can't wait to see what we can build together!

Happy Coding! 🍻🍻🍻

The Seeed Studio Application Engineering Team