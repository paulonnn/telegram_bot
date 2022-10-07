import telebot
import requests
import datetime
import json

Chave_API = "5449080279:AAEMmhTKME9SZXpDUTn2jSQHbpwsc6uTQGg"

bot = telebot.TeleBot(Chave_API)

RETORNARFILTRADO_LEN = 18 # '/RetornarFiltrado '
RETORNARPRECOSPORESTADO_LEN = 25 # '/RetornarPrecosPorEstado '
RETORNARTODOSPRECOSPORESTADO_LEN = 30 #

DATA_ATT = datetime.date.today().strftime("%d/%m/%Y")

#Comando de /RetornarFiltrado
@bot.message_handler(commands=["RetornarFiltrado"])
def responder(mensagem):
    msg_text = mensagem.text[RETORNARFILTRADO_LEN:]
    if msg_text == "":
        msg_text = "Favor inserir todos os parâmetros necessários: /RetornarFiltrado ESTADO/MUNICIPIO/COMBUSTIVEL"
        return bot.send_message(mensagem.chat.id, msg_text)
    
    parametros = msg_text.split('/')

    estado = parametros[0].upper()
    municipio = parametros[1].upper()
    produto = parametros[2].upper()

    #Request
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarFiltrado/{0}/{1}/{2}'.format(estado, municipio, produto))
    resposta = r.json()    
    respString = "Seus filtros:"
    respString += "\nEstado: " + resposta['estado']
    respString += "\nMunicipio: " + resposta['municipio']
    respString += "\nProduto: " + resposta['produto']
    respString += "\n"
    respString += "\nPreços:"
    respString += "\nPreço médio de revenda: R$" + str(resposta['preco_medio_revenda'])
    respString += "\nPreço minímo de revenda: R$" + str(resposta['preco_minimo_revenda'])
    respString += "\nPreço máximo de revenda: R$" + str(resposta['preco_maximo_revenda'])
    respString += "\nData da atualização dos preços: " + DATA_ATT
    
    bot.send_message(mensagem.chat.id, respString)

#Comando de /RetornarMunicipios
@bot.message_handler(commands=["RetornarMunicipios"])
def responder(mensagem):
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarMunicipios')
    resposta = r.json()    
    strResp = "Lista de Municípios disponíveis para consulta:\n\n"

    for c in resposta:
        strResp += c + "\n"
    
    print(resposta)
    strResp += "\nData da atualização: " + DATA_ATT
    bot.send_message(mensagem.chat.id, strResp)

#Comando de /RetornarEstados
@bot.message_handler(commands=["RetornarEstados"])
def responder(mensagem):
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarEstados')
    resposta = r.json()    
    strResp = "Lista de Estados disponíveis para consulta:\n\n"

    for c in resposta:
        strResp += c + "\n"
    
    print(resposta)
    strResp += "\nData da atualização: " + DATA_ATT
    bot.send_message(mensagem.chat.id, strResp)

#Comando de /RetornarCombustiveis
@bot.message_handler(commands=["RetornarCombustiveis"])
def responder(mensagem):
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarProdutos')
    resposta = r.json()    
    strResp = "Lista de Combustiveis disponíveis para consulta:\n\n"

    for c in resposta:
        strResp += c + "\n"
    
    strResp += "\nData da atualização: " + DATA_ATT
    bot.send_message(mensagem.chat.id, strResp)

#Comando de /RetornarPrecosPorEstado
@bot.message_handler(commands=["RetornarPrecosPorEstado"])
def responder(mensagem):
    msg_text = mensagem.text[RETORNARPRECOSPORESTADO_LEN:]
    if msg_text == "":
        msg_text = "Favor inserir todos os parâmetros necessários: /RetornarPrecosPorEstado COMBUSTIVEL"
        return bot.send_message(mensagem.chat.id, msg_text)

    combustivel = msg_text.upper()    

    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarPrecosPorEstados/{0}'.format(combustivel))
    resposta = r.json()    
    respString = "Preço médio de revenda do {0} por estado\n\n".format(combustivel)

    for r in resposta:
        respString += "\nEstado: " + r['estado']    
        respString += "\nProduto: " + r['produto']
        respString += "\nPreço médio de revenda: R$" + str(r['preco_medio_revenda'])
        respString += "\n"
    
    respString += "\nData da atualização dos preços: " + DATA_ATT
    bot.send_message(mensagem.chat.id, respString)

#Comando de /RetornarTodosPrecosPorEstado
@bot.message_handler(commands=["RetornarTodosPrecosPorEstado"])
def responder(mensagem):
    msg_text = mensagem.text[RETORNARTODOSPRECOSPORESTADO_LEN:]
    if msg_text == "":
        msg_text = "Favor inserir todos os parâmetros necessários: /RetornarTodosPrecosPorEstado ESTADO"
        return bot.send_message(mensagem.chat.id, msg_text)

    estado = msg_text.upper()    

    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarTodosPrecosPorEstado/{0}'.format(estado))
    resposta = r.json()          
    respString = "Preço médio de revenda dos combustiveis referentes ao estado de {0}\n\n".format(estado)

    for r in resposta:        
        respString += "\nProduto: " + r['produto']                
        respString += "\nPreço médio de revenda: R$" + str(r['preco_medio_revenda'])
        respString += "\n"
    
    respString += "\nData da atualização dos preços: " + DATA_ATT
    bot.send_message(mensagem.chat.id, respString)    







#Adicionar antes desse bloco abaixo todos os comandos
def verificar(mensagem):
    return True

@bot.message_handler(func=verificar) #Só vai retornar caso a func "verificar" retornar True
def responder(mensagem):
    texto = """Bem-vindo ao Gasolina Bot!\nEscolha uma opção para continuar (Clique no item desejado):
    \n/RetornarMunicipios - Para retornar todos os municipios disponíveis para consulta.
    \n/RetornarEstados - Para retornar todos os estados disponíveis para consulta.
    \n/RetornarCombustiveis - Para retornar todos os combustiveis disponíveis para consulta.
    \n/RetornarFiltrado ESTADO/MUNICIPIO/COMBUSTIVEL - Para retornar todas as informações de combustivel de maneira filtrada.
    \n/RetornarPrecosPorEstado COMBUSTIVEL - Para retornar todas os preços médios de revenda do combustivel escolhido por estado.
    \n/RetornarTodosPrecosPorEstado ESTADO - Para retornar todas os preços médios de revenda dos combustiveis por estado.
    \n\nResponder qualquer outra coisa não vai funcionar, clique em uma das opções ou digite /menu para ver esse menu sempre que desejar."""
    bot.reply_to(mensagem, texto)

bot.polling()