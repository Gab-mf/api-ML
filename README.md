# 📊 API de Vitivinicultura - Embrapa
## ✅ Visão Geral
Este projeto implementa uma API REST que realiza a coleta de dados públicos de vitivinicultura diretamente do site da Embrapa. A API organiza os dados e os disponibiliza para possíveis aplicações analíticas e de machine learning (ML).

## 🛠️ Como funciona cada parte do sistema
1. Coleta de Dados (Ingestão)
Foi utilizado Selenium e BeautifulSoup para automatizar a navegação nas páginas da Embrapa e identificar os links de download das planilhas oficiais.

O arquivo é baixado automaticamente e lido com pandas, tratando adequadamente arquivos .csv.

A coleta é feita sob demanda, quando o usuário acessa a API.

2. API REST
Desenvolvida com Flask, expõe os seguintes endpoints:

/api/producao

/api/processamento

/api/comercializacao

/api/importacao

/api/exportacao

Cada rota corresponde a uma aba dos dados da Embrapa e realiza a extração e retorno dos dados em formato JSON.

A API é protegida com JWT (JSON Web Tokens) para garantir segurança e controle de acesso.

A documentação está disponível via Swagger, permitindo fácil exploração e testes dos endpoints.

3. Armazenamento dos Dados
Atualmente, a API realiza o processamento em memória e entrega os dados diretamente ao usuário.

Para evolução do projeto, o armazenamento pode ser feito em:

Banco de dados relacional (PostgreSQL)

Data Lake (Amazon S3)

Arquivos locais versionados por data e aba.

4. Uso Futuro em Machine Learning
O projeto está preparado para alimentar modelos de machine learning com os dados coletados.

Exemplo de pipeline:

Coleta: extração via API.

Processamento: limpeza e transformação dos dados.

Armazenamento: persistência em base estruturada.

Modelagem: treinamento de modelos preditivos.

## 🤖 Cenário escolhido para aplicação de Machine Learning
🎯 Previsão da Produção de Vinho ao Longo dos Anos
Variável target: quantidade produzida (em litros ou toneladas) de cada tipo de vinho.

Objetivo: prever a produção futura com base nos dados históricos.

Benefícios:

Auxilia produtores na tomada de decisão sobre plantio, colheita e vendas.

Apoia políticas públicas para o setor de vitivinicultura.

Facilita planejamento logístico e financeiro das vinícolas.

🛠️ Modelo de Machine Learning sugerido:
Tipo: Série temporal

Exemplo: ARIMA, Prophet ou LSTM

Entradas: ano, tipo de vinho, região (se disponível)

Saída: previsão de produção para anos futuros.

## 📄 Tecnologias usadas
Python

Flask

Flask-JWT-Extended

Flasgger (Swagger UI)

Selenium

BeautifulSoup

Pandas

