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

from utils.login import LoginTwitch, NordVpnLogin
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

# Area das variáveis específicas de cada persona

email_login = ""
email_password = ""
twitch_username = ""
twitch_password = ""
server = ""
data_base_name = ""
home = ""
faixaEtaria = 0 # ----Mudar para a faixa etária desejada----

if faixaEtaria == 0: # 12-
    tempo_min = 300
    tempo_max = 600 
    jogosAssistir = allJogos

if faixaEtaria == 1:
    tempo_min = 300
    tempo_max = 600
    jogosAssistir = allJogos

# Configurar Logs
logging.basicConfig(
    filename="simulador.log",  
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S"  
)

# Configurar o WebDriver
chromeOptions = Options()
googleDir = "user-data-dir=" + home + "/.config/google-chrome"
chromeOptions.add_argument(googleDir)
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
                    
                    href = recommended_channels[i].get_attribute("href")  
                    channel_name = href.split("/")[-1]

                    logging.info(f"Canal Recomendado {i}: {channel_name} ({href})")

                    print(channel_name)
                    time.sleep(1.5)
                    channel = getChannelInfo(channel_name)
                    nomeArquivo = "coletaTwitch_" + data_base_name + "_recomendados.csv"
                    registrar_dados_recomendados(nomeArquivo, channel, id_transmissao)
                except Exception as e:
                    logging.error(f"Erro ao processar canal {i}: {str(e)}")
                    pass
        else:
            logging.error("Nenhum canal recomendado encontrado")
                
    except Exception as e:
        logging.error(f"Erro ao recuperar canais recomendados: {e}")
        pass

def Treino(driver):
    global id_transmissao

    NordVpnLogin(server)

    #TODO : Modularizar a pesquisa, para pesquisar mais de uma vez por sessão (3 a 5 vezes)
    #TODO : Mudar lógica de pesquisa, para pesquisar clicando na recomendação ao invés de apertar enter
    #TODO : Caso não encontre a transmissão, não contar a tentativa e salvar esse registro no CSV




 ################################
    tempoDeVisualizacao = random.randint(tempo_min, tempo_max)
    jogoPesquisado = random.choice(list(jogosAssistir))
    logging.info(f"Jogo escolhido: {jogoPesquisado}")
    time.sleep(random.uniform(3.0, 4.0))

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Search"]')))
    barraBusca = driver.find_element('css selector', '[placeholder="Search"]')
    barraBusca.clear()
    barraBusca.send_keys(jogoPesquisado)
    
    time.sleep(random.uniform(1.0, 2.0))

    barraBusca.send_keys(Keys.DOWN)
    time.sleep(random.uniform(0.7, 1.0))
    barraBusca.send_keys(Keys.RETURN) 

    time.sleep(random.uniform(1.5, 2.5))

    videoAssistido = random.randint(0, 2)

    #Mudar daqui pra baixo para selecionar os recomendados

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Layout-sc-1xcs6mc-0')))
    canais_achados = driver.find_elements(By.CSS_SELECTOR, '.Layout-sc-1xcs6mc-0')
    print(canais_achados)

    if len(canais_achados) == 0:
        logging.error("Nenhuma transmissão encontrada")
        screenshot_path = "screenshot_transmissao_nao_encontrada_" + id_transmissao + ".png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Nenhuma transmissão para {jogoPesquisado} encontrada Screenshot salva em: {screenshot_path}")
        return
    elif len(canais_achados) < (videoAssistido + 1):
        logging.INFO(f"Transmissão {videoAssistido} não encontrada, tentando transmissão 0")

        # Tirando o print da tela e salvando
        screenshot_path = "screenshot_transmissao_nao_encontrada_" + id_transmissao + ".png"
        driver.save_screenshot(screenshot_path)
        logging.info(f"Transmissão {id_transmissao} não encontrada Screenshot salva em: {screenshot_path}")

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

    nomeArquivo = "coletaTwitch_" + data_base_name + ".csv"
    registrar_dados(nomeArquivo, channel, tempoDeVisualizacao, jogoPesquisado, id_transmissao)

    id_transmissao += 1
    time.sleep(tempoDeVisualizacao)
################################

def acessarTwitch(driver):
    driver.get("https://www.google.com")

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

id_transmissao = 0

schedule.every().day.at("08:00").do(TreinarPersona1)
schedule.every().day.at("12:00").do(TreinarPersona1)
schedule.every().day.at("16:00").do(TreinarPersona1)
schedule.every().day.at("20:00").do(TreinarPersona1)
schedule.every().day.at("00:00").do(TreinarPersona1)
schedule.every().day.at("04:00").do(TreinarPersona1)

logging.info("Agendamento iniciado. Aguardando próxima execução...")

TreinarPersona1()
while True:
    schedule.run_pending()
    time.sleep(1)


