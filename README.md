# Interface Gráfica - Captador de Temperatura e Umidade (São Paulo)

Este projeto consiste em uma aplicação Python com interface gráfica feita em **Tkinter** que acessa automaticamente um site de previsão do tempo, captura a **temperatura e umidade** do ar da cidade de **São Paulo**, e armazena esses dados em uma **planilha Excel** com data e hora.

## Objetivo

Desenvolver uma automação prática com interface amigável que simula um projeto real, aplicando conceitos de:

- Web scraping com **Selenium**
- Manipulação de planilhas com **OpenPyXL**
- Interface gráfica com **Tkinter**
- Controle de versão com **Git**
- Armazenamento de projeto no **GitHub**

## Funcionalidades

- Captura temperatura atual de SP
- Captura umidade do ar
- Armazena os dados em um Excel com data/hora
- Interface gráfica simples com botão de execução

## Tecnologias Usadas

- Python 3.x
- Selenium
- OpenPyXL
- Tkinter

## Instalação

```bash
git clone https://github.com/leobrboy/Interface-grafica.git
cd Interface-grafica
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Desenvolvido por

**Leonardo Ramiro Santos do Nascimento**  
GitHub: [@leobrboy](https://github.com/leobrboy)
