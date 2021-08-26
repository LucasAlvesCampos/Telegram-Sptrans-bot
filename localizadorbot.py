from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from apiSptrans import SPTransClient

token = 'SEU TOKEN DA SPTRANS'
sp = SPTransClient()
sp.auth(token)

STATE1 = 1
STATE2 = 2

def welcome(update, context):
    message = "Olá, " + update.message.from_user.first_name + "! Bem vindo ao rastreador de Ônibus!!! Para iniciar o rastreio de seu ônibus digite /rastreio"
    print(message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def rastreio(update, context):
    message = 'Por favor, digite o nome ou o número do Ônibus que deseja rastrear.  Exemplo: "Rio Pequeno" ou "477p"'
    update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True))
    return STATE1

def inputFeedback(update, context):
    feedback = update.message.text
    global data
    data = (sp.search_by_bus(update.message.text))
    for i in range(len(data)):
        if data[i]['sl'] == 1:
            context.bot.send_message(chat_id=update.message.chat_id, parse_mode="HTML", text=f"[OPÇÃO {i + 1}]<i> {data[i]['lt']} {data[i]['tp']} - {data[i]['ts']}</i> <strong>SENTIDO {data[i]['tp']}</strong>")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, parse_mode="HTML", text=f"[OPÇÃO {i + 1}]<i> {data[i]['lt']} {data[i]['tp']} - {data[i]['ts']}</i> <strong>SENTIDO {data[i]['ts']}</strong>")
    message = 'Por favor, digite qual opção deseja rastrear. Exemplo: "1"'
    update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True))
    return STATE2

def inputFeedback2(update, context):

    feedback = update.message.text

    if data[int(update.message.text)-1]['sl'] == 1:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode="HTML", text=f"Você escolheu a OPÇÃO {update.message.text}:<i> {data[int(update.message.text)-1]['lt']} {data[int(update.message.text)-1]['tp']} - {data[int(update.message.text)-1]['ts']}</i> <strong>SENTIDO {data[int(update.message.text)-1]['tp']}</strong>")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, parse_mode="HTML", text=f"Você escolheu a OPÇÃO {update.message.text}:<i> {data[int(update.message.text)-1]['lt']} {data[int(update.message.text)-1]['tp']} - {data[int(update.message.text)-1]['ts']}</i> <strong>SENTIDO {data[int(update.message.text)-1]['ts']}</strong>")

    local = sp.get_bus_position(data[int(update.message.text)-1]['cl'])
    for i in range (0, len(local['vs']), 1):
        context.bot.sendLocation(chat_id=update.message.chat_id,latitude=local['vs'][i]['py'] , longitude=local['vs'][i]['px'])

    context.bot.send_message(chat_id=update.message.chat_id, parse_mode="HTML", text=f"Fim do rastreio, para iniciar outro digite /rastreio")

    return ConversationHandler.END

def cancel(update, context):
    return ConversationHandler.END


def main():
    token = 'TOKEN DO BOT TELEGRAM'
    updater = Updater(token=token, use_context=True)

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('rastreio', rastreio)],
        states={
            STATE1: [MessageHandler(Filters.text, inputFeedback)],
            STATE2: [MessageHandler(Filters.text, inputFeedback2)]
        },
        fallbacks=[CommandHandler('cancel', cancel)])

    updater.dispatcher.add_handler(conversation_handler)

    updater.dispatcher.add_handler(CommandHandler("start", welcome))


    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()