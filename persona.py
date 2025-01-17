from math import e
import random
import time
import logging
import schedule

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import collector
from utils.login import ChromeLogin, LoginTwitch
from utils.csv_operations import registrar_dados

jogosLivre = {"Minecraft"}
jogos10 = {"ROBLOX"}
jogos12 = {"Fortnite", "Sea of Thieves", "The Sims 4", "League of Legends", "Overwatch 2"}
jogos14 = {"Valorant"}

# 0 = 0 - 10
# 1 = 10 - 13
# 2 = 13 - 17
# 3 = 18+
faixaEtaria = 2

# Area das variáveis específicas de cada faixa etária
if faixaEtaria == 0:
    #Talvez tenha que mudar a varivel para que em toda ocorrencia randomize o numero
    tempoDeVisualizacao = random.uniform(450, 900) # Em segundos
    jogosAssistir = jogosLivre

if faixaEtaria == 1:
    tempoDeVisualizacao = random.uniform(600, 600) # Em segundos
    jogosAssistir = jogosLivre.union(jogos10)

if faixaEtaria == 2:
    tempoDeVisualizacao = random.uniform(900,   3600) # Em segundos
    jogosAssistir = jogosLivre.union(jogos10, jogos12, jogos14)

if faixaEtaria == 3:
    tempoDeVisualizacao = 3600 # Em segundos
    jogosAssistir = "A DEFINIR"

# Area das variáveis específicas de cada persona

diretorio_perfil = "--profile-directory=Profile 6"
google_login = "crianca1LOCUS@gmail.com"
google_password = "Superben10!"
twitch_username = "crianca0101"
twitch_password = "Superben10!"

# Configurar Logs
logging.basicConfig(
    filename="simulador.log",  # Nome do arquivo de log
    level=logging.INFO,  # Nível de registro (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
    datefmt="%Y-%m-%d %H:%M:%S"  # Formato da data
)

# Configurar o WebDriver
chromeOptions = Options()
chromeOptions.add_argument(diretorio_perfil)
chromeOptions.add_argument("user-data-dir=/home/flavio/.config/google-chrome")
chromeOptions.add_argument("--window-size=1280,800")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-notifications")
chromeOptions.add_argument("--disable-infobars")
chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-dev-shm-usage")
chromeOptions.add_argument("--remote-debugging-port=9222")
chromeOptions.add_argument("--disable-gpu")
chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
chromeOptions.add_experimental_option("useAutomationExtension", False)

def assistirRecomendado(driver):
    try:
        first_channel = driver.find_element(By.XPATH, '(//div[@class="Layout-sc-1xcs6mc-0 cwtKyw side-nav-card"])[1]/a')
        first_channel.click()
        print("Primeiro canal clicado com sucesso!")
    except Exception as e:
        print(f"Erro ao clicar no elemento: {e}")
        pass

def Treino(driver):

    jogoPesquisado = random.choice(list(jogosAssistir))
    logging.info(f"Jogo escolhido: {jogoPesquisado}")

    barraBusca = driver.find_element('css selector', '[placeholder="Buscar"]')
    barraBusca.send_keys(jogoPesquisado)
    
    time.sleep(random.uniform(1.0, 2.0))

    barraBusca.send_keys(Keys.RETURN)

    time.sleep(random.uniform(1.5, 2.5))

    videoAssistido = random.randint(0, 2)

    canais_achados = driver.find_elements(By.CSS_SELECTOR, '[data-a-target="search-result-live-channel"]')
    videoAssistido = 1
    if len(canais_achados) == 0:
        print("Nenhum canal encontrado")
        return
    elif len(canais_achados) < videoAssistido:
        print("Canal não encontrado")
        return
    else:
        video = canais_achados[videoAssistido]
    
    logging.info(f"Assistindo {video.text} por {tempoDeVisualizacao} segundos")
    video.click()
    time.sleep(tempoDeVisualizacao)

def acessarTwitch(driver):
    driver.get("https://www.google.com")

    try:
        ChromeLogin(driver)
        time.sleep(random.uniform(3.0, 5.5))
    except:
        logging.info("Erro ao logar no Google ou Login já realizado")
        pass

    try:
        driver.get("https://www.twitch.tv")
        LoginTwitch(driver)
    except:
        logging.info("Erro ao logar no Twitch ou Login já realizado")
        pass

def TreinarPersona1():
    #iniciar driver
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
        driver.maximize_window()
    except:
        logging.error("Erro ao iniciar o driver")
        exit()
    
    acessarTwitch(driver)

    try:
        logging.info("Iniciando treino...")
        Treino(driver)
        logging.info("Treino concluído com sucesso.")
    except Exception as e:
        logging.error(f"Erro durante o treino: {e}")

    driver.quit()


schedule.every().day.at("10:00").do(TreinarPersona1)
schedule.every().day.at("13:35").do(TreinarPersona1)

logging.info("Agendamento iniciado. Aguardando próxima execução...")

while True:
    schedule.run_pending()
    time.sleep(1)

