from math import e
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def ChromeLogin(driver, google_login, google_password):
    #fazer login na conta google
    time.sleep(random.uniform(1.5, 3.0))
    driver.find_element(By.LINK_TEXT, "Fazer login").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "identifier")))
    driver.find_element(By.NAME, "identifier").send_keys(google_login)
    time.sleep(random.uniform(0.2, 0.5))
    driver.find_element(By.NAME, "identifier").send_keys(Keys.RETURN)
    time.sleep(random.uniform(1, 2.5))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Passwd")))
    driver.find_element(By.NAME, "Passwd").send_keys(google_password)
    time.sleep(random.uniform(0.2, 0.5))
    driver.find_element(By.NAME, "Passwd").send_keys(Keys.RETURN)
    time.sleep(random.uniform(1.2, 3.1))

def GetVerificationCode(driver, email_login, email_password):
    driver.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=171&ct=1739542997&rver=7.5.2211.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26cobrandid%3dab0455a0-8d03-46b9-b18b-df2f57b9e44c%26deeplink%3dowa%252f0%252f%253fstate%253d1%2526redirectTo%253daHR0cHM6Ly9vdXRsb29rLmxpdmUuY29tL21haWwvMC8%26RpsCsrfState%3d1bded2f3-996b-3a21-d95e-ec0bc4f5ef79&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=ab0455a0-8d03-46b9-b18b-df2f57b9e44c")

    time.sleep(random.uniform(20.0, 25.0))

    email_input = driver.find_element(By.NAME, "loginfmt")
    email_input.send_keys(email_login)
    email_input.send_keys(Keys.RETURN)

    time.sleep(random.uniform(20.0, 25.0))

    password_input = driver.find_element(By.NAME, "passwd")
    password_input.send_keys(email_password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(random.uniform(20.0, 25.0))

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Twitch']"))
    )
    emailsTwitch = driver.find_elements(By.XPATH, "//span[text()='Twitch']")
    print(emailsTwitch.__len__())
    for email in emailsTwitch:
        if email.is_displayed():  # Verifica se está visível
            email.click()
            break  # Para no primeiro que for clicável
    print("primeiro email aberto")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "x_header-message-code")))
    verification_div = driver.find_element(By.CLASS_NAME, "x_header-message-code")
    verification_code = verification_div.text.strip()  # Remove espaços extras
    print(verification_code)
    return verification_code


def LoginTwitch(driver, twitch_username, twitch_password, email_login, email_password):
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
        campoVerificacao = WebDriverWait(driver, 4.0).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Digit 1"]')))
        try:
            #troca de aba
            original_tab = driver.current_window_handle
            driver.execute_script("window.open('');")
            time.sleep(random.uniform(1.0, 2.0))
            driver.switch_to.window(driver.window_handles[-1])

            #Resgata o código de verificação
            verificationCode = GetVerificationCode(driver, email_login, email_password)

            #Volta para a aba original
            time.sleep(random.uniform(1.0, 2.0))
            driver.switch_to.window(original_tab)
        except Exception as e:
            print(e)
            print("Erro ao resgatar código de verificação")
            driver.quit()
            exit()

    
        time.sleep(random.uniform(1.0, 2.0))
        campoVerificacao.send_keys(verificationCode)
        time.sleep(random.uniform(1.0, 2.0))
        campoVerificacao.send_keys(Keys.RETURN)
    except:
        print("Código de verificação não solicitado")
        pass