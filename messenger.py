# coding: utf-8
import os
import time
from fbmq import QuickReply, NotificationType
from fbpage import page
from models.all_models import *
from app.FacebookPlatform import FacebookPlatform

USER_SEQ = {}
CONFIDENCE_THRESHOLD = 0.5
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)


@page.handle_optin
def received_authentication(event):
    sender_id = event.sender_id
    recipient_id = event.recipient_id
    time_of_auth = event.timestamp

    pass_through_param = event.optin.get("ref")

    print("Received authentication for user %s and page %s with pass "
          "through param '%s' at %s" % (sender_id, recipient_id, pass_through_param, time_of_auth))

    page.send(sender_id, "Authentication successful")


@page.handle_echo
def received_echo(event):
    message = event.message
    message_id = message.get("mid")
    app_id = message.get("app_id")
    metadata = message.get("metadata")
    print("page id : %s , %s" % (page.page_id, page.page_name))
    print("Received echo for message %s and app %s with metadata %s" % (message_id, app_id, metadata))


# def send_humanly(sender_id, text):
#     send_typing_on(sender_id),
#     time.sleep(len(text.split(' '))/5.0)
#     send_message(sender_id, text)
#     send_typing_off(sender_id)


@page.handle_message
def received_message(event):
    platform = FacebookPlatform()
    platform.receive_message(event)

#
# def send_message(recipient_id, text):
#         page.send(recipient_id, text,
#                   callback=send_text_callback,
#                   notification_type=NotificationType.REGULAR)
#
#
# def send_text_callback(payload, response):
#     print('Callback send')
#
#
# def send_text_message(recipient, text):
#     page.send(recipient, text, metadata="DEVELOPER_DEFINED_METADATA")
#
#
# def initiate_feedback():
#     for p in models.select_participants():
#         page.send(p.fb_id, "We would appreciate your feedback!",
#                   quick_replies=[QuickReply(title="Okay", payload="PICK_OK"),
#                                  QuickReply(title="I'm busy", payload="PICK_NO")],
#                   metadata="DEVELOPER_DEFINED_METADATA")




#
# # TODO could be used to keep track of what questionnaire should be launched
# def bot_ask_participation(recipient, question):
#     page.send(recipient, question,
#               quick_replies=[QuickReply(title="OK", payload="PICK_OK"),
#                              QuickReply(title="No thanks", payload="PICK_NO")],
#               metadata="DEVELOPER_DEFINED_METADATA")


@page.callback(['PICK_OK'])
def bot_callback_ok(payload, event):
    # log participant
    bot_log_participant(event.sender_id)

    # Participant have accepted answering questionnaire.
    # This is the only place where it is OK to proceed from state 0 to 1
    # Ask first question

    current_state = State.get_state(event.sender_id)
    print("current_state == None {}".format(current_state is None))

    # Should not happen - State SHOULD be created at this point
    if current_state is None or current_state.q_numb != 0:
        print("Unexpected state in bot_callback_OK")
        print(str(event.sender_id))
        return

    # Get list of questions
    # questions = get_questions(current_state.qstnnr.id)
    questions = Questionnaire.select_all_questions(current_state.qstnnr.id)

    page.send(event.sender_id, questions[current_state.q_numb].question)


@page.callback(['PICK_NO'])
def bot_callback_no(payload, event):
    # log participant
    bot_log_participant(event.sender_id)

    current_state = State.get_state(event.sender_id)

    # Should not happen - State SHOULD be created at this point
    if current_state is None or current_state.q_numb != 0:
        print("Unexpected state in bot_callback_NO")
        return
    State.delete_state(event.sender_id)
    text = "Ok, maybe next time! Have a good day!"
    page.send(event.sender_id, text)


# def send_typing_off(recipient):
#     page.typing_off(recipient)
#
#
# def send_typing_on(recipient):
#     page.typing_on(recipient)



def bot_log_participant(fb_id):
    participant = Participant.get_participant(fb_id)
    if participant is None:
        profile = page.get_user_profile(fb_id)
        name = "{} {}".format(profile['first_name'], profile['last_name'])
        participant = Participant.create_participant(name, fb_id)
    return participant

