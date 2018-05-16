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