import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Lista de ações permitidas
lista_acoes = ["petr4", "vale3"]

# Função para iniciar o driver
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# Função para buscar dados da ação com Selenium
def buscar_dados_acao(acao):
    acao = acao.lower()
    if acao not in lista_acoes:
        return None

    url = f"https://statusinvest.com.br/acoes/{acao}"
    driver = iniciar_driver()
    driver.get(url)

    # Espera a página carregar
    time.sleep(3)

    try:
        preco = driver.find_element(By.XPATH, "//strong[@id='headerTickerPrice']").text
        #dy = driver.find_element(By.XPATH, "//div[contains(@class, 'top-info')]/div[3]//strong").text
        #pvp = driver.find_element(By.XPATH, "//div[contains(@class, 'top-info')]/div[4]//strong").text
        #roe = driver.find_element(By.XPATH, "//div[contains(@class, 'top-info')]/div[5]//strong").text
        #liquidez = driver.find_element(By.XPATH, "//div[contains(@class, 'top-info')]/div[7]//strong").text
        #setor = driver.find_element(By.XPATH, "//div[@class='info w-100']/div[1]/div/a").text
        #subsetor = driver.find_element(By.XPATH, "//div[@class='info w-100']/div[2]/div/a").text

        driver.quit()
        return {
            "Preço atual": preco#,
            #"Dividend Yield": dy,
            #"P/VP": pvp,
            #"ROE": roe,
            #"Liquidez Média Diária": liquidez,
            #"Setor": setor,
            #"Subsetor": subsetor
        }
    except Exception as e:
        driver.quit()
        return None

# --- Streamlit App ---
st.set_page_config(page_title="Dashboard de Ações", layout="wide")
st.title("📊 Dashboard de Ações - StatusInvest (com Selenium)")

acao_input = st.text_input("Digite o código da ação (ex: PETR4, VALE3):").lower()

if acao_input:
    if acao_input not in lista_acoes:
        st.warning("⚠️ Ação não permitida. Use apenas: petr4 ou vale3.")
    else:
        if st.button("🔄 Atualizar dados"):
            with st.spinner("Buscando dados..."):
                dados = buscar_dados_acao(acao_input)
                if dados:
                    st.success(f"✅ Dados da ação {acao_input.upper()}:")
                    for key, value in dados.items():
                        st.write(f"**{key}**: {value}")
                else:
                    st.error("❌ Nenhum dado foi encontrado.")