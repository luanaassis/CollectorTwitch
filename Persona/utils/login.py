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
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Fazer login")))
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

def GetVerificationCode(driver):
    driver.get("https://mail.google.com/mail/u/0/#inbox")
    time.sleep(random.uniform(1.0, 3.0))

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
    time.sleep(random.uniform(4.0, 6.0))
            #nao esta funcionando mais, nao faço ideia do porque
    element  = driver.find_element(By.XPATH, '//div[@style="background:#faf9fa;border:1px solid #dad8de;text-align:center;padding:5px;margin:0 0 5px 0;font-size:24px;line-height:1.5;width:80%"]')
    print(element.text)
    codVerificacao = element.text
    return codVerificacao


def LoginTwitch(driver, twitch_username, twitch_password):
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
        except Exception as e:
            print(e)
            print("Erro ao resgatar código de verificação")
            driver.quit()
            exit()

    
        time.sleep(random.uniform(1.0, 2.0))
        campoVerificacao.send_keys(verificationCode)
        campoVerificacao.send_keys(Keys.RETURN)
        time.sleep(random.uniform(2.0, 5.0))
    except:
        print("Código de verificação não solicitado")
        pass