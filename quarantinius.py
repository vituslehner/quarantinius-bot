#!/usr/bin/env python

import telebot
from telebot import types
import random
import sys
from threading import Timer



TOKEN = ""
with open('.token', 'r') as file:
    TOKEN = file.read().replace('\n', '')

bot = None
bot = telebot.TeleBot(TOKEN)

user = bot.get_me()


challenges = [
    [
        {"type": "textonly", "text": "Ja nice, alle am Start. Dann kann der Spaß beginnen. Ihr werdet von mir jede Menge Challenges und Quizes bekommen, die ihr als Gruppe lösen müsst. Klickt euch während eures Videocalls einfach hier durch.", "gifUrl": ""},
        #{"type": "question", "text": "Frage a1", "options": ["Antwort a", "Antwort b", "Antwort c"], "option_correct": 0},
        {"type": "activity",
            "text": "Starten wir mit der etwas anderen Vorstellungsrunde.\n\nHallo, ich bin’s der [Quarantinius], der ja momentan gerne [Faxen] macht in [eurer Gruppe]. Jetzt ihr, ersetzt die Felder einfach und nennt auch euren letzten nicht-virtuellen Kontakt. Ich Spaßvogel hatte natürlich keinen 😜"},
        {"type": "textonly", "text": "Ihr macht auch allen Blödsinn mit, oder? Als würdet ihr euch nicht schon kennen. Naja jetzt lernt ihr euch und eurer aller safe spaces noch besser kennen. "},
        {"type": "activity", "text": "Denn jetzt präsentieren alle ihren Lieblingsgegenstand pro Raum. Auf geht’s, auf Entdeckertour durch die Wohnung! Die Person mit dem witzigsten Intro von eben beginnt."},
        {"type": "textonly", "text": "Ja schade, dass ich nicht mit im Video Call bin. Zu der Erkenntnis werde ich heute immer wieder kommen…"},
        {"type": "activity", "text": "Ok, nächster Punkt. Alle stellen sich im Call auf stumm. Gemutet erzählt ihr den anderen in einem Wort, was ihr sonst so macht gerade. Die anderen müssen das Gesagte erraten. Klappt das nicht auf Anhieb, versucht es mit Pantomime noch einmal. Die Person mit der schlechtesten Kamera/Übertragung beginnt. Wer’s errät, ist als nächstes dran."},
        {"type": "activity", "text": "Kommando Pimperle. Wer kennt’s nicht. Die Person, die zuletzt Sport gemacht hat, gibt die Kommandos. Jetzt heißt es aufmerksam sein. Jede*r hat nur 3 Leben."},
        {"type": "activity", "text": "Eigentlich gab es eben keine Verlierer. Alle sind Gewinner, ihr wolltet nur unterschiedlich lange spielen. Feiert euch mit einer Laola Welle über die Bildschirme hinweg. Bei der Person im linken oberen Bildschirm startet die Welle bis sie rechts unten angekommen ist. Und dann wieder zurück!"},
        {"type": "activity",
            "text": "Naja, ‘der Reihe nach’ geht anders. Das üben wir noch einmal in etwas anderer Form. Dafür holen sich alle ein Zettelchen und notieren (im Geheimen) ihr Highlight mit dieser Gruppe. "},
        {"type": "activity", "text": "Jetzt wandert der Zettel virtuell, von der oberen linken Ecke des oberen linken Bildschirms über alle dazwischenliegenden Bildschirm zur rechten unteren Ecke des Bildschirms rechts unten. Verstanden? Das heißt auf der Höhe, wo der Zettel einen Bildschirm verlässt, startet er auf dem daneben. Dabei dürfen möglichst keine Sprünge entstehen, zumindest darf die untere Ecke eines Bildschirms nicht vor der letzten Person erreicht werden. Versucht das erstmal, bevor ich auf euer aller Zettel eingehe."},
        {"type": "activity", "text": "Geschafft? Das Ganze war so eine Art Stille Post, nur anders! Jetzt geben nämlich alle anderen eine Vermutung ab, was die letzte Person als Highlight auf ihren Zettel geschrieben hat. Sobald dies aufgelöst wurde, ratet ihr bei der vorletzten, dann der vorvorletzten Person und so weiter. "},
        {"type": "activity",
            "text": "Was ihr schon alles zusammen erlebt habt. Da könnt ihr ja gleich weiter in Erinnerungen schwelgen. Wer mag ruft sich ein gemeinsam entstandenes Foto vor Augen und beschreibt es den anderen (möglichst abstrakt oder humorvoll, in wenigen Worten oä.).  "},
        {"type": "textonly", "text": "Mit dieser Aufgabe könntet ihr wohl ewig weiter machen. Macht das gerne, wenn euch danach ist. Ansonsten endet diese Session hier, habt Spaß bei einer anderen bzw. vergesst nicht, euch fürs nächste Mal zu verabreden. Apropos, das Ganze geht auch ohne Video Call, ganz einfach in eurer Telegram Gruppe. Wir hören voneinander!"},

    ]
]

groups = []
# list that stores each group
# group is dict that stores challenges


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


@bot.message_handler(commands=['start'])
def send_start(message):
    try:
        global groups

        rand_chall = random.randint(0, len(challenges)-1)
        group_challenges = challenges[rand_chall]
        group = {"chat_id": message.chat.id, "challenges": group_challenges,
                 "current_challenge_index": 0, "score": 0}

        group_index = find(groups, "chat_id", message.chat.id)
        if group_index == -1:
            groups.append(group)
        else:
            groups[group_index] = group

        bot.reply_to(message, "Na dann geht's los!")
        do_challenge(group_challenges[0], message)

    except:
        print("Unexpected error in send_start: {}".format(sys.exc_info()[0]))


@bot.message_handler(commands=['next'])
def send_next(message):
    try:
        next_challenge(message)
    except:
        print("Unexpected error in send_next: {}".format(sys.exc_info()[0]))


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Tippe /start um loszulegen.")


def do_challenge(challenge, message):
    try:
        c_type = challenge["type"]
        c_text = challenge["text"]

        if c_type == "activity":
            inline_markup = types.InlineKeyboardMarkup()
            inline_markup.add(types.InlineKeyboardButton(
                "Geschafft 🙂", callback_data="yes"))
            inline_markup.add(types.InlineKeyboardButton(
                "Nicht geschafft 😕", callback_data="no"))

            send_message(message.chat.id, c_text, reply_markup=inline_markup)

        elif c_type == "textonly":
            send_message(message.chat.id, challenge["text"])
            Timer(3, next_challenge, [message]).start()

        elif c_type == "question":
            options = challenge["options"]

            inline_markup = types.InlineKeyboardMarkup()
            for index, option in enumerate(options):
                button = types.InlineKeyboardButton(
                    option, callback_data=index + 1)
                inline_markup.add(button)

            send_message(message.chat.id, c_text, reply_markup=inline_markup)

    except KeyError as e:
        print(e)
    except:
        print("Unexpected error in do_challenge: {}".format(sys.exc_info()[0]))


def next_challenge(message):
    try:
        global groups

        group_index = find(groups, "chat_id", message.chat.id)
        if group_index == -1:
            send_message(
                message.chat.id, "Wir kennen uns doch noch garnicht?! Tippe /start um ein neues Spiel zu starten.", reply_to=message)
            return

        group = groups[group_index]

        next_challenge_index = group["current_challenge_index"] + 1
        challenge_count = len(group["challenges"])

        if next_challenge_index < challenge_count:
            next_challenge = group["challenges"][next_challenge_index]
            do_challenge(next_challenge, message)
        else:
            #send_message(message.chat.id, "Das war's! Dein Score beträgt {}. Tippe /start um ein neues Spiel zu starten.".format(group["score"]))
            final_summary(group["score"], message)

        group["current_challenge_index"] = next_challenge_index
        groups[group_index] = group
    except:
        print("Unexpected error in next_challenge: {}".format(
            sys.exc_info()[0]))


@bot.callback_query_handler(func=lambda call: True)
def inline_callback(call):
    try:
        global groups
        message = call.message

        group_index = find(groups, "chat_id", message.chat.id)
        if group_index == -1:
            print("callback but no group")
            return

        bot.answer_callback_query(call.id, "Erledigt!")
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id, reply_markup=None)

        group = groups[group_index]

        if group["current_challenge_index"] >= len(group["challenges"]):
            send_message(
                message.chat.id, "Wie spielen doch garnicht! Tippe /start um ein neues Spiel zu starten.", reply_to=message)

        current_challenge = group["challenges"][group["current_challenge_index"]]

        if current_challenge["type"] == "question":
            index = int(float(call.data)) - 1
            answer = current_challenge["options"][index]

            send_message(message.chat.id, "Antwort: " + answer)

            if current_challenge["option_correct"] == index:
                send_message(message.chat.id, "Sehr schön, das war richtig!")
                group["score"] += 1
            else:
                send_message(message.chat.id,
                             "Leider falsch! Beim nächsten Mal vielleicht...")

        if current_challenge["type"] == "activity":
            answer = call.data

            if answer == "yes":
                send_message(message.chat.id, "Gute Arbeit!")
                group["score"] += 1
            else:
                send_message(message.chat.id,
                             "Kann ja nicht jedes Mal klappen.")
        next_challenge(message)

    except:
        print("Unexpected error in inline_callback: {}".format(
            sys.exc_info()[0]))


def internal_send(chat_id, text, reply_markup, reply_to):
    if reply_to != None:
        bot.reply_to(reply_to, text, reply_markup=reply_markup)
    else:
        bot.send_message(
            chat_id, text, reply_markup=reply_markup)


def send_message(chat_id, text, reply_markup=None, schedule_in_secs=2, reply_to=None):
    print(chat_id)
    try:
        if schedule_in_secs == None:
            internal_send(chat_id, text, reply_markup, reply_to)
        else:
            t = Timer(schedule_in_secs, internal_send, args=[
                      chat_id, text, reply_markup, reply_to])
            t.start()
    except NameError as e:
        print(e)
    except:
        print("Unexpected error in send_message: {}".format(sys.exc_info()[0]))


def final_summary(score, message):
    try:
        if score == 2:
            bot.send_message(
                message.chat.id, "Das war ja spitzenmäßig!! Ihr habt {} Punkte erreicht.".format(score))
            bot.send_animation(
                message.chat.id, "https://media.giphy.com/media/5oGIdt1xapQ76/giphy.gif")
        elif score == 1:
            bot.send_message(
                message.chat.id, "Nicht übel. Ihr habt {} Punkte".format(score))
            bot.send_animation(
                message.chat.id, "https://media.giphy.com/media/nXxOjZrbnbRxS/giphy.gif")
        elif score == 0:
            bot.send_message(
                message.chat.id, "Beim nächsten mal wird's bestimmt besser. Ihr habt immerhin {} Punkte erreicht.".format(score))
            bot.send_animation(
                message.chat.id, "https://media.giphy.com/media/3oEjI80DSa1grNPTDq/giphy.gif")
    except:
        print("Unexpected error in final_summary: {}".format(
            sys.exc_info()[0]))


bot.polling()
