import os
import time
from colorama import Fore
import stdiomask
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from db_sql import banco_dados

# Chamando a class banco_dados no arquivo
db = banco_dados()

class sistema():

    # Informações para usar posteriomente no código
    usuario_cadastrado = ''
    senha = ''
    email_sender = ''
    caracteres = '@#!%&*()$":'
    email_principal = "heenrikk3@gmail.com"

    # Iniciando o menu
    def __init__(self) -> None:
         self.token = 'fxsugfifhslaqxxb'
         self.menu()

    # Função que exibi o menu na console do usuario
    def menu(self):

        os.system('cls')
    
        print('Sistema de Login\n'
        '\n'
        'Opções: \n'
        '[1]Cadastrar\n'
        '[2]Login\n'
        '[3]Fechar\n'
    )
        # Validação de escolha do usuario para executar funções para cada tipo de escolha
        opcoes = input("Digite uma opção: ")
        
        #Funçao para cadastrar um usuario
        if opcoes == "1":
            self.cadastrar()
        #Função para logar o usuario
        if opcoes == '2':
             #chamando diretamente a função de login do banco de dados
             db.validar_login()
                
        #Função para encerrar o codigo
        if opcoes == '3':
                print('Sistema fechando...')
                time.sleep(1)
                exit()

    # Função para validar o input do usuario tratando o que o usuario digita
    def cadastrar(self):
            
            self.usuario_cadastrado = input("Digite seu usuario: ")
            while len(self.usuario_cadastrado) == 0 or len(self.usuario_cadastrado) > 15:
                self.usuario_cadastrado = input("Usuario inválido, digite novamente: ")
            while re.search(r'[@#!$%^&*()<>?/\|}{~:]', self.usuario_cadastrado):
                self.usuario_cadastrado = input("Usuario inválido, digite novamente: ")

            self.senha = input("Digite uma senha: ")
            while len(self.senha) < 8 or len(self.senha) > 20:
                self.senha = stdiomask.getpass(prompt="Digite uma senha com mais de 8 caracteres: ", mask='*')  
            while re.search(r'[.@#_!$%^&*()<>?/\|}{~:]', self.senha):
                self.senha = stdiomask.getpass(prompt="Digite uma senha válida: ", mask='*')

            self.email_sender = input("Digite seu email: ")
            while len(self.email_sender) == 0:
                    self.email_sender = input("Email inválido, digite novamente: ")
            while '@' not in self.email_sender:
                self.email_sender = input("Digite um email válido: ")
                
            partes = self.email_sender.split('@')
            dominio = partes[1]
            while dominio != 'gmail.com':      
                self.email_sender = input("Seu email não termina com @gmail.com, digite outro: ")
                if "gmail.com" in self.email_sender:
                    break

            # Chamando a função para inserir dados
            db.inserir_dados(self.usuario_cadastrado, self.senha, self.email_sender)
            print(Fore.BLUE + "Usuario cadastrado!" + Fore.RESET)
            print("Voltando para o menu...")

            #Retornando o menu do usario
            time.sleep(2)
            self.enviar_email()
            self.menu()

    #Função para enviar o email de confirmação de cadastro
    def enviar_email(self):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(self.email_principal, self.token)
        msg = MIMEMultipart()
        msg['From'] = self.email_principal
        msg['To'] = self.email_sender
        msg['Subject'] = 'Usuario cadastrado!'
        body = f'Você criou uma conta com o email {self.email_sender} no sistema de login do Diego!'
        msg.attach(MIMEText(body, 'plain'))
        server.sendmail(self.email_principal, self.email_sender, msg.as_string().encode('utf-8'))
        server.quit()
