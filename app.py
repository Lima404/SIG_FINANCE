from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np

# Inicializar o Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

# Função para calcular pesos dos critérios usando AHP
def calculate_weights(criteria_matrix):
    criteria_normalized = criteria_matrix / criteria_matrix.sum(axis=0)
    criteria_weights = criteria_normalized.mean(axis=1)
    return criteria_weights

# Função para normalizar alternativas
def normalize_alternatives(alternatives, weights):
    normalized_df = alternatives.copy()
    for column in alternatives.columns[1:]:  # Ignorar a primeira coluna (nomes das ações)
        if column.lower() == "risk":  # Critérios onde menor é melhor
            normalized_df[column] = 1 - (alternatives[column] / alternatives[column].max())
        else:
            normalized_df[column] = alternatives[column] / alternatives[column].max()

    # Calcular pontuações
    normalized_df["Score"] = np.dot(normalized_df.iloc[:, 1:], weights)
    return normalized_df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Receber dados do usuário
        data = request.json
        if not data or "criteria_matrix" not in data or "alternatives" not in data:
            return jsonify({"error": "Invalid input. 'criteria_matrix' and 'alternatives' are required."}), 400

        # Matriz de comparação dos critérios
        criteria_matrix = np.array(data["criteria_matrix"])

        # Alternativas enviadas pelo usuário
        alternatives_data = data["alternatives"]
        alternatives = pd.DataFrame(alternatives_data)

        # Calcular os pesos dos critérios
        weights = calculate_weights(criteria_matrix)

        # Normalizar e calcular pontuações
        result_df = normalize_alternatives(alternatives, weights)

        # Ordenar as alternativas
        result = result_df.sort_values(by="Score", ascending=False).to_dict(orient="records")
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/analyze-to-excel", methods=["POST"])
def analyze_to_excel():
  try:
      # Receber dados do usuário
      data = request.json
      if not data or "criteria_matrix" not in data or "alternatives" not in data:
          return jsonify({"error": "Invalid input. 'criteria_matrix' and 'alternatives' are required."}), 400

      # Matriz de comparação dos critérios
      criteria_matrix = np.array(data["criteria_matrix"])

      # Alternativas enviadas pelo usuário
      alternatives_data = data["alternatives"]
      alternatives = pd.DataFrame(alternatives_data)

      # Calcular os pesos dos critérios
      weights = calculate_weights(criteria_matrix)

      # Normalizar e calcular pontuações
      result_df = normalize_alternatives(alternatives, weights)

      # Ordenar as alternativas
      result_df = result_df.sort_values(by="Score", ascending=False)

      # Salvar os resultados em um arquivo Excel
      file_name = "analysis_results.xlsx"
      result_df.to_excel(file_name, index=False)

      # Retornar o arquivo Excel como resposta
      return send_file(file_name, as_attachment=True)

  except Exception as e:
      return jsonify({"error": str(e)}), 500

@app.route("/search", methods=["POST"])
def search():
    try:
        data = request.json
        ticker_symbol = data.get("ticker")

        if not ticker_symbol:
            return jsonify({"error": "Ticker symbol is required"}), 400

        ticker = yf.Ticker(ticker_symbol)
        stock_info = ticker.info

        return jsonify({
            "symbol": stock_info.get("symbol"),
            "regularMarketPrice": stock_info.get("regularMarketPrice"),
            "bid": stock_info.get("bid"),
            "ask": stock_info.get("ask"),
            "previousClose": stock_info.get("previousClose"),
            "open": stock_info.get("open"),
            "dayLow": stock_info.get("dayLow"),
            "dayHigh": stock_info.get("dayHigh"),
            "volume": stock_info.get("volume"),
            "marketCap": stock_info.get("marketCap"),
            "forwardPE": stock_info.get("forwardPE"),
            "trailingPE": stock_info.get("trailingPE"),
            "dividendRate": stock_info.get("dividendRate"),
            "dividendYield": stock_info.get("dividendYield"),
            "sector": stock_info.get("sector"),
            "currency": stock_info.get("currency")
        })
    except Exception as e:
        return jsonify({"error": f"Could not fetch data: {str(e)}"}), 500

@app.route("/history", methods=["POST"])
def history():
    try:
        data = request.json
        ticker_symbol = data.get("ticker")

        if not ticker_symbol:
            return jsonify({"error": "Ticker symbol is required"}), 400

        # Buscar dados históricos
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period="6mo")

        if history.empty:
            return jsonify({"error": "No historical data available for this ticker"}), 404

        # Remover informações de fuso horário
        history.reset_index(inplace=True)
        history['Date'] = history['Date'].dt.tz_localize(None)

        # Salvar os dados históricos em uma planilha Excel
        file_name = f"{ticker_symbol}_history.xlsx"
        history.to_excel(file_name, index=False)

        # Retornar o arquivo Excel como resposta
        return send_file(file_name, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Could not fetch historical data: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
