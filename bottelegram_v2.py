from asyncore import dispatcher
import string
from tracemalloc import start
from telegram import *
from telegram.ext import *
import requests

updater = Updater(token="5449080279:AAEMmhTKME9SZXpDUTn2jSQHbpwsc6uTQGg")
dispatcher = updater.dispatcher

def menu(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("Municipios", callback_data="municipios-listar")], [InlineKeyboardButton("Estados", callback_data="estados-listar")], [InlineKeyboardButton("Combustiveis", callback_data="combustiveis-listar")]]
    texto = "Bem-vindo ao Gasolina Bot!\nEscolha uma opção para continuar (Clique no item desejado):"
    return context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text=texto)

def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("Teste")], [KeyboardButton("Teste 2")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bem-Vindo!", reply_markup=ReplyKeyboardMarkup(buttons))

def ListarEstados(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarEstados')
    resposta = r.json()

    for estado in resposta:
        tipoComando = "{0}-estado".format(estado)
        buttons.append([InlineKeyboardButton(estado, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Lista de Estados disponíveis para consulta")

def msgMenuNovamente(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("Sim", callback_data="menu-listar")]]
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Deseja ver o menu principal novamente?")

def ListarMunicipios(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarMunicipios')
    resposta = r.json()

    for municipio in resposta:
        tipoComando = "{0}-municipio".format(municipio)
        buttons.append([InlineKeyboardButton(municipio, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Lista de Municipios disponíveis para consulta")

def ListarCombustiveis(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarProdutos')
    resposta = r.json()

    for combustivel in resposta:
        tipoComando = "{0}-combustiveis".format(combustivel)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Lista de Combustiveis disponíveis para consulta")  

def messageHandler(update: Update, context: CallbackContext):    

    if update.message.text.lower() != "estados" and update.message.text.lower() != "municipios" and update.message.text.lower() != "combustiveis":
        menu(update, context)

    if "estados".lower() in update.message.text.lower():
        ListarEstados(update, context)

    if "municipios".lower() in update.message.text.lower():
        ListarMunicipios(update, context)

    if "combustiveis".lower() in update.message.text.lower():
        ListarCombustiveis(update, context)

def queryHandlerEstados(update: Update, context: CallbackContext, estado: string):
    r = requests.get(f'http://localhost:5000/api/v1/Registro/RetornarTodosPrecosPorEstado/{estado}')
    resposta = r.json()

    respString = (f"Preço médio de revenda dos combustiveis referentes ao estado do {estado}\n\n")

    for resp in resposta:
        respString += "\nProduto: " + resp['produto']
        respString += "\nPreço médio de revenda: R$" + str(resp['preco_medio_revenda'])
        respString += "\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString)

def queryHandlerMunicipios(update: Update, context: CallbackContext, municipio: string):
    r = requests.get(f'http://localhost:5000/api/v1/Registro/RetornarTodosPrecosPorMunicipio/{municipio}')
    resposta = r.json()

    respString = (f"Preço médio de revenda dos combustiveis referentes ao municipio do {municipio}\n\n")

    for resp in resposta:
        respString += "\nProduto: " + resp['produto']                
        respString += "\nPreço médio de revenda: R$" + str(resp['preco_medio_revenda'])
        respString += "\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString)

def queryHandlerCombustiveis(update: Update, context: CallbackContext, combustivel: string):
    r = requests.get(f'http://localhost:5000/api/v1/Registro/RetornarTodosPrecosPorCombustivel/{combustivel}')
    resposta = r.json()

    respString = (f"Preço médio de revenda do combustivel {combustivel} listado por estado\n\n")

    for resp in resposta:
        respString += "\nEstado: " + resp['estado']
        respString += "\nPreço médio de revenda: R$" + str(resp['preco_medio_revenda'])
        respString += "\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString)   

def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()

    query = query.split('-')
    arg1 = query[0]
    tipoComando = query[1]

    if tipoComando == "listar":
        if arg1 == "estados":
            ListarEstados(update, context)            
        elif arg1 == "municipios":
            ListarMunicipios(update, context)            
        elif arg1 == "combustiveis":
            ListarCombustiveis(update, context)            
        elif arg1 == "menu":
            menu(update, context)
    else:
        if tipoComando == "estado": # Caso seja um ESTADO
            queryHandlerEstados(update, context, arg1)
            msgMenuNovamente(update, context)

        elif tipoComando == "municipio": # Caso seja um MUNICIPIO
            queryHandlerMunicipios(update, context, arg1)
            msgMenuNovamente(update, context)

        elif tipoComando == "combustiveis": # Caso seja um COMBUSTIVEL
            queryHandlerCombustiveis(update, context, arg1)
            msgMenuNovamente(update, context)


dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))

updater.start_polling()