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
        self.especialidade = None
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
def MarcarConsulta(mensagem):
    chat_id = mensagem.chat.id
    name = mensagem.from_user.first_name
    user = User(name)
    user_dict[chat_id] = user    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)                
    markup.add("Clinico Geral","Ortopedista","Psicólogo","Voltar")
    msg = bot.reply_to(mensagem, 'Qual é a sua necessidade?', reply_markup=markup)
    bot.register_next_step_handler(msg, EscolherEspecialidadeHandler)

def EscolherEspecialidadeHandler(mensagem):
    if(mensagem.text == "Clinico Geral"):
        EscolherClinicoGeral(mensagem)
    if(mensagem.text == "Voltar"):
        Iniciar(mensagem)
        

def EscolherClinicoGeral(mensagem):  
    # if(mensagem.text == "Voltar"):
    #     MarcarConsulta(mensagem)  
    # else :        
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
            bot.register_next_step_handler(msg, EscolherDiaClinicoGeral)
        

def EscolherDiaClinicoGeral(mensagem):
    if(mensagem.text == "Voltar"):
        mensagem.text = ""
        MarcarConsulta(mensagem)
    else :
        dia =  date.today()               
        chat_id = mensagem.chat.id
        medico = mensagem.text
        user = user_dict[chat_id]
        user.medico = medico
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        markup.add((dia).strftime("%d/%m/%Y"), (dia + timedelta(days=randrange(30))).strftime("%d/%m/%Y"), (dia + timedelta(days=randrange(70))).strftime("%d/%m/%Y"),"Voltar")
        msg = bot.reply_to(mensagem, 'Qual dos dias disponiveis você deseja marcar a consulta? (Clique em uma opção)', reply_markup=markup)            
        bot.register_next_step_handler(msg, EscolherHorarioClinicoGeral)

def EscolherHorarioClinicoGeral(mensagem):    
    if(mensagem.text == "Voltar"):
        mensagem.text = ""
        EscolherClinicoGeral(mensagem)
    else :
        chat_id = mensagem.chat.id
        user = user_dict[chat_id]
        dia = mensagem.text  
        user.data = dia    
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("08:00", "08:30", "09:00", "09:30", "10:00","Voltar")
        msg = bot.reply_to(mensagem, 'Qual horário você deseja marcar a consulta?', reply_markup=markup)    
        bot.register_next_step_handler(msg, confirmarClinico)

def confirmarClinico(mensagem):  
    if(mensagem.text == "Voltar"):
        mensagem.text = ""
        EscolherDiaClinicoGeral(mensagem)
    else:    
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
    if(mensagem.text == "Não"):
        texto=f"""
        Consulta cancelada!
        Para marcar uma nova consulta pressione /MarcarConsulta"""
        bot.reply_to(mensagem, texto)        
    
    if(mensagem.text=="Sim"):
        texto = f"""
        Consulta marcada com sucesso!
        para acessar o menu dé um oi para o atendente!
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

@bot.message_handler(commands=["VisualizarConsulta"])
def VisualizarConsulta(mensagem):
    chat_id = mensagem.chat.id
    with open ("bd.json") as json_file:
        data = json.load(json_file)
        data = data["consulta"]        
        if(len(data) == 0):
            bot.reply_to(mensagem, "Você não possui consultas marcadas!")
        else:
            for i in data:
                if i["chat_id"] == chat_id:
                    texto = f"""
                    Nome: {i["nome"]}
                    Médico: {i["medico"]}
                    Data: {i["data"]}
                    Horário: {i["hora"]}                    
                    """                
                    bot.send_message(mensagem.chat.id, texto)        

@bot.message_handler(commands=["CancelarConsulta"])
def CancelarConsulta(mensagem):
    chat_id = mensagem.chat.id
    with open ("bd.json") as json_file:
        data = json.load(json_file)
        data = data["consulta"]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        for i in data:
            if i["chat_id"] == chat_id:        
                markup.add(f"""{i["medico"]} - {i["data"]}""")
        bot.reply_to(mensagem, "Qual consulta você deseja cancelar?", reply_markup=markup)  
        bot.register_next_step_handler(mensagem, ApagarConsulta)

def ApagarConsulta(mensagem):
    chat_id = mensagem.chat.id
    with open ("bd.json") as json_file:
        data = json.load(json_file)
        #data = data["consulta"]
        if(len(data) == 0):
            bot.reply_to(mensagem, "Você não possui consultas marcadas!")
        else:
            for i in data["consulta"]:
                if i["chat_id"] == chat_id:
                    if mensagem.text == f"""{i["medico"]} - {i["data"]}""":
                        data["consulta"].remove(i)
                        write_json(data)
                        bot.reply_to(mensagem, "Consulta cancelada com sucesso!")


@bot.message_handler(commands=["ReagendarConsulta"])
def ReagendarConsulta(mensagem):
    chat_id = mensagem.chat.id
    with open ("bd.json") as json_file:
        data = json.load(json_file)
        data = data["consulta"]
        
        if(len(data) == 0):
            bot.reply_to(mensagem, "Você não possui consultas marcadas!")
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
            
            for i in data:
                if i["chat_id"] == chat_id:        
                    markup.add(f"""{i["medico"]} - {i["data"]}""")
            bot.reply_to(mensagem, "Qual consulta você deseja reagendar?", reply_markup=markup)  
            bot.register_next_step_handler(mensagem, Reagendar)

def Reagendar(mensagem):
    chat_id = mensagem.chat.id
    with open ("bd.json") as json_file:
        data = json.load(json_file)                
        
        for i in data["consulta"]:
            if i["chat_id"] == chat_id:
                if mensagem.text == f"""{i["medico"]} - {i["data"]}""":
                    data["consulta"].remove(i)
                    write_json(data)
                    bot.reply_to(mensagem, 
                    f"""Consulta cancelada!
                    Agora você pode marcar uma nova consulta!""")                    
                    MarcarConsulta(mensagem)





def verificar(mensagem):    
    return True

@bot.message_handler(func=verificar)
def Iniciar(mensagem):            
    texto = f"""
    Olá {mensagem.from_user.first_name},escolha uma opção para continuar (Clique no item):
     /MarcarConsulta Marcar consulta com um médico
     /ReagendarConsulta Reagendar consulta
     /VisualizarConsulta Visualizar consulta
     /CancelarConsulta Cancelar consulta
Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)

bot.polling()