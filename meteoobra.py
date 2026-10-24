
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

# Configuração do MeteoObra
FUSO = ZoneInfo("Europe/Lisbon")
LATITUDE = 38.7223
LONGITUDE = -9.1393

SAUDACOES = [
    "Boa noite! 🌙 Está na hora de preparar o dia de amanhã.",
    "Olá! 👋 Aqui está a tua atualização meteorológica.",
    "Boa noite! 🌦️ Vamos ver o tempo previsto para amanhã?",
    "Olá! É o MeteoObra. Vamos preparar o próximo dia de trabalho.",
    "Boa noite! 📋 Aqui tens a previsão para planeares melhor os trabalhos."
]

DESCRICOES_TEMPO = {
    0: "céu limpo",
    1: "maioritariamente limpo",
    2: "parcialmente nublado",
    3: "encoberto",
    45: "nevoeiro",
    48: "nevoeiro com formação de gelo",
    51: "chuvisco fraco",
    53: "chuvisco moderado",
    55: "chuvisco intenso",
    61: "chuva fraca",
    63: "chuva moderada",
    65: "chuva forte",
    71: "queda de neve fraca",
    73: "queda de neve moderada",
    75: "queda de neve forte",
    80: "aguaceiros fracos",
    81: "aguaceiros moderados",
    82: "aguaceiros fortes",
    95: "trovoada",
    96: "trovoada com granizo",
    99: "trovoada com granizo forte"
}

def obter_previsao():
    url = "https://api.open-meteo.com/v1/forecast"

    parametros = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "precipitation_sum"
        ],
        "timezone": "Europe/Lisbon",
        "forecast_days": 2
    }

    resposta = requests.get(url, params=parametros, timeout=30)
    resposta.raise_for_status()
    dados = resposta.json()

    amanha = (datetime.now(FUSO).date() + timedelta(days=1)).isoformat()
    dias = dados["daily"]
    indice = dias["time"].index(amanha)

    codigo = dias["weather_code"][indice]

    return {
        "data": amanha,
        "estado": DESCRICOES_TEMPO.get(
            codigo, "estado do tempo variável ou não especificado"
        ),
        "minima": dias["temperature_2m_min"][indice],
        "maxima": dias["temperature_2m_max"][indice],
        "prob_chuva": dias["precipitation_probability_max"][indice],
        "chuva_mm": dias["precipitation_sum"][indice]
    }

def criar_mensagem(previsao):
    saudacao = random.choice(SAUDACOES)

    return f"""{saudacao}

🌦️ MeteoObra | Previsão para Lisboa
📅 Data: {previsao['data']}
🌤️ Estado do tempo: {previsao['estado']}

🌡️ Temperatura mínima: {previsao['minima']} °C
🌡️ Temperatura máxima: {previsao['maxima']} °C
☔ Probabilidade máxima de chuva: {previsao['prob_chuva']}%
🌧️ Precipitação prevista: {previsao['chuva_mm']} mm

📋 Sugestão: confirma as condições antes de planear trabalhos no exterior.
"""

if __name__ == "__main__":
    try:
        previsao = obter_previsao()
        mensagem = criar_mensagem(previsao)
        print(mensagem)
    except (requests.RequestException, KeyError, ValueError) as erro:
        print(f"Erro ao obter a previsão meteorológica: {erro}")
        raise
