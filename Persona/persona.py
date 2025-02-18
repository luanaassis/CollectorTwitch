from math import e
import random
import time
import logging
import schedule
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils.login import ChromeLogin, LoginTwitch
from utils.csv_operations import registrar_dados, registrar_dados_recomendados
from utils.channelCollector import getChannelInfo

jogosLivre = {"Minecraft", "EA Sports FC 25"}
jogos10 = {"ROBLOX"}
jogos12 = {"Fortnite", "Sea of Thieves", "The Sims 4", "League of Legends", "Overwatch 2", "Marvel Rivals"}
jogos14 = {"Valorant"}
jogos16 = {"Counter-Strike"}
jogos18 = {"Grand Theft Auto V"}

jogosE = {"EA Sports FC 25"}  # Everyone (Livre para todas as idades)
jogosE10 = {"Minecraft"}  # Everyone 10+ (Maiores de 10 anos)
jogosT = {"ROBLOX", "Fortnite", "Sea of Thieves", "The Sims 4", "League of Legends", "Overwatch 2", "Marvel Rivals", "Valorant"}  # Teen (Maiores de 13 anos)
jogosM = {"Counter-Strike", "Grand Theft Auto V"}  # Mature (Maiores de 17 anos)

allJogos = jogosLivre.union(jogos10, jogos12, jogos14, jogos16, jogos18)


# 0 = 0 - 9
# 1 = 10 - 11
# 2 = 12 - 13
# 3 = 14 - 15
# 4 = 16 - 17
# 5 = 18+
faixaEtaria = 0

# Area das variáveis específicas de cada faixa etária

if faixaEtaria == 0: # 12-
    tempo_min = 600
    tempo_max = 3600 
    jogosAssistir = jogosLivre.union(jogos10, jogos12)

if faixaEtaria == 1:
    tempo_min = 900
    tempo_max = 7200
    jogosAssistir = allJogos

# Area das variáveis específicas de cada persona


email_login = "mickevans13@outlook.com"
email_password = "LOCUS123!"
twitch_username = "mickevans13"
twitch_password = "LOCUS123!"

# Configurar Logs
logging.basicConfig(
    filename="simulador.log",  # Nome do arquivo de log
    level=logging.INFO,  # Nível de registro (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
    datefmt="%Y-%m-%d %H:%M:%S"  # Formato da data
)

# Carregar variáveis de ambiente
load_dotenv()

# Configurar o WebDriver
chromeOptions = Options()
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
                try:
                    # Pega o atributo 'href' diretamente do elemento <a>
                    href = recommended_channels[i].get_attribute("href")  # Exemplo: "/yoda"

                    # Extrai o nome do canal do href (última parte da URL)
                    channel_name = href.split("/")[-1]  # "yoda"

                    logging.info(f"Canal Recomendado {i}: {channel_name} ({href})")

                    print(channel_name)
                    time.sleep(1.5)
                    channel = getChannelInfo(channel_name)
                    registrar_dados_recomendados("coletaTwitchBr1_recomendados.csv", channel, id_transmissao)
                except Exception as e:
                    logging.error(f"Erro ao processar canal {i}: {str(e)}")
                    pass
        else:
            logging.error("Nenhum canal recomendado encontrado")
                
    except Exception as e:
        logging.error(f"Erro ao recuperar canais recomendados: {e}")
        pass

def Treino(driver):

    tempoDeVisualizacao = random.randint(tempo_min, tempo_max)

    jogoPesquisado = random.choice(list(jogosAssistir))
    logging.info(f"Jogo escolhido: {jogoPesquisado}")

    time.sleep(random.uniform(3.0, 4.0))

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Search"]')))
    barraBusca = driver.find_element('css selector', '[placeholder="Search"]')
    barraBusca.send_keys(jogoPesquisado)
    
    time.sleep(random.uniform(1.0, 2.0))

    barraBusca.send_keys(Keys.RETURN)

    time.sleep(random.uniform(1.5, 2.5))

    videoAssistido = random.randint(0, 2)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-a-target="search-result-live-channel"]')))
    canais_achados = driver.find_elements(By.CSS_SELECTOR, '[data-a-target="search-result-live-channel"]')
    print(canais_achados)

    if len(canais_achados) == 0:
        logging.error("Nenhuma transmissão encontrada")
        screenshot_path = "screenshot_nenhuma_transmissao_nao_encontrada.png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot salva em: {screenshot_path}")
        return
    elif len(canais_achados) < (videoAssistido + 1):
        logging.INFO(f"Transmissão {videoAssistido} não encontrada, tentando transmissão 0")

        # Tirando o print da tela e salvando
        screenshot_path = "screenshot_transmissao_nao_encontrada.png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot salva em: {screenshot_path}")

        videoAssistido = 0
    
    video = canais_achados[videoAssistido]

    print(video)

    logging.info(f"Assistindo {video.text} por {tempoDeVisualizacao} segundos")
    video.click()
    RecuperarRecomendados(driver)

    id = driver.current_url.split("/")[-1]
    print(id)
    channel = getChannelInfo(id)
    print(channel)
    registrar_dados("coletaTwitchUS1.csv", channel, tempoDeVisualizacao, jogoPesquisado, id_transmissao)
    id_transmissao += 1
    time.sleep(tempoDeVisualizacao)

def acessarTwitch(driver):
    driver.get("https://www.google.com")
    driver.get("https://www.twitch.tv")

    try:
        driver.get("https://www.twitch.tv")
        LoginTwitch(driver, twitch_username, twitch_password, email_login, email_password)
    except:
        logging.info("Erro ao logar no Twitch ou Login já realizado")
        pass

def TreinarPersona1():
    #iniciar driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chromeOptions)
    driver.maximize_window()
   
    
    acessarTwitch(driver)
    time.sleep(random.uniform(1.0, 2.0))

    try:
        logging.info("Iniciando treino...")
        Treino(driver)
        logging.info("Treino concluído com sucesso.")
    except Exception as e:
        logging.error(f"Erro durante o treino: {e}")

    driver.quit()

schedule.every().day.at("06:00").do(TreinarPersona1)
schedule.every().day.at("10:00").do(TreinarPersona1)
schedule.every().day.at("14:00").do(TreinarPersona1)
schedule.every().day.at("19:30").do(TreinarPersona1)
schedule.every().day.at("22:00").do(TreinarPersona1)

id_transmissao = 0

logging.info("Agendamento iniciado. Aguardando próxima execução...")
while True:
    schedule.run_pending()
    time.sleep(1)


