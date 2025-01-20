# SIG_FINANCE

### Lembre-se de rodar o sistema usando o comando python app.py

### Exemplos de requisições do sistema.

1. http://127.0.0.1:5001/search {
  {
    "ticker": "AAPL"
}} - Esssa requiseção pode ser feita através do sistema insominia ou postman, ou se preferir, pode rodar na pagina html aqui no repositório.

2. http://127.0.0.1:5001/history{{
    "ticker": "AAPL"
}} - essa requisição gera um documento xlsx de acordo com o ticket da empresa busacada, nesse caso da apple, usada apenas no insominia ou postman.

3. http://127.0.0.1:5001//analyze {
  {
    "criteria_matrix": [
        [1, 3, 5],
        [0.3333, 1, 2],
        [0.2, 0.5, 1]
    ],
    "alternatives": [
        {"Symbol": "AMZN", "Return": 0.15, "Risk": 0.08, "Liquidity": 0.9},
        {"Symbol": "TSLA", "Return": 0.12, "Risk": 0.05, "Liquidity": 0.85},
        {"Symbol": "META", "Return": 0.10, "Risk": 0.07, "Liquidity": 0.8}
    ]
}} - essa requisição mais robusta analisa algumas empresas de acordo com seus critérios, nela você incrementa o symbol da empresa como AMZN (amazon), o indice de retorno, risco e liquidez, pode ser usado no insominia ou postman.

4. http://127.0.0.1:5001/analyze-to-excel {
  {
    "criteria_matrix": [
        [1, 3, 5],
        [0.3333, 1, 2],
        [0.2, 0.5, 1]
    ],
    "alternatives": [
        {"Symbol": "AAPL", "Return": 0.15, "Risk": 0.08, "Liquidity": 0.9},
        {"Symbol": "MSFT", "Return": 0.12, "Risk": 0.05, "Liquidity": 0.85},
        {"Symbol": "GOOGL", "Return": 0.10, "Risk": 0.07, "Liquidity": 0.8}
    ]
}} - requisição que transforma o resultado da analise em um arquivo excel.

