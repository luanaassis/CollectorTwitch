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
# 2 = 14 - 17
# 3 = 18+
faixaEtaria = 2

# Area das variáveis específicas de cada faixa etária

if faixaEtaria == 0:
    tempo_min = 450
    tempo_max = 900 
    jogosAssistir = jogosLivre

if faixaEtaria == 1:
    tempo_min = 600
    tempo_max = 1800
    jogosAssistir = jogosLivre.union(jogos10)

if faixaEtaria == 2:
    tempo_min = 900
    tempo_max = 3600 
    jogosAssistir = jogosLivre.union(jogos10, jogos12, jogos14)

if faixaEtaria == 3:
    tempo_min = 900
    tempo_max = 7200
    jogosAssistir = "A DEFINIR"

# Area das variáveis específicas de cada persona

diretorio_perfil = "--profile-directory=Profile 1"
google_login = "flaviocrianco@gmail.com"
google_password = "Superben10!"
twitch_username = "flaviocrianco"
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
chromeOptions.add_argument("user-data-dir=/home/locus/.config/google-chrome")
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

def RecuperarRecomendados(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//div[@class="Layout-sc-1xcs6mc-0 cwtKyw side-nav-card"])/a')))
        recommended_channels = driver.find_elements(By.XPATH, '(//div[@class="Layout-sc-1xcs6mc-0 cwtKyw side-nav-card"])/a')

        logging.info("Canais Recomendados atualmente:")
        if(len(recommended_channels) != 0):
            for i in range(len(recommended_channels)):
                logging.info(f"Canal Recomendado {i}: {recommended_channels[i].text}")
        else:
            logging.error("Nenhum canal recomendado encontrado")
                
    except Exception as e:
        logging.error(f"Erro ao recuperar canais recomendados: {e}")
        pass

def Treino(driver):

    tempoDeVisualizacao = random.randint(tempo_min, tempo_max)

    jogoPesquisado = random.choice(list(jogosAssistir))
    logging.info(f"Jogo escolhido: {jogoPesquisado}")

    barraBusca = driver.find_element('css selector', '[placeholder="Buscar"]')
    barraBusca.send_keys(jogoPesquisado)
    
    time.sleep(random.uniform(1.0, 2.0))

    barraBusca.send_keys(Keys.RETURN)

    time.sleep(random.uniform(1.5, 2.5))

    videoAssistido = random.randint(0, 2)

    canais_achados = driver.find_elements(By.CSS_SELECTOR, '[data-a-target="search-result-live-channel"]')

    if len(canais_achados) == 0:
        logging.error("Nenhuma transmissão encontrada")
        screenshot_path = "screenshot_nenhuma_transmissao_nao_encontrada.png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot salva em: {screenshot_path}")
        return
    elif len(canais_achados) < videoAssistido:
        logging.INFO(f"Transmissão {videoAssistido} não encontrada, tentando transmissão 0")

        # Tirando o print da tela e salvando
        screenshot_path = "screenshot_transmissao_nao_encontrada.png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot salva em: {screenshot_path}")

        videoAssistido = 0
    
    video = canais_achados[videoAssistido]

    logging.info(f"Assistindo {video.text} por {tempoDeVisualizacao} segundos")
    video.click()
    RecuperarRecomendados(driver)
    time.sleep(tempoDeVisualizacao)

def acessarTwitch(driver):
    driver.get("https://www.google.com")

    try:
        ChromeLogin(driver, google_login, google_password)
        time.sleep(random.uniform(3.0, 5.5))
    except:
        logging.info("Erro ao logar no Google ou Login já realizado")
        pass

    try:
        driver.get("https://www.twitch.tv")
        LoginTwitch(driver, twitch_username, twitch_password)
    except:
        logging.info("Erro ao logar no Twitch ou Login já realizado")
        pass

def TreinarPersona1():
    #iniciar driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chromeOptions)
    driver.maximize_window()
   
    
    acessarTwitch(driver)

    try:
        logging.info("Iniciando treino...")
        Treino(driver)
        logging.info("Treino concluído com sucesso.")
    except Exception as e:
        logging.error(f"Erro durante o treino: {e}")

    driver.quit()

schedule.every().day.at("10:00").do(TreinarPersona1)
schedule.every().day.at("14:00").do(TreinarPersona1)
schedule.every().day.at("18:00").do(TreinarPersona1)

logging.info("Agendamento iniciado. Aguardando próxima execução...")

while True:
    schedule.run_pending()
    time.sleep(1)


