import csv
import os
import time
from datetime import datetime
from twitchio import Client
from twitchio import Message
import asyncio

OAUTH_TOKEN = 'oauth:0hvgub57fwqekdaj5ku3cl18g3d0wp'  # Obtenha em: https://twitchapps.com/tmi/


async def collect_twitch_chat(
    channel_id: str,
    oauth_token: str,
    csv_filename: str,
    duration: int,
    StreamTitle: str,
    StreamGame: str
):
    """
    Coleta mensagens do chat da Twitch e salva em um CSV.
    
    Parâmetros:
    - channel_id (str): Id do canal a ser monitorado.
    - oauth_token (str): Token OAuth (opcional, busca do .env).
    - csv_filename (str): Nome do arquivo CSV de saída.
    - duration (int): Duração em segundos para coletar mensagens.
    - StreamTitle (str): Título da stream.
    - StreamGame (str): Jogo da stream.
    """
    
    # Configurações do CSV
    HEADER = [
        'timestamp', 'message_id', 'user_id', 'user_name', 'channel_id',
        'channel_id', 'stream_title', 'stream_game', 'message_content',
        'user_badges', 'badge_info', 'is_mod', 'is_sub', 'user_color',
        'bits_used', 'reply_parent_id', 'channel_reward_id', 'emotes_used',
        'is_deleted', 'deletion_reason'
    ]

    # Cria arquivo CSV com cabeçalho se necessário
    if not os.path.exists(csv_filename) or os.stat(csv_filename).st_size == 0:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
            csv.writer(file).writerow(HEADER)

    client = Client(
        token=oauth_token,
        initial_channels=[channel_id]
    )

    @client.event()
    async def event_ready():
        print(f'Conectado como {client.nick}')
        print(f'Pronto para coletar mensagens de: {channel_id}')

    @client.event()
    async def event_message(message: Message):
        try:
            tags = message.tags
            author = message.author

            # Correção 1: Badges são strings, não objetos!
            user_badges = tags.get('badges', '')  # Formato: 'subscriber/12,moderator/1'
            
            # Correção 2: Emotes via tags (não message.emotes)
            emotes = tags.get('emotes', '')  # Formato: 'emotesv2_123:0-4,6-10/456:12-15'

            # Obtem timestamp do servidor ou usa o tempo atual como fallback
            timestamp_ms = tags.get('tmi-sent-ts')
            if timestamp_ms:
                timestamp = datetime.fromtimestamp(int(timestamp_ms) / 1000).isoformat()
            else:
                timestamp = datetime.now().isoformat()

            # Monta os dados
            data = [
                timestamp,
                tags.get('id', 'N/A'),
                author.id,
                author.name,
                channel_id,
                tags.get('room-id', 'N/A'),
                StreamTitle,
                StreamGame,
                message.content,
                user_badges,  # Já formatado como string
                tags.get('badge-info', 'N/A'),
                tags.get('mod', '0'),
                tags.get('subscriber', '0'),
                tags.get('color', '#FFFFFF'),
                tags.get('bits', '0'),
                tags.get('reply-parent-msg-id', 'N/A'),
                tags.get('custom-reward-id', 'N/A'),
                emotes,  # Emotes como string (IDs e posições)
                tags.get('deleted', '0'),
                tags.get('deletion-reason', 'N/A')
            ]

            with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(data)
            print(f'Mensagem salva: {author.name} -> {message.content}')

        except AttributeError as e:
             # Pode ocorrer se message.author ou message.channel for None inesperadamente
             print(f"Erro de atributo ao processar mensagem: {e} - Mensagem: {message.raw_data}")
        except Exception as e:
            print(f'Erro geral ao processar mensagem: {e} - Mensagem: {message.raw_data}')

    print(f"Iniciando coleta do chat de {channel_id} por {duration} segundos...")
    try:
        # Conecta e inicia o cliente de forma não bloqueante
        task = asyncio.create_task(client.start())

        # Mantém a função principal "viva" pela duração desejada
        await asyncio.sleep(duration)

        task.cancel()

    except Exception as e:
        print(f"Erro durante a execução do cliente: {e}")
    finally:
        # NAO ESTA FINALIZANDO
        print(f"Tempo esgotado ({duration}s). Finalizando coleta de {channel_id}...")
        await client.close()
        print(f"Coleta do chat de {channel_id} finalizada. Dados salvos em {csv_filename}")

if __name__ == "__main__":
    asyncio.run(collect_twitch_chat(
        channel_id="loud_coringa",
        oauth_token=OAUTH_TOKEN,
        csv_filename="chat_custom.csv",  
        duration=60,  # Tempo em segundos para coleta
        StreamTitle="Título da Stream Exemplo",
        StreamGame="Jogo da Stream Exemplo"
    ))
