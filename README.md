# ChatGPT Persona Fallback Skill

When in doubt, ask chatgpt

You need to configure an api_key, get it at https://beta.openai.com/account/api-keys


## About 

Capabilities:
- Remembers what user said earlier in the conversation
- Trained to decline inappropriate requests

Limitations:

- May occasionally generate incorrect information
- May occasionally produce harmful instructions or biased content
- Limited knowledge of world and events after 2021

## Configuration

Under skill settings you can tweak some parameters for chatGPT


- `key` - your api_key to access OpenAI
- `persona` - can be used to create a "persona", give a personality to chatGPT
- `engine` - LLM model to use, valid options `"gpt-3.5-turbo", "ada", "babbage", "curie", "text-davinci-002", "text-davinci-003"`

The default persona is `The assistant is helpful, creative, clever, and very friendly, remembers conversations.`


## Examples 

* "Explain quantum computing in simple terms"
* "Got any creative ideas for a 10 year old’s birthday?"
