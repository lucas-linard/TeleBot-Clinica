import telebot
from telebot import types
import json
from datetime import date, timedelta
from random import randrange


CHAVE_API = "5787455269:AAHeom_PmlWUL5jgeiiLkxOPN1Y9ycCjQfc"

bot = telebot.TeleBot(CHAVE_API)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.id = None
        self.medico = None
        self.data = None
        self.hora = None


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
    chat_id = mensagem.chat.id
    name = mensagem.from_user.first_name
    user = User(name)
    user_dict[chat_id] = user
    texto = """
    Qual é a sua necessidade? (Clique em uma opção)
    /ClinicoGeral Clinico Geral
    """
    msg = bot.reply_to(mensagem, texto)        
    #write_json(mensagem)
    bot.register_next_step_handler(msg, EscolherClinicoGeral)
    
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
        bot.reply_to(mensagem, texto)
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
    chat_id = mensagem.chat.id
    medico = mensagem.text
    user = user_dict[chat_id]
    user.medico = medico
    
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
    chat_id = mensagem.chat.id
    user = user_dict[chat_id]
    dia = mensagem.text  
    user.data = dia    
    bot.send_message(mensagem.chat.id, texto)
    bot.register_next_step_handler(mensagem, confirmarClinico)

def confirmarClinico(mensagem):  
    chat_id = mensagem.chat.id
    user = user_dict[chat_id]
    hora = mensagem.text  
    user.hora = hora       
    texto = f"""
    Confirma a consulta?
    nome{user.name}
    medico{user.medico}
    data{user.data}
    hora{user.hora}
    /1 - Sim
    /2 - Não
    """
    
    bot.send_message(mensagem.chat.id, texto)
    bot.register_next_step_handler(mensagem, sucessoClinico)

def sucessoClinico(mensagem):     
    texto = """
    consulta marcada com sucesso!
    """
    bot.send_message(mensagem.chat.id, texto)    





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


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
#bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
#bot.load_next_step_handlers()


bot.polling()