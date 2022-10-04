import telebot
import requests
import json

Chave_API = "5449080279:AAEMmhTKME9SZXpDUTn2jSQHbpwsc6uTQGg"

bot = telebot.TeleBot(Chave_API)

RETORNARFILTRADO_LEN = 18 # '/RetornarFiltrado '

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
    print(resposta)    
    respString = "Seus filtros:"
    respString += "\nEstado: " + resposta['estado']
    respString += "\nMunicipio: " + resposta['municipio']
    respString += "\nProduto: " + resposta['produto']
    respString += "\n"
    respString += "\nPreços:"
    respString += "\nPreço médio de revenda: " + str(resposta['preco_medio_revenda'])
    respString += "\nPreço minímo de revenda: " + str(resposta['preco_minimo_revenda'])
    respString += "\nPreço máximo de revenda: " + str(resposta['preco_maximo_revenda'])    
    
    bot.send_message(mensagem.chat.id, respString)

#Comando de /RetornarMunicipios
@bot.message_handler(commands=["RetornarMunicipios"])
def responder(mensagem):
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarMunicipios')
    resposta = r.json()
    print(type(resposta))
    strResp = "Lista de Municípios disponíveis para consulta:\n\n"

    for c in resposta:
        strResp += c + "\n"
    
    bot.send_message(mensagem.chat.id, strResp)

#Comando de /RetornarEstados
@bot.message_handler(commands=["RetornarEstados"])
def responder(mensagem):
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarEstados')
    resposta = r.json()
    print(type(resposta))
    strResp = "Lista de Estados disponíveis para consulta:\n\n"

    for c in resposta:
        strResp += c + "\n"
    
    bot.send_message(mensagem.chat.id, strResp)

#Comando de /RetornarCombustiveis
@bot.message_handler(commands=["RetornarCombustiveis"])
def responder(mensagem):
    r = requests.get('http://localhost:5000/api/v1/Registro/RetornarProdutos')
    resposta = r.json()
    print(type(resposta))
    strResp = "Lista de Combustiveis disponíveis para consulta:\n\n"

    for c in resposta:
        strResp += c + "\n"
    
    bot.send_message(mensagem.chat.id, strResp)







#Adicionar antes desse bloco abaixo todos os comandos
def verificar(mensagem):
    return True

@bot.message_handler(func=verificar) #Só vai retornar caso a func "verificar" retornar True
def responder(mensagem):
    texto = """Escolha uma opção para continuar (Clique no item desejado):
    \n/RetornarMunicipios - Para retornar todos os municipios disponíveis para consulta.
    \n/RetornarEstados - Para retornar todos os estados disponíveis para consulta.
    \n/RetornarCombustiveis - Para retornar todos os combustiveis disponíveis para consulta.
    \n/RetornarFiltrado ESTADO/MUNICIPIO/COMBUSTIVEL - Para retornar todas as informações de combustivel de maneira filtrada.    
    \nResponder qualquer outra coisa não vai funcionar, clique em uma das opções ou digite /menu para ver esse menu sempre que desejar."""
    bot.reply_to(mensagem, texto)

bot.polling()