from fbpage import page as fbpage
import time
from fbmq import QuickReply, NotificationType
from app.ChatBot import Chatbot

class Platform:
    def __init__(self):
        self.name = 'default'
        self.page = None

    def send_humanly(self, sender_id, text):
        raise NotImplemented('Wit the hell?')

    def send_typing_off(self, recipient):
        raise NotImplemented('Wit the hell?')

    def send_typing_on(self, recipient):
        raise NotImplemented('Wit the hell?')

    def send_message(self, recipient_id, text):
        raise NotImplemented('Wit the hell?')

    def get_user_profile(self, user_id):
        raise NotImplemented('Wit the hell?')


class FacebookPlatform(Platform):
    USER_SEQ = {}

    def __init__(self):
        super(FacebookPlatform, self).__init__()
        self.name = 'FacebookPlatform'
        self.page = fbpage

    def send_humanly(self, sender_id, text):
        self.send_typing_on(sender_id),
        time.sleep(len(text.split(' ')) / 5.0)
        self.send_message(sender_id, text)
        self.send_typing_off(sender_id)

    def send_typing_off(self, recipient):
        self.page.typing_off(recipient)

    def send_typing_on(self, recipient):
        self.page.typing_on(recipient)

    def send_message(self, recipient_id, text):
        self.page.send(recipient_id, text, notification_type=NotificationType.REGULAR)

    def receive_message(self, event):
        sender_id = event.sender_id
        recipient_id = event.recipient_id
        time_of_message = event.timestamp
        message = event.message
        print("Received message for user %s and page %s at %s with message:"
              % (sender_id, recipient_id, time_of_message))
        print(message)

        seq = message.get("seq", 0)
        message_id = message.get("mid")
        app_id = message.get("app_id")
        metadata = message.get("metadata")

        message_text = message.get("text")
        message_attachments = message.get("attachments")
        quick_reply = message.get("quick_reply")

        # Should NOT take care of callbacks TODO this might be a dirty solution
        if quick_reply is not None:
            print("received message contains payload, returning")
            return

        # Retrieve labels
        nlp = message['nlp']
        keyword = None
        confidence = 0

        # Get keywords from nlp
        if nlp is not None:
            # We're expecting only one item. Facebook dev settings, Built-In NLP
            # However, seems I cant access item0, need to iterate through instead
            items = nlp['entities']
            for ent_id in items:
                # ent_id is a string containing the entity id
                keyword = items[ent_id][0]['value']
                confidence = items[ent_id][0]['confidence']

        print("Keyword = " + str(keyword) + ", Confidence = " + str(confidence))

        # TODO Not sure about the details. Avoids several handlings of the same event.
        seq_id = sender_id + ':' + recipient_id
        if FacebookPlatform.USER_SEQ.get(seq_id, -1) >= seq:
            print("Ignore duplicated request")
            return None
        else:
            FacebookPlatform.USER_SEQ[seq_id] = seq

        chatbot = Chatbot(self)
        chatbot.receive(nlp, sender_id)

    def get_user_profile(self, user_id):
        return self.page.get_user_profile(fb_user_id=user_id)