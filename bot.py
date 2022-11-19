import requests
import time
import json
import os
#Ler as mensagens que estao chegando
# while True:
#     token = "5646362143:AAHdx8pPwxlJ9-vNcEcJZ0KHMblCEWTHL2g"
#     url_base = f"https://api.telegram.org/bot{token}/getUpdates"
#     response = requests.get(url_base)
#     print(response.json())
#     time.sleep(10)

class TelegramBot:
    def __init__(self):
        print("Iniciando o bot")
        token = "5787455269:AAHeom_PmlWUL5jgeiiLkxOPN1Y9ycCjQfc"
        self.url_base = f"https://api.telegram.org/bot{token}/"
        self.menu_level = ""
        
    #Iniciar o bot
    def Iniciar(self):
        update_id = None
        self.menu_level = "menu"
        while True:
            atualizacao = self.obter_mensagens(update_id)
            mensagens = atualizacao["result"]            
            if mensagens:
                for mensagem in mensagens:                    
                    nome = mensagem["message"]["from"]["first_name"]
                    update_id = mensagem["update_id"]
                    chat_id = mensagem["message"]["from"]["id"]
                    eh_primeira_mensagem = mensagem["message"]["message_id"] == 1   
                    resposta = self.criar_resposta(mensagem,nome, eh_primeira_mensagem)
                    self.responder(resposta,chat_id)
    #Obter mensagens
    
    def obter_mensagens(self, update_id):
        link_requisicao = f"{self.url_base}getUpdates?timeout=100"
        if update_id:
            link_requisicao = f"{link_requisicao}&offset={update_id + 1}"
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)
    
    #criar uma resposta
    def criar_resposta(self, mensagem, nome, eh_primeira_mensagem):
        mensagem = mensagem["message"]["text"]
        print(self.menu_level)
        
        if eh_primeira_mensagem == True or mensagem .lower() == "menu" or "bom dia":
        #if eh_primeira_mensagem == True :            
            return f'''Olá, {nome} seja bem vindo a nossa clininca. oque deseja fazer?
            {os.linesep}1- Agendar uma consulta{os.linesep}2- Cancelar uma consulta{os.linesep}3- Verificar uma consulta'''
        
        #if self.menu_level == "menu":
        if mensagem == '1':
            self.menu_level = "agendar"
            #print(self.menu_level)
            return "Digite o dia da consulta"
        if mensagem == '2':
            return "Digite o dia da consulta que deseja cancelar"        
        
        if self.menu_level == "agendar":
            self.menu_level = "menu"
            return f"Consulta marcada para o dia {mensagem}"
    
    #responder
    def responder(self, resposta, chat_id):
        #enviar
        link_de_envio = f"{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}"
        requests.get(link_de_envio)

bot = TelegramBot()
bot.Iniciar()