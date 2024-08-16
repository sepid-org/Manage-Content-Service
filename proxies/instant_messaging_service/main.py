from django.conf import settings
import requests
from utilities.singleton_class import Singleton


class InstantMessagingServiceProxy(Singleton):
    url = settings.INSTANT_MESSAGE_URL

    def __init__(self, website):
        self.website = website

    def send_solve_question_reward_notification(self, recipient, question_id, cost):
        message = f'بابت حل سوال {question_id} به شما {cost} امتیاز اضافه شد'
        self._send_notification(recipient=recipient, message=message)

    def send_submit_answer_cost_notification(self, recipient, question_id, cost):
        message = f'بابت اقدام به حل سوال {question_id} {cost} قدر پول از شما کم شد'
        self._send_notification(recipient=recipient, message=message)

    def _send_notification(self, recipient, message):
        res = requests.post(
            f'{self.url}/send-message', json={'sender': self.website, 'recipient': recipient, 'message': message})
        return res.status_code
