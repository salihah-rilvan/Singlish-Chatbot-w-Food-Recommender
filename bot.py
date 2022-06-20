import json
import requests
import time
import urllib
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from food_recommender import FoodRecommender as fr
from chat_model import ChatModel as cm
from chat_model_blenderbot import ChatModel as cm_bb
from recommender_context import RecommenderTrigger as rt 

TOKEN = "2071179099:AAFewX2SGYhLjK-FA1ohB1cr-vEXGG5tQTA"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

user_state = {}
chat_bot = cm(model_path="./checkpoint-60000")
# chat_bot_bb = cm_bb(model_path="./pytorch_model_v2")
recc_trigger = rt()

cuisines = []
with open('./data/cuisines_top15.txt') as c:
    cuisines = c.read().splitlines() 

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        reply_markup = None

        if("callback_query" in update):
            reply_markup = {}
            text = "You picked {}\nSend your location pls".format(update["callback_query"]["data"])
            chat = update["callback_query"]["message"]["chat"]["id"]
            if(chat not in user_state):
                user_state[chat] = { "cuisine" : { "text": update["callback_query"]["data"] , "datetime" : datetime.now().strftime('%Y-%m-%d %H:%M:%S') } }
            remove_markup(chat,update["callback_query"]["message"]["message_id"], update["callback_query"]["data"])
            answer_callback_query(update["callback_query"]["id"])
        elif("message" in update):
            if("location" in update["message"]):
                text = "Long: {}, Lat: {}".format(update["message"]["location"]["longitude"], update["message"]["location"]["latitude"])
                chat = update["message"]["chat"]["id"]
                if(chat in user_state):
                    current_datetime = datetime.now()
                    dt_diff = current_datetime - datetime.strptime(user_state[chat]["cuisine"]["datetime"], '%Y-%m-%d %H:%M:%S')
                    mins_diff = (dt_diff.days * 24 * 60) + (dt_diff.seconds/60)
                    if(mins_diff > 15):
                        del user_state[chat]
                        keyboard = {
                            "inline_keyboard": [
                                [
                                    {"text": "Chinese", "callback_data": "Chinese"},
                                    {"text": "Cafes", "callback_data": "Cafes"},
                                    {"text": "Japanese", "callback_data": "Japanese"},
                                    {"text": "Asian Fusion", "callback_data": "Asian Fusion"}
                                ],
                                [
                                    {"text": "Singaporean", "callback_data": "Singaporean"},
                                    {"text": "Seafood", "callback_data": "Seafood"},
                                    {"text": "Indian", "callback_data": "Indian"},
                                    {"text": "Italian", "callback_data": "Italian"}
                                ],
                                [
                                    {"text": "Thai", "callback_data": "Thai"},
                                    {"text": "Korean", "callback_data": "Korean"},
                                    {"text": "Bars", "callback_data": "Bars"},
                                    {"text": "Fast Food", "callback_data": "Fast Food"}
                                ]
                            ]
                        }
                        # keyboard = {
                        #     "inline_keyboard": [
                        #         [
                        #             {"text": "Asian", "callback_data": "Asian Fusion"},
                        #             {"text": "Thai", "callback_data": "Thai"}
                        #         ],
                        #         [
                        #             {"text": "Korean", "callback_data": "Korean"},
                        #             {"text": "Japanese", "callback_data": "Japanese"}
                        #         ]
                        #     ]
                        # }
                        text = "Take so long, select your cuisine again la"
                        reply_markup = json.dumps(keyboard)
                    else:
                        recc = fr()
                        food_recc = recc.get_ranked_restaurants((update["message"]["location"]["longitude"], update["message"]["location"]["latitude"]), user_state[chat]["cuisine"]["text"])
                        if food_recc:
                            text = "Here are some suggestions !\n\n"
                            for rc in food_recc:
                                text += "Name: {}\nAddress: {}\nRating: {}\n\n".format(rc["name"],rc["address"],rc["rating"])
                        else:
                            text = "Sorry there aren't any places with {} cuisine in your vicinity..".format(user_state[chat]["cuisine"]["text"])
                        del user_state[chat]
                else:
                    text = "Send me location for what, want to stalk me ah?"
            elif(recc_trigger.check_recommend_context(update["message"]["text"]) > 0.6):
                chat = update["message"]["chat"]["id"]
                if(chat in user_state):
                    current_datetime = datetime.now()
                    dt_diff = current_datetime - datetime.strptime(user_state[chat]["cuisine"]["datetime"], '%Y-%m-%d %H:%M:%S')
                    mins_diff = (dt_diff.days * 24 * 60) + (dt_diff.seconds/60)
                    if(mins_diff > 15):
                        del user_state[chat]
                        keyboard = {
                            "inline_keyboard": [
                                [
                                    {"text": "Chinese", "callback_data": "Chinese"},
                                    {"text": "Cafes", "callback_data": "Cafes"},
                                    {"text": "Japanese", "callback_data": "Japanese"},
                                    {"text": "Asian Fusion", "callback_data": "Asian Fusion"}
                                ],
                                [
                                    {"text": "Singaporean", "callback_data": "Singaporean"},
                                    {"text": "Seafood", "callback_data": "Seafood"},
                                    {"text": "Indian", "callback_data": "Indian"},
                                    {"text": "Italian", "callback_data": "Italian"}
                                ],
                                [
                                    {"text": "Thai", "callback_data": "Thai"},
                                    {"text": "Korean", "callback_data": "Korean"},
                                    {"text": "Bars", "callback_data": "Bars"},
                                    {"text": "Fast Food", "callback_data": "Fast Food"}
                                ]
                            ]
                        }
                        # keyboard = {
                        #     "inline_keyboard": [
                        #         [
                        #             {"text": "Asian", "callback_data": "Asian Fusion"},
                        #             {"text": "Thai", "callback_data": "Thai"}
                        #         ],
                        #         [
                        #             {"text": "Korean", "callback_data": "Korean"},
                        #             {"text": "Japanese", "callback_data": "Japanese"}
                        #         ]
                        #     ]
                        # }
                        text = "Take so long, select your cuisine again la"
                        reply_markup = json.dumps(keyboard)
                    else:
                        text = "You have selected a cuisine: " + user_state[chat]["cuisine"]["text"] + "\nPlease send your location for recommendation leh"
                else:
                    # keyboard = {
                    #     "inline_keyboard": []
                    # }
                    # t_count = 0
                    # temp_arrays = []
                    # for t in cuisines:
                    #     temp_arrays.append({"text": t, "callback_data": t})
                    #     t_count += 1
                    #     if(t_count == 4):
                    #         keyboard["inline_keyboard"].append(temp_arrays)
                    #         temp_arrays = []
                    #         t_count = 0

                    keyboard = {
                        "inline_keyboard": [
                            [
                                {"text": "Chinese", "callback_data": "Chinese"},
                                {"text": "Cafes", "callback_data": "Cafes"},
                                {"text": "Japanese", "callback_data": "Japanese"},
                                {"text": "Asian Fusion", "callback_data": "Asian Fusion"}
                            ],
                            [
                                {"text": "Singaporean", "callback_data": "Singaporean"},
                                {"text": "Seafood", "callback_data": "Seafood"},
                                {"text": "Indian", "callback_data": "Indian"},
                                {"text": "Italian", "callback_data": "Italian"}
                            ],
                            [
                                {"text": "Thai", "callback_data": "Thai"},
                                {"text": "Korean", "callback_data": "Korean"},
                                {"text": "Bars", "callback_data": "Bars"},
                                {"text": "Fast Food", "callback_data": "Fast Food"}
                            ]
                        ]
                    }
                    text = "Please select a cuisine"
                    reply_markup = json.dumps(keyboard)
            else:
                text = chat_bot.generate_response(update["message"]["text"])
                chat = update["message"]["chat"]["id"]
            send_message(text, chat, reply_markup)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def remove_markup(chat_id,message_id,cuisine):
    keyboard = {
        "inline_keyboard": []
    }
    get_url(URL+"editMessageText?chat_id={}&message_id={}&reply_markup={}&text=You have selected a cuisine: {} \nSend your location for recommendation ah".format(chat_id,message_id,json.dumps(keyboard),cuisine))

def answer_callback_query(callback_id):
    get_url(URL+"answerCallbackQuery?callback_query_id={}".format(callback_id))

def send_message(text, chat_id, markup):
    text = urllib.parse.quote_plus(text)
    if(markup):
        url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(text, chat_id,markup)
    else:
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

# def main() -> None:
#     """Run the bot."""
#     # Create the Updater and pass it your bot's token.
#     updater = Updater("2071179099:AAFewX2SGYhLjK-FA1ohB1cr-vEXGG5tQTA")
#     # Start the Bot
#     updater.start_polling()

#     # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT
#     updater.idle()


if __name__ == '__main__':
    main()

