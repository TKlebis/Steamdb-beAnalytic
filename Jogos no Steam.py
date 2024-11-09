#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install webdriver-manager


# In[ ]:


pip install -U selenium webdriver-manager


# In[ ]:


conda install -c conda-forge selenium


# In[8]:


pip install selenium


# In[ ]:


pip show selenium


# In[10]:


pip install --upgrade selenium


# In[ ]:


import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# Configuração do WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# URL da página
url = 'https://steamdb.info/sales/'

# Abrir a página
driver.get(url)

try:
    # Espera até que o seletor de quantidade de itens esteja presente
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "DataTables_Table_0_length")))

    # Encontrar o seletor de quantidade de itens por página
    select_element = driver.find_element(By.NAME, "DataTables_Table_0_length")
    select = Select(select_element)
    
    # Selecionar a opção "All (slow)" para mostrar todos os itens
    select.select_by_visible_text("All (slow)")

    # Aguardar o carregamento completo dos dados
    time.sleep(5)  # Aumente o tempo de espera para garantir o carregamento completo

    # Rolar a página para baixo para carregar mais dados
    for _ in range(100):  # Ajuste conforme necessário para carregar todos os dados
        driver.execute_script("window.scrollBy(0, 1000);")  # Rolar a página
        time.sleep(4)  # Aumente o tempo de espera entre cada rolagem

    # Coletar todas as linhas da tabela de jogos
    linhas = driver.find_elements(By.CSS_SELECTOR, "tr.app")

    # Lista para armazenar dados de cada linha
    dados = []

    for index, linha in enumerate(linhas, start=1):
        # Coletar todas as células de uma linha
        celulas = linha.find_elements(By.TAG_NAME, "td")
        
        # Verificar se o número de células está de acordo com o esperado
        if len(celulas) >= 8:  # Garantir que pegamos o número certo de células
            jogo = celulas[1].text  # Nome do jogo
            desconto = celulas[2].text  # Desconto
            preco = celulas[3].text  # Preço
            avaliacao = celulas[4].text  # Avaliação
            liberar = celulas[5].text  # Data de lançamento
            
            # Coletar o atributo 'title' para a coluna 'Termina'
            termina = celulas[6].get_attribute('title') if celulas[6].get_attribute('title') else celulas[6].text.strip()
            
            # Coletar o atributo 'title' para a coluna 'Iniciado'
            iniciado = celulas[7].get_attribute('title') if len(celulas) > 7 else 'N/A'
            
            # Adiciona a linha aos dados, incluindo um ID único para cada jogo
            dados.append({
                'ID': index,  # ID progressivo
                'Jogo': jogo,
                'Desconto': desconto,
                'Preço': preco,
                'Avaliação': avaliacao,
                'Liberar': liberar,
                'Termina': termina,
                'Iniciado': iniciado
            })

    # Coletar todas as células que contêm datas detalhadas em UTC e GMT-3
    celulas_com_datas = driver.find_elements(By.XPATH, "//td[contains(@title, 'UTC')]")
    
    # Lista para armazenar as datas extraídas
    datas_extracao = []

    for celula in celulas_com_datas:
        data = celula.get_attribute('title')
        if data:
            datas_extracao.append(data)
        else:
            datas_extracao.append("NA")  # Substituir dados ausentes por "NA"

    # Criar um DataFrame com as datas coletadas
    df_datas = pd.DataFrame(datas_extracao, columns=["Datas"])

    # Garantir que as colunas sejam corretamente combinadas
    for i, row in df_datas.iterrows():
        if i < len(dados):  # Garantir que o índice exista em ambas as listas
            dados[i]['Datas'] = row['Datas']

    # Criar um DataFrame final com todos os dados
    df = pd.DataFrame(dados)

    # Remover qualquer coluna duplicada (se houver)
    if 'ID' in df.columns:
        df = df.loc[:, ~df.columns.duplicated()]

    # Renomear as colunas conforme solicitado
    df = df.rename(columns={
        'Jogo': 'ID',
        'Desconto': 'Jogo',
        'Preço': 'Desconto',
        'Avaliação': 'Preço',
        'Liberar': 'Avaliação',
        'Termina': 'Liberar',
        'Iniciado': 'Termina'
    })

    # Salvar o DataFrame em um arquivo CSV
    output_path = '/mnt/data/jogos_descontos_completo.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')

    # Mostrar o DataFrame
    print(df)

except Exception as e:
    print(f"Erro ao coletar dados: {e}")
finally:
    # Fechar o navegador após a execução
    driver.quit()

# Link para download do arquivo CSV
from IPython.display import FileLink
FileLink(output_path)


# In[ ]:


df.to_csv('jogos_descontos_divididos.csv', index=False, encoding='utf-8')

print("Arquivo CSV gerado com sucesso!")


# In[ ]:


from IPython.display import FileLink

# Gerar o link de download para o arquivo
FileLink('jogos_descontos_divididos.csv')

