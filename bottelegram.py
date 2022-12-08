from asyncore import dispatcher
import string
from telegram import *
import telegram
from telegram.ext import *
import requests
from datetime import date

DATA_ATUAL = date.today().strftime("%d/%m/%Y")

updater = Updater(token="TOKEN_DO_BOT_AQUI")
dispatcher = updater.dispatcher

def menu(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("Pesquisar por Municipios", callback_data="municipios-listar")],
        [InlineKeyboardButton("Pesquisar por Estados", callback_data="estados-listar")],        
        [InlineKeyboardButton("Postos mais baratos (por combustível)", callback_data="combustiveisBaratos-listar")],
        [InlineKeyboardButton("Verificar endereço dos postos mais baratos (por municipio e combustível)", callback_data="combustiveisBaratosPorMunicipio-listar")],
        [InlineKeyboardButton("Avaliar o BOT", callback_data="opcao-avaliar")]]
    texto = "<b>Bem-vindo ao Gasolina Bot!</b>\n\nAqui você pode obter informações sobre as cotações de combustíveis por estado e município.\n\nEscolha uma opção para continuar (<b><i>Clique</i></b> no item desejado):"
    return context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text=texto, parse_mode=telegram.constants.PARSEMODE_HTML)

def menuNovamente(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("Pesquisar por Municipios", callback_data="municipios-listar")],
        [InlineKeyboardButton("Pesquisar por Estados", callback_data="estados-listar")],        
        [InlineKeyboardButton("Postos mais baratos (por combustível)", callback_data="combustiveisBaratos-listar")],
        [InlineKeyboardButton("Verificar endereço dos postos mais baratos (por municipio e combustível)", callback_data="combustiveisBaratosPorMunicipio-listar")],
        [InlineKeyboardButton("Avaliar o BOT", callback_data="opcao-avaliar")]]
    texto = "Escolha uma opção para continuar (<b><i>Clique</i></b> no item desejado):"
    return context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text=texto, parse_mode=telegram.constants.PARSEMODE_HTML)

def iniciarCommand(update: Update, context: CallbackContext):
    menu(update, context)

def ListarEstados(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('https://localhost:7106/api/v1/Registro/RetornarEstados', verify=False)
    resposta = r.json()

    for estado in resposta['data']:
        tipoComando = "{0}-estado".format(estado)
        buttons.append([InlineKeyboardButton(estado, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Estados disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)

def ListarMunicipios(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('https://localhost:7106/api/v1/Registro/RetornarMunicipios', verify=False)
    resposta = r.json()

    for municipio in resposta['data']:
        tipoComando = "{0}-municipio".format(municipio)
        buttons.append([InlineKeyboardButton(municipio, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Clique no municipio para o qual deseja realizar a consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)

def ListarMunicipiosCotacaoPosto(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('https://localhost:7106/api/v1/CotacaoPosto/RetornarMunicipios', verify=False)
    resposta = r.json()

    for municipio in resposta['data']:
        tipoComando = "{0}-BaratosComEnd".format(municipio)
        buttons.append([InlineKeyboardButton(municipio, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Clique no municipio para o qual deseja realizar a consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)    

def ListarCombustiveis(update: Update, context: CallbackContext, municipio: string):
    buttons = []
    r = requests.get('https://localhost:7106/api/v1/Registro/RetornarProdutos', verify=False)
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-combustiveis-{1}".format(combustivel, municipio)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Combustiveis disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)  

def MenuListarMunicipiosBaratos(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('https://localhost:7106/api/v1/Registro/RetornarMunicipios', verify=False)
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-municipiosBaratos".format(combustivel)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Clique no municipio para o qual deseja realizar a consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)  

def MenuListarCombustiveisBaratos(update: Update, context: CallbackContext):
    buttons = []
    r = requests.get('https://localhost:7106/api/v1/Registro/RetornarProdutos', verify=False)
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-combustiveisBaratos".format(combustivel)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Combustiveis disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)  

def queryHandlerListarCombustiveisBaratos(update: Update, context: CallbackContext, produto: string):
    r = requests.get(f'https://localhost:7106/api/v1/Registro/PrecoMediaASCPorProduto/{produto}', verify=False)
    resposta = r.json()    

    if resposta['status'] == 200:
        data_tratada = resposta['data'][0]['data']
        respString = (f"<b>TOP 3 combustíveis mais baratos ({produto})\nData da atualização:</b> {TratarData(data_tratada)}\n")
    
        for resp in resposta['data']:
            respString += "\n<b>Estado:</b> " + resp['estado']
            respString += "\n<b>Municipio:</b> " + resp['municipio']        
            respString += "\n<b>Preço médio de revenda:</b> R$" + str(round(resp['preco_medio_revenda'], 2))
            respString += "\n<b>Número de postos pesquisados: </b>" + str(resp['numero_de_postos_pesquisados'])
            respString += "\n"
    else:
        respString = "Infelizmente não existem dados disponíveis para esta consulta."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)

def queryHandlerCombustiveisBaratosPorMunicipioComEndereco(update: Update, context: CallbackContext, municipio: string):
    buttons = []
    r = requests.get('https://localhost:7106/api/v1/CotacaoPosto/RetornarProdutos', verify=False)
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-ComEndereco-{1}".format(combustivel, municipio)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Lista de Combustiveis disponíveis para consulta</b>", parse_mode=telegram.constants.PARSEMODE_HTML)     

def messageHandler(update: Update, context: CallbackContext):    
    menu(update, context)

def queryHandlerCombustiveisPorMunicipio(update: Update, context: CallbackContext, municipio: string):
    buttons = []
    r = requests.get('https://localhost:7106/api/v1/Registro/RetornarProdutos', verify=False)
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-PrecosByM-{1}".format(combustivel, municipio)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Clique no combustível para o qual deseja realizar a consulta no município de {0}</b>".format(municipio), parse_mode=telegram.constants.PARSEMODE_HTML)  

def queryHandlerCombustiveisPorEstado(update: Update, context: CallbackContext, estado: string):
    buttons = []
    r = requests.get('https://localhost:7106/api/v1/Registro/RetornarProdutos', verify=False)
    resposta = r.json()

    for combustivel in resposta['data']:
        tipoComando = "{0}-PrecosByE-{1}".format(combustivel, estado)
        buttons.append([InlineKeyboardButton(combustivel, callback_data=tipoComando)])

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="<b>Clique no combustível para o qual deseja realizar a consulta no estado de {0}</b>".format(estado), parse_mode=telegram.constants.PARSEMODE_HTML)  

def RetornarTodosPrecosPorMunicipio(update: Update, context: CallbackContext, produto: string, municipio: string):   
    r = requests.get(f'https://localhost:7106/api/v1/Registro/RetornarTodosPrecosPorMunicipio/{municipio}/{produto}', verify=False)
    resposta = r.json()

    if resposta['status'] == 200:
        data_tratada = resposta['data'][0]['dados'][0]['data']
        respString = (f"<b>Preço médio de revenda do combustivel {resposta['data'][0]['dados'][0]['produto']} referente ao municipio do {municipio} no estado de {resposta['data'][0]['dados'][0]['estado']}</b>\n")    
        respString += "\n<b>Município escolhido:</b> " + municipio
        respString += "\n<b>Produto escolhido:</b> " + resposta['data'][0]['dados'][0]['produto']
        respString += "\n<b>Preço médio de revenda:</b> R$ " + str(round(resposta['data'][0]['average'], 2))
        respString += "\n\n<b>Data da atualização:</b> {0}".format(TratarData(data_tratada))
    else:
        respString = "Infelizmente não existem dados disponíveis para esta consulta."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)

def TratarData(data_cotacao: string):
    data_split = data_cotacao.split("-")
    data_tratada = ""
    data_tratada = data_tratada + data_split[2] + "/" + data_split[1] + "/" + data_split[0];
    return data_tratada;
    

def RetornarTodosPrecosPorMunicipioComEndereco(update: Update, context: CallbackContext, produto: string, municipio: string): # COMBUSTIVEIS E MUNICIPIO    
    r = requests.get(f'https://localhost:7106/api/v1/CotacaoPosto/PostosMaisBaratosPorMunicipio/{produto}/{municipio}', verify=False)
    resposta = r.json()
    i = 1
    varNumero = ""    

    if resposta['status'] == 200:
        data_tratada = TratarData(resposta['data'][0]['data_cotacao'])
        respString = (f"<b>TOP 3 postos com o combustível ({produto}) mais barato no municipio de {municipio}</b>\n<b>Data da atualização:</b> {data_tratada}\n")

        for resp in resposta['data']:
            varNumero = resp['numero_rua']
            if varNumero == "SN" or varNumero == "S/N" or varNumero == None:
                varNumero = "(Sem Número)"

            respString += "\n<b>POSTO " + str(i) + "</b>"        
            respString += "\n<b>Endereço:</b> Rua " + resp['nome_rua'] + ", N° " + varNumero + ", Bairro " + resp['bairro_endereco']
            respString += "\n<b>Municipio:</b> " + resp['municipio_endereco']
            respString += "\n<b>CEP:</b> " + str(resp['cep_endereco'])
            respString += "\n<b>Bandeira do posto:</b> " + resp['bandeira_posto']
            respString += "\n<b>Cotação:</b> R$" + str(round(resp['cotacao_produto_posto'], 2))
            respString += "\n"
            i += 1
    else:
        respString = "Infelizmente não existem dados disponíveis para esta consulta."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)    

def RetornarTodosPrecosPorEstado(update: Update, context: CallbackContext, produto: string, estado: string):
    r = requests.get(f'https://localhost:7106/api/v1/Registro/RetornarTodosPrecosPorEstado/{estado}/{produto}', verify=False)
    resposta = r.json()    

    if resposta['status'] == 200:
        data_tratada = resposta['data'][0]['dados'][0]['data']
        respString = (f"<b>Preço médio de revenda dos combustiveis referentes ao estado de {estado}\n</b>")    
        respString += "\n<b>Estado escolhido:</b> " + estado
        respString += "\n<b>Produto escolhido:</b> " + resposta['data'][0]['dados'][0]['produto']
        respString += "\n<b>Preço médio de revenda:</b> R$ " + str(round(resposta['data'][0]['average'], 2))
        respString += "\n\n<b>Data da atualização:</b> {0}".format(TratarData(data_tratada))
    else:
        respString = "Infelizmente não existem dados disponíveis para esta consulta."

    context.bot.send_message(chat_id=update.effective_chat.id, text=respString, parse_mode=telegram.constants.PARSEMODE_HTML)    


def msgAvaliacao(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("1 ⭐", callback_data="1-nota")],
        [InlineKeyboardButton("2 ⭐⭐", callback_data="2-nota")],
        [InlineKeyboardButton("3 ⭐⭐⭐", callback_data="3-nota")],
        [InlineKeyboardButton("4 ⭐⭐⭐⭐", callback_data="4-nota")],
        [InlineKeyboardButton("5 ⭐⭐⭐⭐⭐", callback_data="5-nota")]]
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text="Por favor escolha uma nota de <b>1 a 5</b>", parse_mode=telegram.constants.PARSEMODE_HTML)


def queryHandlerAvaliar(update: Update, context: CallbackContext, nota: int):
    userTelegramID = update.callback_query.from_user.id

    objAvaliacao = {'idUsuarioTelegram': str(userTelegramID),
                    'data' : DATA_ATUAL,
                    'nota' : nota,
                    'descricao' : ''}

    r = requests.post('https://localhost:7106/api/v1/Avaliacao', json = objAvaliacao, verify=False)
    resposta = r.json()

    nota = resposta['nota']

    context.bot.send_message(chat_id=update.effective_chat.id, text=(f"A sua avaliação de nota {nota} foi registrada com sucesso. Agradecemos a sua opinião!"), parse_mode=telegram.constants.PARSEMODE_HTML)

def verificarSeJaAvaliou(update: Update, context: CallbackContext):
    userTelegramID = update.callback_query.from_user.id

    r = requests.get(f'https://localhost:7106/api/v1/Avaliacao/{userTelegramID}', verify=False)
    resposta = r.json()    

    if resposta['status'] == 404:
        return False
    else:
        return True        

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

    elif tipoComando == "estado":
        queryHandlerCombustiveisPorEstado(update, context, arg1)

    elif tipoComando == "municipio":
        queryHandlerCombustiveisPorMunicipio(update, context, arg1)            

    elif tipoComando == "BaratosComEnd":
        queryHandlerCombustiveisBaratosPorMunicipioComEndereco(update, context, arg1)        

    elif tipoComando == "combustiveisBaratos":
        queryHandlerListarCombustiveisBaratos(update, context, arg1)
        menuNovamente(update, context)    

    elif tipoComando == "combustiveis":        
        menuNovamente(update, context)

    elif tipoComando == "avaliar":
        msgAvaliacao(update, context)        

    elif tipoComando == "PrecosByM":
        arg3 = query[2]
        RetornarTodosPrecosPorMunicipio(update, context, arg1, arg3)
        menuNovamente(update, context)

    elif tipoComando == "PrecosByE":
        arg3 = query[2]
        RetornarTodosPrecosPorEstado(update, context, arg1, arg3)
        menuNovamente(update, context)

    elif tipoComando == "ComEndereco":
        arg3 = query[2]
        RetornarTodosPrecosPorMunicipioComEndereco(update, context, arg1, arg3)
        menuNovamente(update, context)
    
    elif tipoComando == "nota":
        if verificarSeJaAvaliou(update, context) == False:
            queryHandlerAvaliar(update, context, arg1)
            menuNovamente(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Você já deu a sua nota para nós, não é permitido mais de uma nota por usuário.", parse_mode=telegram.constants.PARSEMODE_HTML)
            menuNovamente(update, context)

dispatcher.add_handler(CommandHandler("iniciar", iniciarCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(CallbackQueryHandler(queryHandler))

updater.start_polling()