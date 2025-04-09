import requests
from lxml import html
import pandas as pd
import time
import streamlit as st

st.set_page_config(page_title="Ações - Dados em Tempo Real", layout="wide")
st.title("📊 Dashboard de Ações - StatusInvest")

# Lista permitida
lista_acoes = ["petr4", "vale3"]

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

            dados = {
                "Ticker": codigo_acao.upper(),
                "Empresa": extrair('//h1[@title][small]/small/text()'),
                "Valor Atual": extrair('//div[@title="Valor atual do ativo"]/strong/text()'),
                "Variação Dia": extrair('//span[@title="Variação do valor do ativo com base no dia anterior"]/b/text()'),
                "Mín 52 Semanas": extrair('//div[@title="Valor mínimo das últimas 52 semanas"]/strong/text()'),
                "Mín Mês": extrair('//div[@title="Valor mínimo do mês atual"]/span[@class="sub-value"]/text()'),
                "Máx 52 Semanas": extrair('//div[@title="Valor máximo das últimas 52 semanas"]/strong/text()'),
                "Máx Mês": extrair('//div[@title="Valor máximo do mês atual"]/span[@class="sub-value"]/text()'),
                "Dividend Yield": extrair('//div[@title="Dividend Yield com base nos últimos 12 meses"]/strong/text()'),
                "Dividend Yield (soma)": extrair('//div[@title="Soma total de proventos distribuídos nos últimos 12 meses"]/span[@class="sub-value"]/text()'),
                "Valorização 12M": extrair('//div[@title="Valorização no preço do ativo com base nos últimos 12 meses"]/strong/text()'),
                "Valorização Mês": extrair('//div[@title="Valorização no preço do ativo com base no mês atual"]//b/text()'),
                "P/L": extrair("//h3[text()='P/L']/ancestor::div[contains(@title, 'mercado está disposto')]/descendant::strong[contains(@class, 'value')]/text()"),
                "PEG Ratio": extrair("//h3[text()='PEG Ratio']/following::strong[contains(@class, 'value')][1]/text()"),
                "P/VP": extrair("//h3[text()='P/VP']/ancestor::div[contains(@title, 'Facilita a análise')]/descendant::strong[contains(@class, 'value')]/text()"),
                "EV/EBITDA": extrair("//h3[text()='EV/EBITDA']/ancestor::div[contains(@title, 'O EV (Enterprise')]/descendant::strong[contains(@class, 'value')]/text()"),
                "EV/EBIT": extrair("//h3[text()='EV/EBIT']/ancestor::div[contains(@title, 'O EV (Enterprise')]/descendant::strong[contains(@class, 'value')]/text()"),
                "P/EBITDA": extrair("//h3[text()='P/EBITDA']/ancestor::div[contains(@title, 'O EBITDA permite')]/descendant::strong[contains(@class, 'value')]/text()"),
                "P/EBIT": extrair("//h3[text()='P/EBIT']/ancestor::div[contains(@title, 'Indica qual')]/descendant::strong[contains(@class, 'value')]/text()"),
                "VPA": extrair("//h3[text()='VPA']/ancestor::div[contains(@title, 'Indica qual')]/descendant::strong[contains(@class, 'value')]/text()"),
                "P/ATIVO": extrair("//h3[text()='P/Ativo']/ancestor::div[contains(@title, 'Preço da ação')]/descendant::strong[contains(@class, 'value')]/text()"),
                "LPA": extrair("//h3[text()='LPA']/ancestor::div[contains(@title, 'Indicar se a empresa')]/descendant::strong[contains(@class, 'value')]/text()"),
                "P/SR": extrair("//h3[text()='P/SR']/ancestor::div[contains(@title, 'Valor de mercado da empresa')]/descendant::strong[contains(@class, 'value')]/text()"),
                "P/Cap. Giro": extrair("//h3[text()='P/Cap. Giro']/ancestor::div[contains(@title, 'Preço da ação')]/descendant::strong[contains(@class, 'value')]/text()"),
                "P/Ativo Circ. Liq.": extrair("//h3[text()='P/Ativo Circ. Liq.']/ancestor::div[contains(@title, 'É a diferença entre o ativo')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Dív. líquida/PL": extrair("//h3[text()='Dív. líquida/PL']/ancestor::div[contains(@title, 'Indica quanto')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Dív. líquida/EBITDA": extrair("//h3[text()='Dív. líquida/EBITDA']/ancestor::div[contains(@title, 'Indica')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Dív. líquida/EBIT": extrair("//h3[text()='Dív. líquida/EBIT']/ancestor::div[contains(@title, 'Indica')]/descendant::strong[contains(@class, 'value')]/text()"),
                "PL/Ativos": extrair("//h3[text()='PL/Ativos']/ancestor::div[contains(@title, 'O Patrimônio')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Passivos/Ativos": extrair("//h3[text()='Passivos/Ativos']/ancestor::div[contains(@title, 'Calculo')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Liq. corrente": extrair("//h3[text()='Liq. corrente']/ancestor::div[contains(@title, 'Indica')]/descendant::strong[contains(@class, 'value')]/text()"),
                "M. Bruta": extrair("//h3[text()='M. Bruta']/ancestor::div[contains(@title, 'Mede')]/descendant::strong[contains(@class, 'value')]/text()"),
                "M. EBITDA": extrair("//h3[text()='M. EBITDA']/ancestor::div[contains(@title, 'É o percentual')]/descendant::strong[contains(@class, 'value')]/text()"),
                "M. EBIT": extrair("//h3[text()='M. EBIT']/ancestor::div[contains(@title, 'Útil')]/descendant::strong[contains(@class, 'value')]/text()"),
                "M. Líquida": extrair("//h3[text()='M. Líquida']/ancestor::div[contains(@title, 'Revela')]/descendant::strong[contains(@class, 'value')]/text()"),
                "ROE": extrair("//h3[text()='ROE']/ancestor::div[contains(@title, 'Mede')]/descendant::strong[contains(@class, 'value')]/text()"),
                "ROA": extrair("//h3[text()='ROA']/ancestor::div[contains(@title, 'O retorno')]/descendant::strong[contains(@class, 'value')]/text()"),
                "ROIC": extrair("//h3[text()='ROIC']/ancestor::div[contains(@title, 'Mede')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Giro ativos": extrair("//h3[text()='Giro ativos']/ancestor::div[contains(@title, 'Mede')]/descendant::strong[contains(@class, 'value')]/text()"),
                "CAGR Receitas 5 anos": extrair("//h3[text()='CAGR Receitas 5 anos']/ancestor::div[contains(@title, 'O CAGR')]/descendant::strong[contains(@class, 'value')]/text()"),
                "CAGR Lucros 5 anos": extrair("//h3[text()='CAGR Lucros 5 anos']/ancestor::div[contains(@title, 'O CAGR')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Tipo": extrair("//h3[text()='Tipo']/following-sibling::strong[@class='value']/text()"),
                "Tag Along": extrair("//span[contains(., 'Tag Along')]/ancestor::div[2]//strong[@class='value']/text()"),
                "Liq. méd. diária": extrair("//span[contains(., 'Liquidez média diária') or contains(., 'Liq. méd. diária')]/ancestor::div[2]//strong[@class='value']/text()"),
                "Patrimônio líquido": extrair("//h3[text()='Patrimônio líquido']/ancestor::div[contains(@title, 'É uma')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Ativos": extrair("//h3[text()='Ativos']/ancestor::div[contains(@title, 'Ativo')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Ativo circulante": extrair("//h3[text()='Ativo circulante']/ancestor::div[contains(@title, 'Ativo')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Dívida bruta": extrair("//h3[text()='Dívida bruta']/ancestor::div[contains(@title, 'Representa')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Disponibilidade": extrair("//h3[text()='Disponibilidade']/ancestor::div[contains(@title, 'Representa')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Dívida líquida": extrair("//h3[text()='Dívida líquida']/ancestor::div[contains(@title, 'A dívida')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Valor de mercado": extrair("//h3[text()='Valor de mercado']/ancestor::div[contains(@title, 'O valor')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Valor de firma": extrair("//h3[text()='Valor de firma']/ancestor::div[contains(@title, 'Soma do valor')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Nº total de papéis": extrair("//h3[span[contains(text(), 'Nº total de papéis')]]/following-sibling::strong/text()"),
                "Segmento de listagem": extrair("//h3[text()='Segmento de listagem']/ancestor::div[contains(@title, 'Segmento')]/descendant::strong[contains(@class, 'value')]/text()"),
                "Free Float": extrair("//h3[text()='Free Float']/../../following-sibling::strong[@class='value']/text()"),
                "Setor de Atuação": extrair("//span[contains(text(), 'Setor de Atuação')]/following::strong[@class='value'][1]/text()"),
                "Subsetor de Atuação": extrair("//span[contains(text(), 'Subsetor de Atuação')]/following::strong[@class='value'][1]/text()"),
                "Subsetor de Atuação": extrair("//span[contains(text(), 'Subsetor de Atuação')]/following::strong[@class='value'][1]/text()"),
                "Segmento de Atuação": extrair("//span[contains(text(), 'Segmento de Atuação')]/following::strong[@class='value'][1]/text()")
            }

            return dados
        else:
            print(f"Erro ao acessar {codigo_acao}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao buscar {codigo_acao}: {e}")
        return None

# Entrada de tickers
tickers_input = st.text_input("Digite os tickers separados por vírgula:", "petr4,vale3")
tickers_digitados = [t.strip().lower() for t in tickers_input.split(',') if t.strip()]

# Filtra apenas os tickers autorizados
tickers_validos = [t for t in tickers_digitados if t in lista_acoes]
tickers_invalidos = [t for t in tickers_digitados if t not in lista_acoes]

if tickers_invalidos:
    st.warning(f"⚠️ Os seguintes tickers não estão disponíveis no momento: {', '.join(tickers_invalidos)}")

if st.button("🔄 Atualizar Dados"):
    if not tickers_validos:
        st.error("❌ Nenhum ticker válido informado.")
    else:
        dados_extraidos = []
        with st.spinner("Buscando dados..."):
            for ticker in tickers_validos:
                dados = extrair_dados_acao(ticker)
                if dados:
                    dados_extraidos.append(dados)
                time.sleep(10)

        if dados_extraidos:
            df_resultado = pd.DataFrame(dados_extraidos)
            st.success("✅ Dados atualizados com sucesso!")
            st.dataframe(df_resultado)
        else:
            st.error("❌ Nenhum dado foi encontrado.")
