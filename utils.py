#%%
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

#Função para ouvir e reconhecer a fala

def ouvir_microfone():
    #Habilita o microfone do usuário
    microfone = sr.Recognizer()

    #usando o microfone
    with sr.Microphone() as source:

        #Chama um algoritmo de reducao de ruidos no som
        microfone.adjust_for_ambient_noise(source)

        #Frase para o usuario dizer algo
        print("Diga alguma coisa: ")

        #Armazena o que foi dito numa variavel
        audio = microfone.listen(source, phrase_time_limit=3)

    try:

        #Passa a variável para o algoritmo reconhecedor de padroes
        frase = microfone.recognize_google(audio,language='pt-BR')

        #Retorna a frase pronunciada
        print("Você disse: " + frase)

    #Se nao reconheceu o padrao de fala, exibe a mensagem

    except:
       frase = False
       print("Não entendi")

    return frase

#Funcao responsavel por falar 

def cria_audio(audio, filename):

    tts = gTTS(audio,lang='pt-br')

    #Salva o arquivo de audio

    tts.save(filename)

    print("Audio criado com sucesso...")

def play_audio(filename):
    #Da play ao audio
    playsound(filename)

# %%
