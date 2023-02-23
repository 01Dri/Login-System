import pymysql.cursors
from colorama import Fore
import time
import os
from os import system

class banco_dados():

      #Chjamando a class sistema do arquivo functionss 
      # informações para conexao com o banco de dados
      host = 'localhost'
      user = 'root'
      password = ''

      # funcão para conectar ao db
      def conecta(self):
            try: 
                  self.conexao = pymysql.connect(
                  host=self.host,
                  user=self.user,
                  password=self.password,
                  db='usuarios',
                  charset='utf8mb4',
                  cursorclass=pymysql.cursors.DictCursor
                  )
                  self.cursor = self.conexao.cursor()
            except:
                  print(Fore.RED + 'Banco de dados off-line ou inexistente!' + Fore.RESET)
                  exit()
      

            # verificando seu a table cliente, se não, ele cria uma com os valores nome, email, senha
            #Se sim, ele ignora ele pula para o reesto do código
            try:
                  self.cursor.execute("""CREATE TABLE clientes (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    nome VARCHAR(100) NOT NULL,
                                    email VARCHAR(100) NOT NULL,
                                    senha VARCHAR(20) NOT NULL
                                    )
                                    """)
            except:
                  pass

      # Função para inserir dados no mysql
      def inserir_dados(self, nome, senha, email):
            self.conecta()
            consulta = 'SELECT * FROM clientes WHERE nome = %s'
            self.cursor.execute(consulta, (nome,))
            resultado = self.cursor.fetchone()
            
            #Serie de validações para confirmar se o usuario digitado não existe
            while resultado is not None:
                  print(Fore.RED + "Nome de usuario já cadastrado!")
                
                  nome = input("Digite novamente um nome: ")
                  email = input("Digite novamente o email: ")
                  senha = input("Digite novamente a senha: ")
                  consulta = 'SELECT * FROM clientes WHERE nome = %s'
                  self.cursor.execute(consulta, (nome,))
                  resultado = self.cursor.fetchone()
                  if resultado is None:
                        break
                      
                  

            consulta = 'SELECT * FROM clientes WHERE email = %s'
            self.cursor.execute(consulta, (email,))
            resultado = self.cursor.fetchone()
            while resultado is not None:
                  print(Fore.RED + "Email  já cadastrado!" + Fore.RESET)
            
                  email = input("Digite novamente o email: ")
                  consulta = 'SELECT * FROM clientes WHERE email = %s'
                  self.cursor.execute(consulta, (email,))
                  resultado = self.cursor.fetchone()
                  if resultado is None:
                        break
                        
            # Inserindo dados no mysql após condições
            self.cursor.execute('INSERT INTO clientes (nome, email, senha) VALUES (%s, %s, %s)', (nome, email, senha))
            self.conexao.commit()
            self.cursor.close()
            self.conexao.close()
                  
            
      # Função para validar e fazer  o login do usuario, se realmente existe na base de dados
      def validar_login(self):
            self.conecta()
            user = input("Digite seu nome: ")
            senha_user = input("Digite sua senha: ")
            self.cursor.execute('SELECT * FROM clientes')
            resultados = self.cursor.fetchall()
            consulta = 'SELECT * FROM clientes WHERE nome = %s'
            self.cursor.execute(consulta, (user,))
            resultado = self.cursor.fetchone()
            
            while resultado is None:
                  user = input(Fore.RED + "Nome incorreto!, digite novamente: " + Fore.RESET)
                  senha_user = input("Digite novamente sua senha: ")
                  consulta = 'SELECT * FROM clientes WHERE nome = %s'
                  self.cursor.execute(consulta, (user,))
                  resultado = self.cursor.fetchone()
                  if resultado is not None:
                        continue
            while resultado['senha'] != senha_user:
                  senha_user = input(Fore.RED + "Senha incorreta, digite novamente: " + Fore.RESET)
            
            os.system('cls')
            print(Fore.GREEN + '===================================' + Fore.RESET)
            print(Fore.GREEN + f"Bem vindo {user}" + Fore.RESET)
            print(Fore.GREEN + '===================================' + Fore.RESET)
            time.sleep(5)
