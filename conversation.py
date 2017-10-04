import config
import apiai
import uuid
import json


class Conversation(object):
    def __init__(self):
        self.client = apiai.ApiAI(config.apiai['client_access_token'])
        self.last_answer = None

    def set_session(self, name_str):
        self.session_id = uuid.uuid3(uuid.NAMESPACE_DNS, name_str).hex

    def make_question(self, text):
        self.last_answer = self.__send_text(text)

    def get_answer(self):
        answer = ''
        if self.last_answer:
            answer = self.last_answer['result']['fulfillment']['speech']
        return answer

    def __send_text(self, text):
        request = self.client.text_request()
        request.session_id = self.session_id
        request.query = text

        response = request.getresponse()
        data = response.read().decode('utf-8')
        return json.loads(data)
