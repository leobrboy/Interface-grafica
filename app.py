from tkinter import Tk, Button, Label
from datetime import datetime
from openpyxl import Workbook, load_workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import traceback

ARQUIVO_EXCEL = "dados_temperatura.xlsx"

def buscar_dados():
    status_label.config(text="Buscando dados...")

    options = Options()
    # options.add_argument("--headless")  # Desativado para ver o navegador
# options.add_argument("--disable-gpu")

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.climatempo.com.br/previsao-do-tempo/cidade/558/saopaulo-sp")

        # Close cookie consent popup if present
        try:
            consent_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
            )
            consent_button.click()
        except:
            pass

        temperatura_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Temperatura')]/following-sibling::*[1] | //td[contains(text(), 'Temperatura')]/following-sibling::td"))
        )

        umidade_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Umidade')]/following-sibling::*[1] | //td[contains(text(), 'Umidade')]/following-sibling::td"))
        )

        temperatura = temperatura_element.text.strip().replace("°", "")
        umidade = umidade_element.text.strip()
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if not os.path.exists(ARQUIVO_EXCEL):
            wb = Workbook()
            ws = wb.active
            ws.append(["Data/Hora", "Temperatura (°C)", "Umidade"])
        else:
            wb = load_workbook(ARQUIVO_EXCEL)
            ws = wb.active

        # Clean temperatura string to handle multiple lines or values
        temperatura_clean = temperatura.split('\n')[0].strip()
        umidade_clean = umidade.replace('%','').split('\n')[0].strip()
        temperatura_str = f"{int(float(temperatura_clean))}°C"
        umidade_str = f"{int(umidade_clean)}%"
        ws.append([data_hora, temperatura_str, umidade_str])
        try:
            wb.save(ARQUIVO_EXCEL)
        except PermissionError:
            status_label.config(text="Erro: Feche o arquivo Excel antes de salvar.")
            return
 
        status_label.config(text=f"Capturado: {temperatura}°C, {umidade}")
    except Exception as e:
        status_label.config(text="Erro ao captar dados.")
        print("Erro:", e)
        traceback.print_exc()
    finally:
        driver.quit()

# Interface gráfica com Tkinter
app = Tk()
app.title("Captura de Temperatura SP (ClimaTempo)")
app.geometry("300x180")

titulo = Label(app, text="Temperatura São Paulo", font=("Arial", 14))
titulo.pack(pady=10)

botao = Button(app, text="Buscar previsão", command=buscar_dados, width=20, height=2, bg="lightblue")
botao.pack(pady=10)

status_label = Label(app, text="", font=("Arial", 10))
status_label.pack()

app.mainloop()
