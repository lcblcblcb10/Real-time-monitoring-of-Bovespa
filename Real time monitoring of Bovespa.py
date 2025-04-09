import requests
from lxml import html
import pandas as pd
import streamlit as st
import time

st.set_page_config(page_title="Ações - PETR4 e VALE3", layout="wide")
st.title("📊 Dados de Ações - PETR4 e VALE3")

def extrair_dados_acao(codigo_acao):
    url = f"https://statusinvest.com.br/acoes/{codigo_acao.lower()}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tree = html.fromstring(response.content)

            def extrair(xpath_expr):
                result = tree.xpath(xpath_expr)
                return result[0].strip() if result else "Não encontrado"

            return {
                "Ticker": codigo_acao.upper(),
                "Empresa": extrair('//h1[@title][small]/small/text()'),
                "Valor Atual": extrair('//div[@title="Valor atual do ativo"]/strong/text()'),
                "Variação Dia": extrair('//span[@title="Variação do valor do ativo com base no dia anterior"]/b/text()'),
                "Dividend Yield": extrair('//div[@title="Dividend Yield com base nos últimos 12 meses"]/strong/text()'),
                "P/L": extrair("//h3[text()='P/L']/ancestor::div[contains(@title, 'mercado está disposto')]/descendant::strong[contains(@class, 'value')]/text()"),
                "ROE": extrair("//h3[text()='ROE']/ancestor::div[contains(@title, 'Mede')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Liq. méd. diária": extrair("//span[contains(., 'Liquidez média diária') or contains(., 'Liq. méd. diária')]/ancestor::div[2]//strong[@class='value']/text()"),
                "Valor de mercado": extrair("//h3[text()='Valor de mercado']/ancestor::div[contains(@title, 'O valor')]/descendant::strong[contains(@class, 'value')]/text()"),
            }
        else:
            return None
    except:
        return None

# Tickers fixos
tickers = ["petr4", "vale3"]
dados_extraidos = []

with st.spinner("Buscando dados..."):
    for ticker in tickers:
        dados = extrair_dados_acao(ticker)
        if dados:
            dados_extraidos.append(dados)
        time.sleep(1)

if dados_extraidos:
    df_resultado = pd.DataFrame(dados_extraidos)
    st.dataframe(df_resultado)
else:
    st.error("❌ Não foi possível obter os dados.")