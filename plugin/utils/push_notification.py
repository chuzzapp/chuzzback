import json
import os
from skygear.action import push_users
from skygear.container import SkygearContainer


class PushNotificationPayload():

    def __init__(self, title_loc_key='', title_loc_args=None,
                 body_loc_key='', body_loc_args=None,
                 data=None):
        self.title_loc_key = title_loc_key
        self.title_loc_args = title_loc_args
        self.body_loc_key = body_loc_key
        self.body_loc_args = body_loc_args
        self.data = data

    def _build_apns_payload(self):
        payload = {
            'aps': {
                'alert': {
                    'title-loc-key': self.title_loc_key,
                    'title-loc-args': self.title_loc_args,
                    'loc-key': self.body_loc_key,
                    'loc-args': self.body_loc_args,
                }
            },
            'from': 'Chuzz',
            'operation': 'notification',
        }

        if self.data is not None:
            payload.update(self.data)

        return payload

    def _build_gcm_notification_payload(self):
        return {
            'notification': {
                'title_loc_key': self.title_loc_key,
                'title_loc_args': self.title_loc_args,
                'body_loc_key': self.body_loc_key,
                'body_loc_args': json.dumps(self.body_loc_args),
            }
        }

    def _build_gcm_data_payload(self):
        payload = {
            'content-available': '1'
        }

        if self.data is not None:
            payload.update(self.data)

        return {
            'data': payload
        }

    def build_payloads_to_send(self):
        return [
            {
                'apns': self._build_apns_payload(),
                'gcm': self._build_gcm_notification_payload(),
            },
            {
                'gcm': self._build_gcm_data_payload()
            }
        ]


def send_push_notification(user_ids, payload):
    container = SkygearContainer(
        endpoint=os.getenv('SKYGEAR_ENDPOINT'),
        api_key=os.getenv('SKYGEAR_APIKEY'),
    )

    for raw_payload in payload.build_payloads_to_send():
        push_users(container, user_ids, raw_payload)


def notify_followers_for_new_poll(user_ids, poll_id, poll_name,
                                  celebrity_name):
    send_push_notification(
        user_ids,
        PushNotificationPayload(
            body_loc_key='NOTIFICATION_NEW_CELEBRITY_POLL_BODY',
            body_loc_args=[celebrity_name, poll_name],
            data={'poll_id': poll_id}
        )
    )


def notify_users_for_interested_new_poll(user_ids, poll_id, poll_name):
    send_push_notification(
        user_ids,
        PushNotificationPayload(
            body_loc_key='NOTIFICATION_NEW_INTERESTED_POLL_BODY',
            body_loc_args=[poll_name],
            data={'poll_id': poll_id}
        )
    )


def notify_user_for_new_answer(user_id, poll_id, poll_name):
    send_push_notification(
        [user_id],
        PushNotificationPayload(
            body_loc_key='NOTIFICATION_NEW_ANSWER_BODY',
            body_loc_args=[poll_name],
            data={'poll_id': poll_id}
        )
    )
