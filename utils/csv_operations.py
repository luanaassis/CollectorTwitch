import csv
import datetime

def registrar_dados(csv_file, jogo, duracao):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Escreve o cabeçalho apenas se o arquivo estiver vazio
        if file.tell() == 0:
            writer.writerow(["Data", "Jogo", "Duração (segundos)"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), jogo, duracao])