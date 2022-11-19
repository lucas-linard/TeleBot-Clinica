import telebot
from telebot import types
import json
from datetime import date, timedelta
from random import randrange


CHAVE_API = "5787455269:AAHeom_PmlWUL5jgeiiLkxOPN1Y9ycCjQfc"

bot = telebot.TeleBot(CHAVE_API)
user_text = ""
# @bot.message_handler(commands=["pizza"])
# def pizza(mensagem):
#     bot.send_message(mensagem.chat.id, "Saindo a pizza pra sua casa: Tempo de espera em 20min")

# @bot.message_handler(commands=["hamburguer"])
# def hamburguer(mensagem):
#     bot.send_message(mensagem.chat.id, "Saindo o Brabo: em 10min chega ai")

# @bot.message_handler(commands=["salada"])
# def salada(mensagem):
#     bot.send_message(mensagem.chat.id, "Não tem salada não, clique aqui para iniciar: /iniciar")
def write_json(data, filename='bd.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)    
# with open('bd.json') as json_file:
#     data = json.load(json_file)
#     print(data)    

@bot.message_handler(commands=["MarcarConsulta"])
def opcao1(mensagem):
    texto = """
    Qual é a sua necessidade? (Clique em uma opção)
    /ClinicoGeral Clinico Geral
    """
    bot.send_message(mensagem.chat.id, texto)    
    user_text = mensagem.text
    #write_json(mensagem)
    bot.register_next_step_handler(mensagem, EscolherClinicoGeral)
    
def EscolherClinicoGeral(mensagem):    
    with open('bd.json') as json_file:
        data = json.load(json_file)
        data = data["medicos"]
        texto = f"""
        Escolha um medico disponivel de sua preferencia! (Clique em uma opção)
        /1 - {data[0]["name"]}
        /2 - {data[1]["name"]}
        /3 - {data[2]["name"]}
        """        
        # markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        # markup.add(data[0]["name"], data[1]["name"], data[2]["name"])
        # msg = bot.reply_to(mensagem, 'What is your gender', reply_markup=markup)        
        bot.send_message(mensagem.chat.id, texto)
        bot.register_next_step_handler(mensagem, EscolherDiaClinicoGeral)

def EscolherDiaClinicoGeral(mensagem):        
    dia =  date.today() 
    texto = f"""
    Qual dos dias disponiveis você deseja marcar a consulta?
    /1 - {(dia).strftime("%d/%m/%Y")}
    /2 - {(dia + timedelta(days=randrange(30))).strftime("%d/%m/%Y")}
    /4 - {(dia + timedelta(days=randrange(40))).strftime("%d/%m/%Y")}
    /5 - {(dia + timedelta(days=randrange(50))).strftime("%d/%m/%Y")}
    /6 - {(dia + timedelta(days=randrange(70))).strftime("%d/%m/%Y")}
    """
    bot.send_message(mensagem.chat.id, texto)
    bot.register_next_step_handler(mensagem, EscolherHorarioClinicoGeral)

def EscolherHorarioClinicoGeral(mensagem):    
    texto = """
    Qual horario você deseja marcar a consulta?
    /1 - 08:00
    /2 - 08:30
    /3 - 9:00
    /4 - 9:30
    /5 - 10:00
    """
    bot.send_message(mensagem.chat.id, texto)
    bot.register_next_step_handler(mensagem, EscolherClinicoGeral)

def confirmarClinico(mensagem): 
    texto = """
    Confirma a consulta?
    /1 - Sim
    /2 - Não
    """
    bot.send_message(mensagem.chat.id, texto)
    bot.register_next_step_handler(mensagem, EscolherClinicoGeral)



def verificar(mensagem):    
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):            
    texto = f"""
    Olá {mensagem.from_user.first_name},escolha uma opção para continuar (Clique no item):
     /MarcarConsulta Marcar consulta com um médico
     /ReagendarConsulta Reagendar consulta
     /VisualizarConsulta Visualizar consulta
     /CancelarConsulta Mandar um abraço pro Lira
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)

bot.polling()