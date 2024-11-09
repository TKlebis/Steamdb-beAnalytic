# ![image](https://github.com/user-attachments/assets/c3ec3aa0-0c01-40b2-8fae-43c42fc67c3b) Engenharia de Dados de Jogos no Steam
![Python Versions](https://img.shields.io/pypi/pyversions/st_pages.svg)

*Autor:*  [Thiago Klebis](https://www.linkedin.com/in/thiagoklebis/)

Este repositório contém um conjunto de consultas SQL projetadas para analisar dados de jogos do Steam, extraídos de uma planilha do Google Sheets e carregados no BigQuery. As consultas abordam diversos aspectos, como descontos, avaliações, preços e datas de liberação dos jogos.

## Objetivo
O objetivo deste repositório é fornecer insights sobre os jogos, como identificar as melhores ofertas, jogos mais bem avaliados, promoções em andamento e muito mais. Utilizando BigQuery e SQL, a análise se concentra em:

- Descontos aplicados nos jogos
- Avaliação dos jogos
- Preços e variações ao longo do tempo
- Promoções e datas de liberação

# ![image](https://github.com/user-attachments/assets/d6632221-5009-4c5a-b5fb-a21121e5ed2e) Captação e Análise de Dados com Python e Selenium

## Objetivo
O código tem como objetivo capturar dados sobre promoções de jogos, como nome, desconto, preço, avaliação, datas de início e término, e outros detalhes diretamente da página da SteamDB. Esses dados são extraídos e salvos em um arquivo CSV para análise posterior.
## Dependências

O código depende das seguintes bibliotecas:

- pandas: Para manipulação de dados e criação de DataFrame.
- selenium: Para automação de navegação na web e coleta de dados.
- webdriver_manager: Para gerenciamento automático do driver do Chrome.

Você pode instalar as bibliotecas necessárias com o comando:
```python
pip install pandas selenium webdriver-manager
```

## Etapas do Código

1. Configuração do WebDriver
O WebDriver do Selenium é configurado com o uso do webdriver_manager, que cuida da instalação e atualização do driver do Chrome de maneira automatizada.
```python
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
```

2. Acesso à Página e Interação
A página de promoções da SteamDB é acessada por meio da URL e o código aguarda até que o seletor da quantidade de itens por página esteja presente.
```python
# URL da página
url = 'https://steamdb.info/sales/'

# Abrir a página
driver.get(url)

# Espera até que o seletor de quantidade de itens esteja presente
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "DataTables_Table_0_length")))
```
3. Seleção de Quantidade de Itens
Uma vez carregada a página, o código seleciona a opção "All (slow)" para exibir todos os itens da página. Isso é feito utilizando o Selenium para interagir com o seletor dropdown.
```python
select_element = driver.find_element(By.NAME, "DataTables_Table_0_length")
select = Select(select_element)

# Seleciona a opção "All (slow)" para mostrar todos os itens
select.select_by_visible_text("All (slow)")

# Aguardar o carregamento completo dos dados
time.sleep(30)  # Aumente o tempo de espera para garantir o carregamento completo
```
4. Rolagem da Página para Carregar Todos os Itens
Como a página possui muitos itens e eles são carregados dinamicamente à medida que o usuário rola a página, o código simula a rolagem da página várias vezes para garantir que todos os dados sejam carregados.
```python
# Rolar a página para baixo para carregar mais dados
for _ in range(90):  # Ajuste conforme necessário para carregar todos os dados
    driver.execute_script("window.scrollBy(0, 1000);")  # Rolar a página
    time.sleep(2)  # Aumente o tempo de espera entre cada rolagem
```

5. Coleta de Dados
Após o carregamento completo da página, o código coleta os dados das promoções, como nome do jogo, desconto, preço, avaliação, datas de início e término, e os armazena em uma lista de dicionários.
```python
# Coletar todas as linhas da tabela de jogos
linhas = driver.find_elements(By.CSS_SELECTOR, "tr.app")

# Lista para armazenar dados de cada linha
dados = []

for index, linha in enumerate(linhas, start=1):
    # Coletar todas as células de uma linha
    celulas = linha.find_elements(By.TAG_NAME, "td")
    
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
        
        # Adiciona a linha aos dados
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
```
6. Extração de Datas
O código também coleta as datas detalhadas (em UTC e GMT-3) dos jogos em promoção, utilizando o método get_attribute para pegar os valores dos atributos title.
```python
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
```

7. Salvar o DataFrame como CSV, Mensagem de sucesso e Gerar o link de download

```python
df.to_csv('jogos_descontos_divididos.csv', index=False, encoding='utf-8')
print("Arquivo CSV gerado com sucesso!")

from IPython.display import FileLink

FileLink('jogos_descontos_divididos.csv')
```

# ![image](https://github.com/user-attachments/assets/1af98db9-6972-4cea-b78d-31296cb1c7cd) Importar o Arquivo CSV para o Google Sheets

Após a coleta e organização dos dados de descontos de jogos, foi gerado um arquivo CSV contendo essas informações. Em seguida, esse arquivo foi importado para o Google Sheets para facilitar o processamento, manipulação e compartilhamento dos dados. A planilha foi nomeada como "steamdb beAnalytic".

## Passos Realizados:
1. Geração do Arquivo CSV:
O arquivo CSV foi gerado a partir de dados extraídos por meio de um script Python utilizando a biblioteca pandas. O arquivo contém informações sobre jogos, descontos, preços, avaliações, entre outros.

2. Importação para o Google Sheets:
O arquivo CSV foi importado manualmente para o Google Sheets através da interface do Google Sheets, permitindo uma visualização e manipulação mais ágil dos dados.

3. Renomeação da Planilha:
Após a importação, a aba da planilha foi renomeada para "steamdb beAnalytic" para refletir o nome do conjunto de dados.
Com a planilha no Google Sheets, ficou mais fácil trabalhar com os dados, realizar análises e gerar relatórios, além de possibilitar o compartilhamento e o acompanhamento em tempo real das informações.

# ![image](https://github.com/user-attachments/assets/d5f2e704-8931-4b67-8126-fd4e2fc0fc6b) Vinculação do Google Sheets ao Google BigQuery e Execução das Queries

Após importar o arquivo CSV para o Google Sheets e criar a tabela com os dados, foi realizada a integração da planilha com o Google BigQuery. A seguir, as queries foram executadas para realizar análises e obter informações valiosas dos dados coletados.

## Passos Realizados:
1. Criação da Tabela no Google Sheets:
A partir do arquivo CSV importado, foi criada uma tabela no Google Sheets com as colunas e dados estruturados adequadamente.

2. Vinculação do Google Sheets ao Google BigQuery:
O Google Sheets foi vinculado ao Google BigQuery, permitindo a execução de queries diretamente sobre os dados armazenados na planilha.
Isso foi feito utilizando a funcionalidade de Conectar Google Sheets ao BigQuery, onde a planilha foi definida como uma tabela externa em BigQuery, permitindo consultas SQL para análise.

3. Execução das Queries:
A seguir, as queries SQL foram executadas no Google BigQuery para realizar análises e extrair as informações necessárias.

## As queries executadas são as seguintes:

1. [Jogos com Desconto](https://docs.google.com/spreadsheets/d/1jk2vONMzgBZaMW2ME8-ouFx1BYEY2tvD0Ecn2p8WQAM/edit?usp=sharing)
•	Obter os jogos que têm o maior e menor desconto aplicado.
```SQL
SELECT Jogo, Desconto
FROM `teste-beanalytic.steamdb.steamdb beAnalytic`
WHERE Desconto IS NOT NULL
ORDER BY Desconto DESC
LIMIT 10;
```
![image](https://github.com/user-attachments/assets/35523690-948b-4f3f-8b8b-fbd9102a45bc)

2. [Jogos com Avaliação Baixa](https://docs.google.com/spreadsheets/d/1ADmHQiOaWIjagjdqQGj7ee9f38tZZRTfJR20urOPMQQ/edit?usp=sharing)
•	Identificar jogos com avaliações abaixo de 0.5
```SQL
SELECT Jogo, Avalia____o
FROM `teste-beanalytic.steamdb.steamdb beAnalytic`
WHERE Avalia____o < 0.5
ORDER BY Avalia____o ASC
LIMIT 10;
```
![image](https://github.com/user-attachments/assets/40451d5f-f450-47c6-a7f1-f0ad714baf15)

3. [Jogos em Promoção no Período](https://docs.google.com/spreadsheets/d/1GXKOxkxBBxAwoLoXRBOcQM4En0rpqFhh0mJ0p2iV7Ww/edit?usp=sharing)
•	Verificar os jogos com promoções (Desconto) e que têm data de término (Termina) próxima
```SQL
SELECT Jogo, Desconto, Termina
FROM `teste-beanalytic.steamdb.steamdb beAnalytic`
WHERE Desconto < 0
ORDER BY Termina ASC
LIMIT 10;
```
![image](https://github.com/user-attachments/assets/d4aba692-d205-4184-973a-ad3409936ba7)

4. [Jogos com Maior Avaliação](https://docs.google.com/spreadsheets/d/17hJXmwKMOTvfXwE78FMVnkSuY1ykcHYzkV-eJ-bvmjU/edit?usp=sharing)
•	Listar jogos com as maiores avaliações (próximas de 1).
```SQL
SELECT Jogo, Avalia____o
FROM `teste-beanalytic.steamdb.steamdb beAnalytic`
WHERE Avalia____o IS NOT NULL
ORDER BY Avalia____o DESC
LIMIT 10;
```
![image](https://github.com/user-attachments/assets/71b17b12-33bf-4675-8e7e-2647034c8de0)

5. [Análise de Jogos com Preço Mais Alto](https://docs.google.com/spreadsheets/d/1sqzqEX8ZTljntTRrIMdHKnpPn392hzGMdpuDa9SC_Jk/edit?usp=sharing)
•	Obter os jogos com os preços mais elevados.

```SQL
SELECT Jogo, Pre__o
FROM `teste-beanalytic.steamdb.steamdb beAnalytic`
WHERE Pre__o IS NOT NULL
ORDER BY CAST(REPLACE(SUBSTR(Pre__o, 3), ',', '.') AS NUMERIC) DESC
LIMIT 10;
```

![image](https://github.com/user-attachments/assets/97127d9a-e891-4c60-b747-f87bf85ef1a6)

6. [Jogos com Variação de Preço](https://docs.google.com/spreadsheets/d/168_CwSpblpGHavv_H-yKNpWBzLbAbXO4fXPAF-vEePk/edit?usp=sharing)
•	Jogos com variação de preço significativa entre as datas.
```SQL
SELECT Jogo, Pre__o, Termina, Inicio
FROM `teste-beanalytic.steamdb.steamdb beAnalytic`
WHERE Pre__o IS NOT NULL
ORDER BY Termina DESC
LIMIT 10;
```
![image](https://github.com/user-attachments/assets/5125c55c-1117-4038-8a7a-e8405fd24f4d)

7. [Jogos Liberados em um Período Específico](https://docs.google.com/spreadsheets/d/16UmNYSrerox5VhAGqEQwnmJ1IeUEaiw9P6fUq5swv4o/edit?usp=sharing)
•	Jogos com liberação marcada para um período específico.
```SQL
SELECT Jogo, Liberar
FROM `teste-beanalytic.steamdb.steamdb beAnalytic`
WHERE Liberar BETWEEN '01/11/2002' AND '01/11/2013'
ORDER BY Liberar
LIMIT 10;
```

![image](https://github.com/user-attachments/assets/f48609b6-8192-4176-8169-a842a162019b)

8. [Jogos com Promoções e Avaliações Baixas](https://docs.google.com/spreadsheets/d/1MIjXKeO3wmrwnzPKEeqIkid8b7ngT09w-U5hStwM034/edit?usp=sharing)
•	Obter jogos que estão em promoção (Desconto) e têm avaliações baixas.

```SQL
SELECT Jogo, Desconto, Avalia____o
FROM `teste-beanalytic.steamdb.steamdb beAnalytic`
WHERE Desconto < 0 AND Avalia____o < 0.5
ORDER BY Avalia____o ASC
LIMIT 10;
```

![image](https://github.com/user-attachments/assets/7d8b9c6e-3544-481d-8ddf-a1304baf7fa2)


# ![image](https://github.com/user-attachments/assets/45fa2584-dc6d-4eb2-b5fb-345e14836c44) Conclusão:
O processo de análise de dados foi concluído com sucesso após o carregamento da planilha CSV no Google Sheets e a vinculação com o Google Query para execução das consultas SQL. Durante o processo, diversas consultas foram realizadas, como a identificação de jogos com desconto, avaliação baixa, promoções e variação de preço. Além disso, foram feitos ajustes nas queries para corrigir problemas com a conversão de datas e garantir que apenas dados válidos fossem analisados. Algumas consultas não retornaram dados devido a inconsistências nos valores de data, mas as correções necessárias foram implementadas para lidar com essas situações.

Agora, a análise de jogos e promoções está pronta para ser utilizada, com as consultas otimizadas e os dados preparados para futuras investigações.

![image](https://github.com/user-attachments/assets/b2c0d2bf-3326-4f41-ac10-f863f1c34e9e)[Thiago Klebis](https://www.linkedin.com/in/thiagoklebis/)
