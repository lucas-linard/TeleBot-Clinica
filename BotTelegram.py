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

def write_json(data, filename='bd.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4)       

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
    if (mensagem.text == "Voltar"):
            return msg
    bot.register_next_step_handler(msg, EscolherClinicoGeral)


def EscolherClinicoGeral(mensagem):        
    with open('bd.json') as json_file:
        data = json.load(json_file)
        data = data["medicos"]
        texto = f"""
        Escolha um medico disponivel de sua preferencia!
        /1 - {data[0]["name"]}
        /2 - {data[1]["name"]}
        /3 - {data[2]["name"]}
        """                        
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)                
        markup.add(data[0]["name"], data[1]["name"], data[2]["name"],"Voltar")
        msg = bot.reply_to(mensagem, 'Escolha um medico disponivel de sua preferencia! (Clique em uma opção)', reply_markup=markup)
        if (mensagem.text == "Voltar"):
            return msg
        bot.register_next_step_handler(msg, EscolherDiaClinicoGeral)        
        

def EscolherDiaClinicoGeral(mensagem):
    if(mensagem.text == "Voltar"):
        msg = opcao1(mensagem)
        bot.register_next_step_handler(msg, opcao1)
    else :
        dia =  date.today()               
        chat_id = mensagem.chat.id
        medico = mensagem.text
        user = user_dict[chat_id]
        user.medico = medico
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup.add((dia).strftime("%d/%m/%Y"), (dia + timedelta(days=randrange(30))).strftime("%d/%m/%Y"), (dia + timedelta(days=randrange(70))).strftime("%d/%m/%Y"))
        msg = bot.reply_to(mensagem, 'Qual dos dias disponiveis você deseja marcar a consulta? (Clique em uma opção)', reply_markup=markup)    
        if (mensagem.text == "Voltar"):
            return msg
        bot.register_next_step_handler(msg, EscolherHorarioClinicoGeral)

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
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("08:00", "08:30", "09:00", "09:30", "10:00")
    msg = bot.reply_to(mensagem, 'Qual horário você deseja marcar a consulta?', reply_markup=markup)    
    bot.register_next_step_handler(msg, confirmarClinico)

def confirmarClinico(mensagem):  
    chat_id = mensagem.chat.id
    user = user_dict[chat_id]
    hora = mensagem.text  
    user.hora = hora       
    texto = f"""
    Confirma a consulta?
    Nome: {user.name}
    Médico: {user.medico}
    Data: {user.data}
    Horário: {user.hora}    
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    markup.add("Sim", "Não")
    msg = bot.reply_to(mensagem, texto, reply_markup=markup)    
    bot.register_next_step_handler(msg, sucessoClinico)

def sucessoClinico(mensagem):     
    texto = """
    Consulta marcada com sucesso!
    """
    chat_id = mensagem.chat.id
    user = user_dict[chat_id]
    with open ("bd.json") as json_file:
        data = json.load(json_file)
        temp = data["consulta"]
        y = {"chat_id" :chat_id, "nome": user.name, "medico": user.medico, "data": user.data, "hora": user.hora}
        temp.append(y)
    write_json(data)
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
     /CancelarConsulta Cancelar consulta
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)

bot.polling()