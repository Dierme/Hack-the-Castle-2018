from app.Platform import Platform
from models.State import State
from models.Participant import Participant


class Chatbot:
    def __init__(self, platform: Platform):
        self.pltfm = platform

    def log_user(self, user_id):
        participant = Participant.get_participant(user_id)
        if participant is None:
            profile = self.pltfm.get_user_profile(user_id)
            name = "{} {}".format(profile['first_name'], profile['last_name'])
            participant = Participant.create_participant(name, user_id)
        return participant

    def receive(self, nlp, sender_id):
        # Put new participants in DB
        self.log_user(sender_id)

        # Determine state
        current_state = State.get_state(sender_id)
        # print("current_state == None {}".format(current_state is None))

        if current_state is None:
            # Check if keyword is available and confidence is high enough'
            # TODO: Check that there is a keywork inside nlp
            if not nlp:
                self.pltfm.send_message(sender_id, "I'm sorry, but I have failed to interpret you")
                return

            # Check if keyword should trigger questionnaire
            # questionnaire = Questionnaire.get_questionnaire(keyword)
            #
            # if questionnaire is not None:
            #     # Questionnaire is found, set state and retrieve questions
            #     current_state = State.create_state(event.sender_id, questionnaire.id)
            #     print("State created, qnnr={}".format(current_state.q_numb))
            #     # questions = get_questions(current_state.qstnnr.id)
            #
            #     # Get user confirmation that user is interested in questionnaire
            #     # Could be solved by using State 0 to trigger quick_reply and never increment
            #     #       from 0->1 unless callback is OK
            #     # First question in Questionnaire contains text question to ask for participation
            #
            #     question = "Is it ok if I ask you a few questions about {}".format(questionnaire.title)
            #     bot_ask_participation(event.sender_id, question)
            #     # page.send(event.sender_id, questions[current_state.q_numb].question)

            # else:

            # Info state
            # info = Info.get_info(keyword)
            # if info is not None:
            #     bot_reply_info(event, info, keyword)
            # else:
            self.pltfm.send_message(sender_id, "I'm sorry, but I have no information for you")
        else:
            # TODO: remove when working with questionnaire
            self.pltfm.send_message(sender_id, "We should never really come here")

            # State is not None
            # Current msg from user concidered as questionnaire answer
            # State contains info on last q asked

            # If State q_numb == 0, it should be handled by callback function
            # Execution here could indicate a bug. Deleting state to avoid getting stuck
            # if current_state.q_numb == 0:
            #     State.delete_state(event.sender_id)
            #     return

            # retrieve relevant questions
            # questions = get_questions(current_state.qstnnr.id)
            # questions = Questionnaire.select_all_questions(current_state.qstnnr.id)
            #
            # last_question_id = questions[current_state.q_numb].id
            #
            # # Save answer to DB.
            # answer = event.message.get("text")
            # Feedback.create_feedback(last_question_id, event.sender_id, answer)
            #
            # # Iterate state
            # current_state = State.inc_state(event.sender_id)
            #
            # # Ask next question or thank user
            #
            # if current_state.q_numb >= len(questions):
            #     page.send(event.sender_id, "Thank you")
            #     State.delete_state(event.sender_id)
            # else:
            #     page.send(event.sender_id, questions[current_state.q_numb].question)


# def bot_log_participant(fb_id):
#     participant = Participant.get_participant(fb_id)
#     if participant is None:
#         profile = page.get_user_profile(fb_id)
#         name = "{} {}".format(profile['first_name'], profile['last_name'])
#         participant = Participant.create_participant(name, fb_id)
#     return participant
#
#
# # Retrieve info from DB and pass when calling this function
# def bot_reply_info(event, info, keyword):
#     reply = "Sorry, I have no information about '{}'".format(keyword)
#     if info is not None:
#         reply = info.info_text
#     page.send(event.sender_id, reply)


# # Launching questionnaire from web interface (organizer)
# # Wont launch for participants already in questionnaire - states are not advanced enough to handle this.
# def bot_launch_questionnaire_all_participants(questionnaire):
#     for participant in Participant.select_all_participants():
#         current_state = State.get_state(participant.fb_id)
#         if current_state is None:
#             # Launch questionnaire
#             # Set state
#             current_state = State.create_state(participant.fb_id, questionnaire.id)
#             print("State created, qnnr={}".format(current_state.q_numb))
#             # Ask participant
#             question = "We would like to have your opinion on {}. Is it ok if I ask you a few questions?".format(questionnaire.title)
#             bot_ask_participation(participant.fb_id, question)
#
#
# # Arg String msg is message to all registered participants
# def bot_msg_all_participants(msg):
#     for participant in Participant.select_all_participants():
#         page.send(participant.fb_id, msg)
#
#
# def bot_receive(event, keyword, confidence):
#     # Put new participants in DB
#     bot_log_participant(event.sender_id)
#
#     # Determine state
#     current_state = State.get_state(event.sender_id)
#     print("current_state == None {}".format(current_state is None))
#     if current_state is None:
#         # Check if keyword is available and confidence is high enough
#         if confidence < CONFIDENCE_THRESHOLD or keyword is None:
#             page.send(event.sender_id, "I'm sorry, but I have failed to interpret you")
#             return
#
#         # Check if keyword should trigger questionnaire
#         questionnaire = Questionnaire.get_questionnaire(keyword)
#
#         if questionnaire is not None:
#             # Questionnaire is found, set state and retrieve questions
#             current_state = State.create_state(event.sender_id, questionnaire.id)
#             print("State created, qnnr={}".format(current_state.q_numb))
#             # questions = get_questions(current_state.qstnnr.id)
#
#             # Get user confirmation that user is interested in questionnaire
#             # Could be solved by using State 0 to trigger quick_reply and never increment
#             #       from 0->1 unless callback is OK
#             # First question in Questionnaire contains text question to ask for participation
#
#             question = "Is it ok if I ask you a few questions about {}".format(questionnaire.title)
#             bot_ask_participation(event.sender_id, question)
#             # page.send(event.sender_id, questions[current_state.q_numb].question)
#
#         else:
#             #Info state
#             info = Info.get_info(keyword)
#             if info is not None:
#                 bot_reply_info(event, info, keyword)
#             else:
#                 page.send(event.sender_id, "I'm sorry, but I have no information for you")
#     else:
#         # State is not None
#         # Current msg from user concidered as questionnaire answer
#         # State contains info on last q asked
#
#         # If State q_numb == 0, it should be handled by callback function
#         # Execution here could indicate a bug. Deleting state to avoid getting stuck
#         # if current_state.q_numb == 0:
#         #     State.delete_state(event.sender_id)
#         #     return
#
#         # retrieve relevant questions
#         # questions = get_questions(current_state.qstnnr.id)
#         questions = Questionnaire.select_all_questions(current_state.qstnnr.id)
#
#         last_question_id = questions[current_state.q_numb].id
#
#         # Save answer to DB.
#         answer = event.message.get("text")
#         Feedback.create_feedback(last_question_id, event.sender_id, answer)
#
#         # Iterate state
#         current_state = State.inc_state(event.sender_id)
#
#         # Ask next question or thank user
#
#         if current_state.q_numb >= len(questions):
#             page.send(event.sender_id, "Thank you")
#             State.delete_state(event.sender_id)
#         else:
#             page.send(event.sender_id, questions[current_state.q_numb].question)