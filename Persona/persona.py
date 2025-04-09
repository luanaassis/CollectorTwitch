from math import e
import random
import time
import logging
import schedule
import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils.login import LoginTwitch
from utils.csv_operations import registrar_dados, registrar_dados_recomendados
from utils.channelCollector import getChannelInfo
from utils.chatCollector import collect_twitch_chat

jogosLivre = {"minecraft", "ea-sports-fc-25"}
jogos10 = {"roblox"}
jogos12 = {"fortnite", "sea-of-thieves", "the-sims-4", "league-of-legends", "overwatch-2", "marvel-rivals"}
jogos14 = {"valorant"}
jogos16 = {"counter-strike"}
jogos18 = {"grand-theft-auto-v"}

jogosE = {"EA Sports FC 25"}  # Everyone (Livre para todas as idades)
jogosE10 = {"Minecraft"}  # Everyone 10+ (Maiores de 10 anos)
jogosT = {"ROBLOX", "Fortnite", "Sea of Thieves", "The Sims 4", "League of Legends", "Overwatch 2", "Marvel Rivals", "Valorant"}  # Teen (Maiores de 13 anos)
jogosM = {"Counter-Strike", "Grand Theft Auto V"}  # Mature (Maiores de 17 anos)

badSearch = {"ROBLOX", "Marvel RIvals", "League of Legends", "Counter-Strike"}


allJogos = jogosLivre.union(jogos10, jogos12, jogos14, jogos16, jogos18)

# Area das variáveis específicas de cada persona ( MUDE AQUI )

idade = "15 - 12/11/2009"
br = True
login = "guilhermebraga0015"
data_base_name = "br15"
home = "/home/twitchcollector1"
OAUTH_TOKEN = 'oauth:0hvgub57fwqekdaj5ku3cl18g3d0wp'  # Obtenha em: https://twitchapps.com/tmi/



email_login = login + "@outlook.com"
email_password = "Locus123!"
twitch_username = login
twitch_password = "Locus123!"
textSearchbar = "Search"
digit = "Digit"
if(br):
    textSearchbar = "Buscar"
    digit = "Dígito" 
    
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
    #TODO : Modularizar a pesquisa, para pesquisar mais de uma vez por sessão (3 a 5 vezes)
    #TODO : Caso não encontre a transmissão, não contar a tentativa e salvar esse registro no CSV
   
    global id_transmissao
    numeroBuscas = random.randint(3, 5)
    logging.info(f"Realizando {numeroBuscas} buscas nessa sessão")
    jogosJaPesquisados = {"jogo"}
    for i in range(numeroBuscas):
        tempoDeVisualizacao = random.randint(tempo_min, tempo_max)
        #Garante que nao repita jogos na mesma sessão
        jogoCandidato = random.choice(list(jogosAssistir))
        while(jogoCandidato in jogosJaPesquisados):
            jogoCandidato = random.choice(list(jogosAssistir))
        
        jogoPesquisado = jogoCandidato
        jogosJaPesquisados.add(jogoCandidato)

        logging.info(f"Jogo escolhido: {jogoPesquisado}")
        time.sleep(random.uniform(3.0, 4.0))

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'[placeholder="{textSearchbar}"]')))
        barraBusca = driver.find_element('css selector',  f'[placeholder="{textSearchbar}"]')
        barraBusca.clear()
        barraBusca.send_keys(jogoPesquisado)
        
        time.sleep(random.uniform(2.0, 2.5))
        jogoLink = "https://www.twitch.tv/directory/category/" + jogoPesquisado
        driver.get(jogoLink)

        time.sleep(random.uniform(15, 20))

        nomeArquivo = "coletaTwitch_" + data_base_name + ".csv"
        canalAssistir = random.randint(0, 2)

        canalPortuguesAssistir = ""

        if(br):
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ScTower-sc-1sjzzes-0.fwymPs.tw-tower")))
                div = driver.find_element(By.CLASS_NAME, "ScTower-sc-1sjzzes-0.fwymPs.tw-tower")

                links = div.find_elements(By.TAG_NAME, "a")

                hrefs = [link.get_attribute("href") for link in links]

                hrefsUtils = {""}
                hrefsUtils.add(hrefs[0])
                hrefsUtils.add(hrefs[3])
                hrefsUtils.add(hrefs[6])
            
                aux = 0
                canalPortuguesAssistir = ""
                for hREF in hrefsUtils:
                    try:
                        time.sleep(random.uniform(1.0, 1.5))
                        id = hREF.split("/")[-1]
                        print(f"ID achado em portugues: {id}")
                        channel = getChannelInfo(id)
                        assistido = False
                        if(aux == canalAssistir):
                            assistido = True
                            canalPortuguesAssistir = id
                        registrar_dados(nomeArquivo, channel, tempoDeVisualizacao, jogoPesquisado, id_transmissao, assistido)
                    except:
                        continue
                    aux += 1
                
                if(canalPortuguesAssistir != ""):
                    link = "https://www.twitch.tv/" + canalPortuguesAssistir
                    driver.get(link)
                    logging.info(f"Assistindo {canalPortuguesAssistir} por {tempoDeVisualizacao} segundos")
                else:
                    canalPortuguesAssistir = hrefs[0].split("/")[-1]
                    if(canalPortuguesAssistir != ""):
                        link = "https://www.twitch.tv/" + canalPortuguesAssistir
                        driver.get(link)
                        logging.info(f"Assistindo {canalPortuguesAssistir} por {tempoDeVisualizacao} segundos")
                    else:
                        logging.error("Erro ao recuperar canais em portugues")
                        i -= 1
                        continue
            except:
                logging.error(f"Algo deu errodo nos card em portugues: {e}")
                i -= 1
                continue
        else:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'article[data-a-target="card-{canalAssistir}"]')))
                canal_escolhido = driver.find_element(By.CSS_SELECTOR, f'article[data-a-target="card-{canalAssistir}"]')
            except:
                    try:
                        canalAssistir = 0
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'article[data-a-target="card-{canalAssistir}"]')))
                        canal_escolhido = driver.find_element(By.CSS_SELECTOR, f'article[data-a-target="card-{canalAssistir}"]')
                    except:
                        logging.error(f"Erro ao recuperar canais na busca por {jogoPesquisado}")
                        i -= 1
                        continue
            for j in range(3):
                print(f"Procurando canal card-{j}...")
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'a[data-a-target="card-{j}"]')))
                    canal_achado = driver.find_element(By.CSS_SELECTOR, f'a[data-a-target="card-{j}"]')
                    href = canal_achado.get_attribute("href")  
                    print(href)
                    id = href.split("/")[-2]
                    print(f"canal {id} listado nas buscas")
                    channel = getChannelInfo(id)
                    print(channel)

                    assistido = False
                    if(j == canalAssistir):
                        assistido = True
                    registrar_dados(nomeArquivo, channel, tempoDeVisualizacao, jogoPesquisado, id_transmissao, assistido)
                except:
                    continue
            canal_escolhido.click()
            logging.info(f"Assistindo {canal_escolhido.text} por {tempoDeVisualizacao} segundos")


        time.sleep(random.uniform(20, 25))
        RecuperarRecomendados(driver)
        id_transmissao += 1
        try:
            channel = getChannelInfo(canalPortuguesAssistir)

            asyncio.run(collect_twitch_chat(
                channel_id=canalPortuguesAssistir,
                oauth_token=OAUTH_TOKEN,
                csv_filename="chat_br15.csv",  
                duration=tempoDeVisualizacao,
                StreamTitle=channel.stream_title,
                StreamLanguage=channel.language,
                StreamGame=channel.last_game_name
            ))
            logging.info(f"Coletado chat do canal {canalPortuguesAssistir} por {tempoDeVisualizacao} segundos")
        except:
            logging.error(f"Erro ao coletar chat do canal {canalPortuguesAssistir}")
            pass
        logging.info(f"Tempo de visualização encerrado, busca {i+1} de {numeroBuscas} encerrada")


def acessarTwitch(driver):
    driver.get("https://www.google.com")

    try:
        driver.get("https://www.twitch.tv")
        LoginTwitch(driver, twitch_username, twitch_password, email_login, email_password, digit)
    except:
        logging.info("Erro ao logar no Twitch ou Login já realizado")
        pass

def TreinarPersona1():
    #iniciar driver
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chromeOptions)
        driver.maximize_window()
   
        acessarTwitch(driver)
        time.sleep(random.uniform(1.0, 2.0))
    except Exception as e:
        logging.error(f"Erro ao iniciar o driver: {e}")
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

    
    time.sleep(random.uniform(1.0, 2.0))
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
    time.sleep(60)


