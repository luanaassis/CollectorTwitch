import csv
from twitchio import Client
from datetime import datetime
import signal
import sys

# Configurações
OAUTH_TOKEN = 'oauth:0hvgub57fwqekdaj5ku3cl18g3d0wp'  # Obtenha em: https://twitchapps.com/tmi/
CHANNEL = 'alanzoka'  # Ex: 'xqc'

# Cria o cliente do Twitch
client = Client(token=OAUTH_TOKEN, initial_channels=[CHANNEL])

# Função para salvar mensagens (ABRE O ARQUIVO A CADA ESCRITA)
def save_to_csv(timestamp, user, channel, message):
    with open('twitch_chat.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, user, channel, message])

# Evento de mensagem recebida
@client.event()
async def event_message(message):
    if message.author and message.content:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_to_csv(timestamp, message.author.name, CHANNEL, message.content)
        print(f'{timestamp} - {message.author.name}: {message.content}')

# Tratamento para Ctrl+C (FECHAMENTO CORRETO)
def signal_handler(sig, frame):
    print("\nEncerrando o script...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Inicia a conexão
client.run()