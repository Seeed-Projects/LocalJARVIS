# LocalLLM
This is a very interesting project. We connect large language models with Home Assistant through Langchain, using the 
large language models to control smart furniture.


## requirements

### hardware Connection

- reComputer
- ...

### software

Need to add detailed installation methods

- Riva
- Langchain
- Gradio
- LLM

optional
```shell
pip3 install --no-cache-dir --verbose gradio==3.38.0
```




## Let's run it

### 1. The basic version ( WebUI+OpenAI )

```python
if __name__ == '__main__':
    chatbot = SeeeBot(openai_api='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')
    chatbot.run()
```

```shell
python3 chatbot.py
```

### 2. Use Riva

```python
if __name__ == '__main__':
    chatbot = SeeeBot(
        openai_api='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',
        riva_server="192.168.49.104:50051",
    )
    chatbot.run()
```

```shell
python3 chatbot.py
```

### 3. Use local LLM

#### Step 1. Install and run local LLM

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

Please note, you need to keep this terminal alive.

#### Step 2. Configure and start the chatbot

You must set `openai_api` to `None` and set `text_inference_server` correctly. 
Please change the IP of the reComputer device in the following example.

```python
if __name__ == '__main__':
    chatbot = SeeeBot(
        openai_api=None, 
        text_inference_server='http://192.168.49.103:8899/generate',
    )
    chatbot.run()
```

After configuring the parameters, you can use the command to start the chatbot.

```shell
python3 chatbot.py
```
