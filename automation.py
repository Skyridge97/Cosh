import os
import time
import random
import string
import signal
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# --- Configuration ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

# --- Gestion de l'arrêt propre ---
def signal_handler(sig, frame):
    print('Arrêt du script...')
    if 'driver' in globals() and driver:
        driver.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# --- Fonctions Utilitaires ---
def get_config():
    config = {
        'referral_link': os.environ.get("REFERRAL_LINK"),
        'accounts_per_hour': int(os.environ.get("ACCOUNTS_PER_HOUR", "3")),
        'pause_hours': os.environ.get("PAUSE_HOURS", "2-4,12-14").split(","),
    }
    if not config['referral_link']:
        print("ERREUR: REFERRAL_LINK non définie")
        sys.exit(1)
    return config

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(f'--user-agent={random.choice(USER_AGENTS)}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--display=:99')
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(length))
    if not any(c.isupper() for c in password):
        password = password[:-1] + random.choice(string.ascii_uppercase)
    return password

def human_like_delay(min_seconds=0.5, max_seconds=2.0):
    time.sleep(random.uniform(min_seconds, max_seconds))

def get_temp_email(driver):
    print("Obtention d'un email temporaire...")
    driver.get("https://temp-mail.org/fr/option/refresh/")
    human_like_delay(3, 5)
    try:
        email_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "mail"))
        )
        return email_element.get_attribute("value")
    except Exception as e:
        print(f"Erreur email: {e}")
        return None

def register_account(driver, referral_link, temp_email, password):
    try:
        driver.get(referral_link)
        human_like_delay(2, 5)
        
        # Adapter ces sélecteurs selon ton site
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        human_like_type(email_field, temp_email)
        
        password_field = driver.find_element(By.ID, "password")
        human_like_type(password_field, password)
        
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()
        
        human_like_delay(5, 10)
        return True
    except Exception as e:
        print(f"Erreur inscription: {e}")
        return False

def human_like_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

# --- Boucle Principale ---
def main():
    config = get_config()
    print(f"🚀 Démarrage du script - Lien: {config['referral_link']}")
    
    while True:
        current_hour = time.localtime().tm_hour
        
        # Vérifier les heures de pause
        in_pause = False
        for pause_range in config['pause_hours']:
            start, end = map(int, pause_range.split("-"))
            if start <= current_hour < end:
                in_pause = True
                print(f"⏸️ Pause programmée ({current_hour}h)")
                time.sleep(3600)
                break
        
        if in_pause:
            continue
        
        # Création des comptes
        for i in range(config['accounts_per_hour']):
            print(f"\n📝 Création du compte {i+1}/{config['accounts_per_hour']}")
            
            driver = setup_driver()
            try:
                temp_email = get_temp_email(driver)
                if not temp_email:
                    continue
                
                password = generate_password()
                print(f"📧 Email: {temp_email}")
                print(f"🔑 Mot de passe: {password}")
                
                if register_account(driver, config['referral_link'], temp_email, password):
                    print("✅ Compte créé avec succès")
                else:
                    print("❌ Échec de création")
                
            except Exception as e:
                print(f"❌ Erreur: {e}")
            finally:
                driver.quit()
            
            # Pause entre les comptes
            delay = random.uniform(600, 1200)
            print(f"⏳ Pause de {delay/60:.1f} minutes...")
            time.sleep(delay)
        
        # Pause avant la prochaine heure
        time.sleep(60)

if __name__ == "__main__":
    main()
