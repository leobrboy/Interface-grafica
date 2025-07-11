from tkinter import Tk, Button, Label
from datetime import datetime
from openpyxl import Workbook, load_workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

ARQUIVO_EXCEL = "dados_temperatura.xlsx"

def buscar_dados():
    status_label.config(text="Buscando dados...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    # Caminho direto para o ChromeDriver
    driver = webdriver.Chrome(executable_path="C:/WebDrivers/chromedriver.exe", options=options)
    driver.get("https://www.google.com/search?q=temperatura+em+São+Paulo")

    try:
        temperatura = driver.find_element(By.ID, "wob_tm").text
        umidade = driver.find_element(By.ID, "wob_hm").text
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
    finally:
        driver.quit()

app = Tk()
app.title("Captura de Temperatura SP")
app.geometry("300x180")

titulo = Label(app, text="Temperatura São Paulo", font=("Arial", 14))
titulo.pack(pady=10)

botao = Button(app, text="Buscar previsão", command=buscar_dados, width=20, height=2, bg="lightblue")
botao.pack(pady=10)

status_label = Label(app, text="", font=("Arial", 10))
status_label.pack()

app.mainloop()
