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

        temperatura_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "temperature__value"))
        )

        umidade_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Umidade') or contains(text(), 'umidade')]"))
        )

        temperatura = temperatura_element.text.strip().replace("°", "")
        umidade = umidade_element.text.strip().split(":")[-1].strip()
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if not os.path.exists(ARQUIVO_EXCEL):
            wb = Workbook()
            ws = wb.active
            ws.append(["Data/Hora", "Temperatura (°C)", "Umidade"])
        else:
            wb = load_workbook(ARQUIVO_EXCEL)
            ws = wb.active

        ws.append([data_hora, temperatura, umidade])
        wb.save(ARQUIVO_EXCEL)

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
