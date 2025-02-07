import csv
from datetime import datetime

def registrar_dados(csv_file, channel_data, View_time, searched_game):
    try:
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Escreve o cabeçalho apenas se o arquivo estiver vazio
            if file.tell() == 0:
                writer.writerow([
                                "Data",
                                "View_time",
                                "searched_game",
                                "channel_name",
                                "language",
                                "last_game_name",
                                "stream_title",
                                "stream_tags",
                                "classification_labels",
                                "is_branded_content"
                                ])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                View_time,
                searched_game,
                channel_data.channel_name,
                channel_data.language,
                channel_data.last_game_name,
                channel_data.stream_title,
                channel_data.stream_tags,
                channel_data.classification_labels,
                channel_data.is_branded_content
                ])
    except Exception as e:
        print(f"Erro ao registrar dados: {e}")
        pass