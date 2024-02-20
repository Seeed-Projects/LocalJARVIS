from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
import requests


class CustomLLM(LLM):
    url = 'http://192.168.49.103:8899/generate'

    # Activate logits sampling
    do_sample: bool = False
    # Maximum number of generated tokens
    max_new_tokens: int = 20
    # The parameter for repetition penalty. 1.0 means no penalty.
    # See [this paper](https://arxiv.org/pdf/1909.05858.pdf) for more details.
    repetition_penalty: Optional[float] = None
    # Whether to prepend the prompt to the generated text
    return_full_text: bool = False
    # Stop generating tokens if a member of `stop_sequences` is generated
    stop: List[str] = []
    # Random sampling seed
    seed: Optional[int] = None
    # The value used to module the logits distribution.
    temperature: Optional[float] = None
    # The number of highest probability vocabulary tokens to keep for top-k-filtering.
    top_k: Optional[int] = None
    # If set to < 1, only the smallest set of most probable tokens with probabilities that add up to `top_p` or
    # higher are kept for generation.
    top_p: Optional[float] = None
    # truncate inputs tokens to the given size
    truncate: Optional[int] = None
    # Typical Decoding mass
    # See [Typical Decoding for Natural Language Generation](https://arxiv.org/abs/2202.00666) for more information
    typical_p: Optional[float] = None
    # Generate best_of sequences and return the one if the highest token logprobs
    best_of: Optional[int] = None
    # Watermarking with [A Watermark for Large Language Models](https://arxiv.org/abs/2301.10226)
    watermark: bool = False
    # Get generation details
    details: bool = False
    # Get decoder input token logprobs and ids
    decoder_input_details: bool = False
    # Return the N most likely tokens at each step
    top_n_tokens: Optional[int] = None

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _construct_query(self, prompt: str) -> List:
        headers = {"Content-Type": "application/json", }
        data = {
            'inputs': prompt,
            'parameters': {
                'do_sample': self.do_sample,
                'max_new_tokens': self.max_new_tokens,
                'repetition_penalty': self.repetition_penalty,
                'return_full_text': self.return_full_text,
                'stop': self.stop,
                'seed': self.seed,
                'temperature': self.temperature,
                'top_k': self.top_k,
                'top_p': self.top_p,
                'truncate': self.truncate,
                'typical_p': self.typical_p,
                'best_of': self.best_of,
                'watermark': self.watermark,
                'details': self.details,
                'decoder_input_details': self.decoder_input_details,
                'top_n_tokens': self.top_n_tokens
            },
        }
        return [headers, data]

    def _call(self, prompt: str, **kwargs) -> str:

        print(f"prompt >>>{prompt}<<<")
        # construct query
        query = self._construct_query(prompt=prompt)

        # post
        resp = requests.post(self.url, headers=query[0], json=query[1])

        if resp.status_code == 200:
            resp_json = resp.json()
            predictions = resp_json['generated_text']
            print(f">>>>{predictions}<<<<<<")
            return predictions
        else:
            return "waiting..."

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"url": self.url}


if __name__ == '__main__':
    from langchain.chains.conversation.memory import ConversationBufferWindowMemory
    from langchain.chains import ConversationChain
    from langchain_core.prompts.prompt import PromptTemplate

    llm = CustomLLM(url='http://192.168.49.103:8899/generate', temperature=0.5, max_new_tokens=100)
    memory = ConversationBufferWindowMemory(k=5)

    template = """ Please answer the human question in short sentences. Just answer the questions and don't generate too much content.
    Current conversation:
    {history}
    Human: {input}
    AI:
    """
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    conversation = ConversationChain(llm=llm, verbose=True, prompt=PROMPT, memory=memory)
    output = conversation.predict(input="How many countries are there in the world")
    print(output)
    output = conversation.predict(input="It is good")
    print(output)
# headers = {"Content-Type": "application/json", }
# data = {
#     'inputs': 'How many countries are there in the world',
#     'parameters': {
#         'max_new_tokens': 100,
#         'temperature': 0.5,
#     },
# }
# resp = requests.post('http://192.168.49.103:8899/generate', headers=headers, json=data)
#
# if resp.status_code == 200:
#     resp_json = resp.json()
#     predictions = resp_json['generated_text']
#     print(predictions)
# else:
#     print("waiting...")
