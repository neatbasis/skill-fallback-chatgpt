import openai as ai
from mycroft import FallbackSkill, intent_file_handler

class ChatGPTSkill(FallbackSkill):

    def __init__(self, name="ChatGPT", bus=None, use_settings=True):
        super().__init__(name, bus, use_settings)
        self._chat = None
        self.max_utts = 15  # memory size TODO from skill settings
        self.qa_pairs = []  # tuple of q+a
        self.messages = []
        self.current_q = None
        self.current_a = None
        self.messages = self.initial_prompt

    def initialize(self):
        self.add_event("speak", self.handle_speak)
        self.add_event("recognizer_loop:utterance", self.handle_utterance)
        self.register_fallback(self.ask_chatgpt, 85)
        
        
    @intent_file_handler('ask.chatgpt.intent')
    def handle_chatgpt(self, message):
        self.ask_chatgpt(message)

    def handle_utterance(self, message):
        utt = message.data.get("utterances")[0]
        self.current_q = utt
        self.current_a = None
        
        # TODO: imperfect, subject to race conditions between bus messages
        # use session_id/ident to track all matches

    def handle_speak(self, message):
        utt = message.data.get("utterance")

        if not self.current_q:
            # TODO - use session_id/ident to track all matches
            # append to previous question if multi-speak answer
            return
        if utt and self.memory:
            self.qa_pairs.append((self.current_q, utt))
            self.messages.append({"role": "user", "content": self.current_q})
            self.messages.append({"role": "system", "content": utt})
        self.current_q = None
        self.current_a = None

    @property
    def memory(self):
        return self.settings.get("memory", True)

    @property
    def engine(self):
        return self.settings.get("engine", "davinci")

    @property
    def initial_prompt(self):
        default_prompt = "The assistant is helpful, creative, clever, and very friendly, remembers conversations"
        content = self.settings.get("initial_prompt", default_prompt)
        return [{"role": "system", "content": content}]

    @property
    def chatgpt(self):
        # this is a property to allow lazy init
        # the key may be set after skill is loaded
        key = self.settings.get("key")
        if not key:
            raise ValueError("OpenAI api key not set in skill settings.json")
        if not self._chat:
            ai.api_key = key
            self._chat = ai.ChatCompletion()
        return self._chat

    @property
    def chat_history(self):
        messages = self.initial_prompt + self.messages[-self.max_utts:]
        return messages

    def get_prompt(self, utt):
        prompt = self.chat_history
        return prompt

    def ask_chatgpt(self, message):
        utterance = message.data['utterance']
        prompt = self.get_prompt(utterance)
        response = self.chatgpt.create(
            model="gpt-3.5-turbo", 
            messages=prompt+[{"role": "user", "content": utterance}]
        )
        message = response.choices[0]['message']
        if self.memory:
            self.messages.append(message)
        self.speak(message['content'])
        return True

def create_skill():
    return ChatGPTSkill()

