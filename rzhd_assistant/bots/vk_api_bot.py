"""
Module that provides functions for connect RASA and VK Bots via LongPools.

It send POST request with JSON data to RASA server
and get JSON data with answer from RASA.
"""
import os
import vk_api

from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from request_to_rasa import get_rasa_json

VK_TOKEN = os.getenv('VK_TOKEN')
vk = vk_api.VkApi(token='vk1.a.0c1isMsL1uhUmpFE_6IKm_WQUO4hYJZfaCNcXhXwN3PAAzvrfilVGvEcePbL6joV2QP5bNFAOXz0zb_dnbuIdAnPqmc4_J_IwsYhwIFEy-2cSwCYLp9mDcbJy2zlG9dm4FBPM5r-FP_DHO_y2OIe8lJ_ibDth-pnpMvvCv_3puL9f8G2fgZTBstE2-SYJ9yo7H232RoJoV7l7wTE-O7x1Q')


def write_msg(user_id, message):
    """Generate message for user.

    Args:
        user_id (_type_): vk user id
        message (_type_): text for user
    """
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': get_random_id(),
    })


def run():
    """Start VK bot."""
    longpoll = VkLongPoll(vk)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                write_msg(event.user_id, get_rasa_json(event.text))


if __name__ == '__main__':
    run()
