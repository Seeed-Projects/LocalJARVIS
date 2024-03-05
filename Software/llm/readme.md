# LocalLLM
This is a very interesting project. We connect large language models with Home Assistant through Langchain, using the 
large language models to control smart furniture.

## Hardware Connection

- [reComputer](https://www.seeedstudio.com/reComputer-Industrial-J4012-p-5684.html)
- [reSpeaker](https://www.seeedstudio.com/ReSpeaker-USB-Mic-Array-p-4247.html?queryID=ce3473db56fa363c3ddbf45d9f465548&objectID=4247&indexName=bazaar_retailer_products)
- [Home Assistant Green](https://www.seeedstudio.com/Home-Assistant-Green-p-5792.html?queryID=2a68661c2c161dffa1ea6547eaf78474&objectID=5792&indexName=bazaar_retailer_products)
- [Display](https://www.seeedstudio.com/15-6-Inch-IPS-Portable-Monitor-p-5757.html?queryID=e09b53d6697c11023e91b14fe847b7e0&objectID=5757&indexName=bazaar_retailer_products)

**(Need a picture hardware connection)**

## LLM Installation

### Basic Dependencies
Use following command to install the basic dependencies:
```shell
pip3 install -r --no-cache-dir --verbose requirement.txt
```
### Riva

Refer to [this wiki](https://wiki.seeedstudio.com/Local_Voice_Chatbot/#install-riva-server)  to install Riva.

### Local LLM  

To simplify the installation process, we can refer to Dusty's [jetson-containers](https://github.com/dusty-nv/jetson-containers/tree/master/packages/llm/text-generation-inference) project to install text generation inference, and use text generation inference to load the [Llama2-7B](https://huggingface.co/meta-llama) large language model.

Open a new terminal on reComputer and run the following command.
```shell
cd ~
git clone https://github.com/dusty-nv/jetson-containers.git
cd jetson-containers
pip install -r requirements.txt
./run.sh $(./autotag text-generation-inference)
export HUGGING_FACE_HUB_TOKEN=<your hugging face token>
text-generation-launcher --model-id meta-llama/Llama-2-7b-chat-hf --port 8899
```
![avatar](./sources/text-generation-inference.png)
You can obtain the hugging face token [here](https://huggingface.co/docs/hub/security-tokens).
Please keep this terminal alive.

## Let's run it

### 1. The basic version ( WebUI+OpenAI )

```shell
python3 chatbot.py \
  --openai_api <openai api key> \
  --ha_access_token <homeassistant api key> \
  --ha_base_url <homeassistant base url>
```

### 2. Use Riva ASR/TTS Server
**Please make sure you have installed the Riva.**

```shell
python3 chatbot.py \
  --openai_api <openai api key> \
  --riva_server <riva server ip and port> \ 
  --ha_access_token <homeassistant api key> \
  --ha_base_url <homeassistant base url>
```

### 3. Use local LLM

**Please make sure you have installed the local model.**

You must set `openai_api` to `None` and set `text_inference_server` correctly. 
Please change the IP of the reComputer device in the following example.

```shell
python3 chatbot_v2.1.py --text_inference_server http://192.168.49.104:8899/generate
```

```shell
python3 chatbot.py \
  --text_inference_server http://<ip>:<port>/generate \
  --ha_access_token <homeassistant api key> \
  --ha_base_url <homeassistant base url>
```

## Run results
https://youtu.be/7t7UspjepdE?si=A8KTiYOZwjy5Ur5C

https://youtu.be/6fRZiXK9qT0?si=qdh0ijOq3WGenboA