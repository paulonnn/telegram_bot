from asyncore import dispatcher
from contextlib import nullcontext
import string
from tracemalloc import start
from telegram import *
import telegram
from telegram.ext import *
import requests
from datetime import date

DATA_ATUAL = date.today().strftime("%d/%m/%Y")

# Token para funcionamento do BOT
updater = Updater(token="5449080279:AAEMmhTKME9SZXpDUTn2jSQHbpwsc6uTQGg")
dispatcher = updater.dispatcher

 # Listar Menu com as opções
def menu(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("Municipios", callback_data="municipios-listar")],
        [InlineKeyboardButton("Estados", callback_data="estados-listar")],        
        [InlineKeyboardButton("Postos mais baratos (por combustível)", callback_data="combustiveisBaratos-listar")],
        [InlineKeyboardButton("Verificar endereço dos postos mais baratos (por municipio e combustível)", callback_data="combustiveisBaratosPorMunicipio-listar")],
        [InlineKeyboardButton("Avaliar o BOT", callback_data="opcao-avaliar")]]
    texto = "Bem-vindo ao Gasolina Bot!\nEscolha uma opção para continuar (<b><i>Clique</i></b> no item desejado):"
    return context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text=texto, parse_mode=telegram.constants.PARSEMODE_HTML)

# TESTE
def startCommand(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton("Teste")], [KeyboardButton("Teste 2")]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bem-Vindo!", reply_markup=ReplyKeyboardMarkup(buttons))

# Pergunta se o usuario deseja mostrar o menu novamente
def msgMenuNovamente(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("Sim", callback_data="menu-listar")]]
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Deseja ver o menu principal novamente?", parse_mode=telegram.constants.PARSEMODE_HTML)

# Lista todos os Estados registrados no banco
def ListarEstados(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarEstados')
    resposta = r.json()

    for estado in resposta['data']:
        tipoComando = "{0}-estado".format(estado)
        buttons.append([InlineKeyboardButton(estado, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Estados disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)

# Lista todos os Municipios registrados no banco
def ListarMunicipios(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarMunicipios')
    resposta = r.json()

    for municipio in resposta['data']:
        tipoComando = "{0}-municipio".format(municipio)
        buttons.append([InlineKeyboardButton(municipio, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Municipios disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)

def ListarMunicipiosCotacaoPosto(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/CotacaoPosto/RetornarMunicipios')
    resposta = r.json()

    for municipio in resposta['data']:
        tipoComando = "{0}-BaratosComEnd".format(municipio)
        buttons.append([InlineKeyboardButton(municipio, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Municipios disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)    

# Lista todos os Combustiveis registrados no banco para o endpoint de RETORNAR PRODUTOS
def ListarCombustiveis(update: Update, context: CallbackContext, municipio: string):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarProdutos')
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-combustiveis-{1}".format(combustivel, municipio)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Combustiveis disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)  

def MenuListarMunicipiosBaratos(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarMunicipios')
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-municipiosBaratos".format(combustivel)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de municipios disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)  

# Lista o preço de todos os combustiveis por Estado escolhido
def queryHandlerListarMunicipiosBaratos(update: Update, context: CallbackContext, municipio: string):
    r = requests.get(f'http://localhost:5000/api/v1/Registro/PrecoMediaASCPorMunicipio/{municipio}')
    resposta = r.json()

    if resposta['status'] == 200:
        respString = (f"<b>TOP 3 municipios mais baratos {municipio}</b>\nData da atualização: {DATA_ATUAL}\n")

        for resp in resposta['data']:        
            respString += "\n<b>Produto:</b> " + resp['produto']
            respString += "\n<b>Preço médio de revenda:</b> R$" + str(round(resp['preco_medio_revenda'], 2))
            respString += "\n<b>Número de postos pesquisados: </b>" + str(resp['numero_de_postos_pesquisados'])
            respString += "\n"
    else:
        respString = "Um erro ocorreu, por favor tente novamente."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)

# Lista todos os Combustiveis registrados no banco para o endpoint de LISTAR TOP 3 MAIS BARATOS POR PRODUTO (combustivel)
def MenuListarCombustiveisBaratos(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarProdutos')
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-combustiveisBaratos".format(combustivel)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Combustiveis disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)  

# def MenuListarCombustiveisBaratosPorMunicipio(update: Update, context: CallbackContext):
#     buttons = []
#     r = requests.get('http://localhost:5000/api/v1/CotacaoPosto/RetornarProdutos')
#     resposta = r.json()

#     for combustivel in resposta['data']:
#         tipoComando = "{0}-RetornarPrecosMaisBaratosPorMunicipioProduto".format(combustivel)
#         buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

#     context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Combustiveis disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)  

# Lista o preço de todos os combustiveis por Estado escolhido
def queryHandlerListarCombustiveisBaratos(update: Update, context: CallbackContext, produto: string):
    r = requests.get(f'http://localhost:5000/api/v1/Registro/PrecoMediaASCPorProduto/{produto}')
    resposta = r.json()

    if resposta['status'] == 200:
        respString = (f"<b>TOP 3 combustíveis mais baratos ({produto})</b>\nData da atualização: {DATA_ATUAL}\n")
    
        for resp in resposta['data']:
            respString += "\n<b>Estado:</b> " + resp['estado']
            respString += "\n<b>Municipio:</b> " + resp['municipio']        
            respString += "\n<b>Preço médio de revenda:</b> R$" + str(round(resp['preco_medio_revenda'], 2))
            respString += "\n<b>Número de postos pesquisados: </b>" + str(resp['numero_de_postos_pesquisados'])
            respString += "\n"
    else:
        respString = "Um erro ocorreu, por favor tente novamente."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)

def queryHandlerCombustiveisBaratosPorMunicipioComEndereco(update: Update, context: CallbackContext, municipio: string):
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/CotacaoPosto/RetornarProdutos')
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-ComEndereco-{1}".format(combustivel, municipio)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Combustiveis disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)     

# Handler para identificar a mensagem enviada pelo usuario
def messageHandler(update: Update, context: CallbackContext):

    if update.message.text.lower() != "estados" and update.message.text.lower() != "municipios" and update.message.text.lower() != "combustiveis":
        menu(update, context)

    if "estados".lower() in update.message.text.lower():
        ListarEstados(update, context)

    if "municipios".lower() in update.message.text.lower():
        ListarMunicipios(update, context)

    if "combustiveis".lower() in update.message.text.lower():
        ListarCombustiveis(update, context)

# Lista o preço de todos os combustiveis por Estado escolhido
def queryHandlerEstados(update: Update, context: CallbackContext, estado: string):
    r = requests.get(f'http://localhost:5000/api/v1/Registro/RetornarTodosPrecosPorEstado/{estado}')
    resposta = r.json()

    if resposta['status'] == 200:
        respString = (f"<b>Preço médio de revenda dos combustiveis referentes ao estado do {estado}</b>\nData da atualização: {DATA_ATUAL}\n")

        for resp in resposta['data']:
            respString += "\n<b>Produto:</b> " + resp['produto']
            respString += "\n<b>Preço médio de revenda:</b> R$" + str(round(resp['preco_medio_revenda'], 2))
            respString += "\n"
    else:
        respString = "Um erro ocorreu, por favor tente novamente."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)

# Lista o preço de todos os combustiveis por Municipio escolhido
def queryHandlerMunicipios(update: Update, context: CallbackContext, municipio: string):
    r = requests.get(f'http://localhost:5000/api/v1/Registro/RetornarTodosPrecosPorMunicipio/{municipio}')
    resposta = r.json()

    if resposta['status'] == 200:
        respString = (f"<b>Preço médio de revenda dos combustiveis referentes ao municipio do {municipio}</b>\nData da atualização: {DATA_ATUAL}\n")

        for resp in resposta['data']:
            respString += "\n<b>Produto:</b> " + resp['produto']
            respString += "\n<b>Preço médio de revenda:</b> R$" + str(round(resp['preco_medio_revenda'], 2))
            respString += "\n"
    else:
        respString = "Um erro ocorreu, por favor tente novamente."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)

# Lista o preço de todos os Combustiveis por estado, de acordo com o Combustivel escolhido
def queryHandlerCombustiveisPorMunicipio(update: Update, context: CallbackContext, municipio: string): # COMBUSTIVEIS E MUNICIPIO
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarProdutos')
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-PrecosByM-{1}".format(combustivel, municipio)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Combustiveis disponíveis para a consulta no municipio de {0}</b>".format(municipio), parse_mode=telegram.constants.PARSEMODE_HTML)  

def queryHandlerCombustiveisPorEstado(update: Update, context: CallbackContext, estado: string): # COMBUSTIVEIS E MUNICIPIO
    buttons = []
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarProdutos')
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-PrecosByE-{1}".format(combustivel, estado)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Combustiveis disponíveis para a consulta no estado de {0}</b>".format(estado), parse_mode=telegram.constants.PARSEMODE_HTML)  

def RetornarTodosPrecosPorMunicipio(update: Update, context: CallbackContext, produto: string, municipio: string): # COMBUSTIVEIS E MUNICIPIO    
    r = requests.get(f'http://localhost:5000/api/v1/Registro/RetornarTodosPrecosPorMunicipio/{municipio}/{produto}')
    resposta = r.json()

    if resposta['status'] == 200:
        respString = (f"<b>Preço médio de revenda dos combustiveis referentes ao municipio do {municipio} no estado de {resposta['data'][0]['dados'][0]['estado']}</b>\n")    
        respString += "\n<b>Produto escolhido:</b> " + resposta['data'][0]['dados'][0]['produto']
        respString += "\n<b>Preço médio de revenda:</b> R$ " + str(round(resposta['data'][0]['average'], 2))
        respString += "\n<b>Data da atualização:</b> {0}".format(DATA_ATUAL)
    else:
        respString = "Um erro ocorreu, por favor tente novamente."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)

def RetornarTodosPrecosPorMunicipioComEndereco(update: Update, context: CallbackContext, produto: string, municipio: string): # COMBUSTIVEIS E MUNICIPIO    
    r = requests.get(f'http://localhost:5000/api/v1/CotacaoPosto/PostosMaisBaratosPorMunicipio/{produto}/{municipio}')
    resposta = r.json()
    i = 1

    if resposta['status'] == 200:
        respString = (f"<b>TOP 3 postos com o combustível ({produto}) mais barato no municipio de {municipio}</b>\nData da atualização: {DATA_ATUAL}\n")

        for resp in resposta['data']:
            respString += "\n<b>POSTO " + str(i) + "</b>"        
            respString += "\n<b>Endereço:</b> Rua " + resp['nome_rua'] + ", N° " + resp['numero_rua'] + ", Bairro " + resp['bairro_endereco']
            respString += "\n<b>Municipio:</b> " + resp['municipio_endereco']
            respString += "\n<b>Bandeira do posto:</b> " + resp['bandeira_posto']
            respString += "\n<b>Cotação:</b> R$" + str(round(resp['cotacao_produto_posto'], 2))
            respString += "\n"
            i += 1
    else:
        respString = "Um erro ocorreu, por favor tente novamente."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)    

def RetornarTodosPrecosPorEstado(update: Update, context: CallbackContext, produto: string, estado: string): # COMBUSTIVEIS E MUNICIPIO    
    r = requests.get(f'http://localhost:5000/api/v1/Registro/RetornarTodosPrecosPorEstado/{estado}/{produto}')
    resposta = r.json()

    if resposta['status'] == 200:
        respString = (f"<b>Preço médio de revenda dos combustiveis referentes ao estado de {estado}</b>\n")    
        respString += "\n<b>Produto escolhido:</b> " + resposta['data'][0]['dados'][0]['produto']
        respString += "\n<b>Preço médio de revenda:</b> R$ " + str(round(resposta['data'][0]['average'], 2))
        respString += "\n<b>Data da atualização:</b> {0}".format(DATA_ATUAL)
    else:
        respString = "Um erro ocorreu, por favor tente novamente."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)    


# Pergunta se o usuario deseja mostrar o menu novamente
def msgAvaliacao(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("1 ⭐", callback_data="1-nota")],
        [InlineKeyboardButton("2 ⭐⭐", callback_data="2-nota")],
        [InlineKeyboardButton("3 ⭐⭐⭐", callback_data="3-nota")],
        [InlineKeyboardButton("4 ⭐⭐⭐⭐", callback_data="4-nota")],
        [InlineKeyboardButton("5 ⭐⭐⭐⭐⭐", callback_data="5-nota")]]
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Por favor escolha uma nota de <b>1 a 5</b>", parse_mode=telegram.constants.PARSEMODE_HTML)

# def msgMaisBaratos(update: Update, context: CallbackContext):
#     buttons = [[InlineKeyboardButton("Combustível", callback_data="combustiveisBaratos-listar")],
#         [InlineKeyboardButton("Município", callback_data="municipiosBaratos-listar")]]
#     context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Deseja realizar a consulta por combustível ou estado?", parse_mode=telegram.constants.PARSEMODE_HTML)


def queryHandlerAvaliar(update: Update, context: CallbackContext, nota: int):
    userTelegramID = update.callback_query.from_user.id

    objAvaliacao = {'idUsuarioTelegram': str(userTelegramID),
                    'data' : DATA_ATUAL,
                    'nota' : nota,
                    'descricao' : ''}

    r = requests.post('http://localhost:5000/api/v1/Avaliacao', json = objAvaliacao)
    resposta = r.json()

    nota = resposta['nota']

    context.bot.send_message(chat_id=update.effective_chat.id, text=(f"A sua avaliação de nota {nota} foi registrada com sucesso. Agradecemos a sua opinião!"), parse_mode=telegram.constants.PARSEMODE_HTML)

def verificarSeJaAvaliou(update: Update, context: CallbackContext):
    userTelegramID = update.callback_query.from_user.id

    r = requests.get(f'http://localhost:5000/api/v1/Avaliacao/{userTelegramID}')
    resposta = r.json()    

    if resposta['status'] == 404:
        return False
    else:
        return True        

# Handler das querys (opções clicaveis)
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
        elif arg1 == "combustiveisBaratos":
            MenuListarCombustiveisBaratos(update, context)        
        elif arg1 == "combustiveisBaratosPorMunicipio":
            ListarMunicipiosCotacaoPosto(update, context)            
        elif arg1 == "menu":
            menu(update, context)

    elif tipoComando == "estado": # Caso seja um ESTADO  
        queryHandlerCombustiveisPorEstado(update, context, arg1)

    elif tipoComando == "municipio": # Caso seja um MUNICIPIO        
        queryHandlerCombustiveisPorMunicipio(update, context, arg1)            

    elif tipoComando == "BaratosComEnd": # Caso seja um COMBUSTIVEL
        queryHandlerCombustiveisBaratosPorMunicipioComEndereco(update, context, arg1)        

    elif tipoComando == "combustiveisBaratos": # Caso seja um COMBUSTIVEL
        queryHandlerListarCombustiveisBaratos(update, context, arg1)
        menu(update, context)

    elif tipoComando == "municipiosBaratos": # Caso seja um COMBUSTIVEL
        queryHandlerListarMunicipiosBaratos(update, context, arg1)
        menu(update, context)

    elif tipoComando == "combustiveis": # Caso seja para avaliar o bot
        # arg3 = query[2]
        # queryHandlerCombustiveis(update, context, arg1)
        menu(update, context)

    elif tipoComando == "avaliar": # Caso seja para avaliar o bot
        msgAvaliacao(update, context)        

    elif tipoComando == "PrecosByM":
        arg3 = query[2]
        RetornarTodosPrecosPorMunicipio(update, context, arg1, arg3)
        menu(update, context)

    elif tipoComando == "PrecosByE":
        arg3 = query[2]
        RetornarTodosPrecosPorEstado(update, context, arg1, arg3)
        menu(update, context)

    elif tipoComando == "ComEndereco":
        arg3 = query[2]
        RetornarTodosPrecosPorMunicipioComEndereco(update, context, arg1, arg3)
        menu(update, context)
    
    elif tipoComando == "nota": # Caso seja para dar a nota de 1 a 5 para o bot        
        if verificarSeJaAvaliou(update, context) == False:
            queryHandlerAvaliar(update, context, arg1)
            menu(update, context)
        else:            
            context.bot.send_message(chat_id=update.effective_chat.id, text="Você já deu a sua nota para nós, não é permitido mais de uma nota por usuário.", parse_mode=telegram.constants.PARSEMODE_HTML)
            menu(update, context)

dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))

updater.start_polling()