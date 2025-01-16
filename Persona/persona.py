from math import e
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


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

def ChromeLogin(driver):
    #fazer login na conta google
    time.sleep(random.uniform(1.5, 3.0))
    driver.find_element(By.LINK_TEXT, "Fazer login").click()
    driver.find_element(By.NAME, "identifier").send_keys(google_login)
    time.sleep(random.uniform(0.2, 0.5))
    driver.find_element(By.NAME, "identifier").send_keys(Keys.RETURN)
    time.sleep(random.uniform(1, 2.5))
    driver.find_element(By.NAME, "Passwd").send_keys(google_password)
    time.sleep(random.uniform(0.2, 0.5))
    driver.find_element(By.NAME, "Passwd").send_keys(Keys.RETURN)
    time.sleep(random.uniform(1.2, 3.1))

def GetVerificationCode(driver):
    driver.get("https://mail.google.com/mail/u/0/#inbox")
    time.sleep(random.uniform(1.0, 3.0))

    firstEmail = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '(//tr[contains(@class, "zA")])[1]'))
    )
    firstEmail.click()
    time.sleep(random.uniform(4.0, 6.0))
            #nao esta funcionando mais, nao faço ideia do porque
    element  = driver.find_element(By.XPATH, '//div[@style="background:#faf9fa;border:1px solid #dad8de;text-align:center;padding:5px;margin:0 0 5px 0;font-size:24px;line-height:1.5;width:80%"]')

    codVerificacao = element.text
    return codVerificacao


def LoginTwitch(driver):
     #clicar em entrar
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button/div/div").click()
    time.sleep(random.uniform(4.0, 6.0))
    # Clicar em username
    driver.find_element(By.ID, "login-username").send_keys(twitch_username)
    time.sleep(random.uniform(2.0, 4.0))
    # Clicar em password
    driver.find_element(By.ID, "password-input").send_keys(twitch_password)
    time.sleep(random.uniform(0.5, 1.2))
    driver.find_element(By.ID, "password-input").send_keys(Keys.RETURN)
    time.sleep(random.uniform(2.0, 5.0))
    try:
        #Se pedir código de verificação
        campoVerificacao = WebDriverWait(driver, 4.0).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Dígito 1"]')))
        try:
            #troca de aba
            original_tab = driver.current_window_handle
            driver.execute_script("window.open('');")
            time.sleep(random.uniform(1.0, 2.0))
            driver.switch_to.window(driver.window_handles[-1])

            #Resgata o código de verificação
            verificationCode = GetVerificationCode(driver)

            #Volta para a aba original
            time.sleep(random.uniform(1.0, 2.0))
            driver.switch_to.window(original_tab)
        except:
            print("Erro ao tentar resgatar o código de verificação")
            driver.quit()
            exit()
    
        time.sleep(random.uniform(1.0, 2.0))
        campoVerificacao.send_keys(verificationCode)
    except:
        print("Código de verificação não solicitado")
        pass


def Treino():

    jogoPesquisado = random.choice(list(jogosAssistir))

   
    barraBusca = driver.find_element('css selector', '[placeholder="Buscar"]')
    barraBusca.send_keys(jogoPesquisado)
    
    time.sleep(random.uniform(1.0, 2.0))

    barraBusca.send_keys(Keys.RETURN)

    time.sleep(random.uniform(1.5, 2.5))

    """ 
    CSS SELECTOR DOS 3 PRIMEIROS RESULTADOS DE PESQUISA (FIREFOX)
    .search-results > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(1) > a:nth-child(1)
    .search-results > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(1) > a:nth-child(1)
    .search-results > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > strong:nth-child(1) > a:nth-child(1)
    """

    """
    XPATH DOS 3 PRIMEIROS RESULTADOS DE PESQUISA (CHROME)
    //*[@id="root"]/div/div[1]/div/main/div[1]/div[3]/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div/div/div[1]/div/strong/a
    //*[@id="root"]/div/div[1]/div/main/div[1]/div[3]/div/div/div/div/div[1]/div[1]/div[3]/div/div/div/div/div[1]/div/strong/a
    //*[@id="root"]/div/div[1]/div/main/div[1]/div[3]/div/div/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div/strong/a
    """
    #videoAssistido = random.randint(1, 3)

    #CONSERTAR, PAROU DE FUNCIONAR
    #Talvez valha a pena usar a posição absoluta dos videos na página, ao inves do css, pois aparentemente este muda.
    videoAssistido = 2
    if(videoAssistido == 1):
        video = driver.find_element(By.CLASS_NAME, 'ScCoreLink-sc-16kq0mq-0 jRnnHH tw-link')
    elif(videoAssistido == 2):
        video = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/main/div[1]/div[3]/div/div/div/div/div[1]/div[1]/div[3]/div/div/div/div/div[1]/div/strong/a')
    else:
        video = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/main/div[1]/div[3]/div/div/div/div/div[1]/div[1]/div[4]/div/div/div/div/div[1]/div/strong/a')

    video.click()
    time.wait(tempoDeVisualizacao)

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
    driver.maximize_window()
    driver.get("https://www.google.com")
except:
    exit()

try:
    ChromeLogin(driver)
    time.sleep(random.uniform(3.0, 5.5))
except:
    pass

try:
    driver.get("https://www.twitch.tv")
    LoginTwitch(driver)
except:
    print("Erro ao logar no Twitch ou Login já realizado")

try:
    Treino()
except Exception as e:
    print(f"Erro ao clicar no canal: {e}")
    try:
        first_channel = driver.find_element(By.XPATH, '(//div[@class="Layout-sc-1xcs6mc-0 cwtKyw side-nav-card"])[1]/a')
        first_channel.click()
        print("Primeiro canal clicado com sucesso!")
    except Exception as e:
        print(f"Erro ao clicar no elemento: {e}")
        pass


#Tempo de visualização
time.sleep(random.uniform(540.0, 720.0))
driver.quit()

"""
#TO DO
- Registrar informações sobre o treino em um csv
- Adicionar um sistema de log
- Possibilitar o treino de mais de uma persona
- tornar o programa um script que será rodado por x tempo e depois encerrado
"""