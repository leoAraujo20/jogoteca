import os

import psycopg
from dotenv import load_dotenv
from psycopg import OperationalError

load_dotenv()

print('Conectando ao banco de dados PostgreSQL com psycopg v3...')

try:
    conn = psycopg.connect(
        host='localhost',
        port='5432',
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
except OperationalError as err:
    print('Não foi possível conectar ao banco de dados.')
    print(err)
    exit()

cursor = conn.cursor()

TABLES = {}

TABLES['Jogos'] = """
      CREATE TABLE IF NOT EXISTS jogos (
      id SERIAL PRIMARY KEY,
      nome VARCHAR(50) NOT NULL,
      categoria VARCHAR(40) NOT NULL,
      console VARCHAR(20) NOT NULL
      );"""

TABLES['Usuarios'] = """
      CREATE TABLE IF NOT EXISTS usuarios (
      id SERIAL PRIMARY KEY,
      username VARCHAR(50) UNIQUE NOT NULL,
      senha VARCHAR(100) NOT NULL
      );"""

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f'Criando tabela {tabela_nome}...', end=' ')
        cursor.execute(tabela_sql)
    except (
        psycopg.Error
    ) as err: 
        print(err)
    else:
        print('OK')

usuario_sql = 'INSERT INTO usuarios (username, senha) VALUES (%s, %s)'
usuarios = [
    ('BD', 'alohomora'),
    ('Mila', 'paozinho'),
    ('Cake', 'python_eh_vida'),
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute(
    'SELECT username FROM usuarios'
) 
print('\n-------------  Usuários Inseridos:  -------------')
for user in cursor.fetchall():
    print(user[0])

jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
    ('Tetris', 'Puzzle', 'Atari'),
    ('God of War', 'Hack n Slash', 'PS2'),
    ('Mortal Kombat', 'Luta', 'PS2'),
    ('Valorant', 'FPS', 'PC'),
    ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
    ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(jogos_sql, jogos)

cursor.execute('SELECT nome FROM jogos')
print('\n-------------  Jogos Inseridos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[0])

conn.commit()

cursor.close()
conn.close()

print('\nBanco de dados preparado com sucesso usando psycopg v3!')
