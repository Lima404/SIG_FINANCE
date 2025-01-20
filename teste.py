from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import yfinance as yf
import pandas as pd

# Inicializar o Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

@app.route("/")
def index():
    return render_template("index.html")

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

        # Salvar os dados históricos em uma planilha Excel
        file_name = f"{ticker_symbol}_history.xlsx"
        history.reset_index(inplace=True)  # Converter o índice para uma coluna
        history.to_excel(file_name, index=False)

        # Retornar o arquivo Excel como resposta
        return send_file(file_name, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Could not fetch historical data: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
