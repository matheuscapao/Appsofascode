
import streamlit as st
import requests
import datetime
from telegram import Bot

API_FOOTBALL_KEY = st.secrets["API_FOOTBALL_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = 2060561447

bot = Bot(token=TELEGRAM_TOKEN)

def enviar_mensagem(texto):
    bot.send_message(chat_id=CHAT_ID, text=texto)

def pegar_partidas_hoje():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    params = {"date": hoje}
    res = requests.get(url, headers=headers, params=params)
    dados = res.json()
    return dados.get("response", [])

def analisar_e_montar_mensagem(partidas):
    if not partidas:
        return "Nenhuma partida encontrada para hoje."

    mensagens = []
    for partida in partidas:
        time_casa = partida["teams"]["home"]["name"]
        time_fora = partida["teams"]["away"]["name"]
        gols_casa = partida["goals"]["home"] or 0
        gols_fora = partida["goals"]["away"] or 0
        status = partida["fixture"]["status"]["short"]

        texto = f"{time_casa} x {time_fora}\nStatus: {status}\nPlacar atual: {gols_casa} x {gols_fora}"

        # Exemplo simples: dica para over 1.5 gols se já tem 1 gol
        if gols_casa + gols_fora >= 1:
            texto += "\nDica: Apostar em OVER 1.5 gols ✅"
        else:
            texto += "\nDica: Aguarde mais gols para apostar."

        mensagens.append(texto)

    return "\n\n".join(mensagens)

st.title("Robô de Apostas - Futebol")

if st.button("Enviar mensagem teste"):
    enviar_mensagem("Olá Matheus! Seu robô de apostas está funcionando 🚀")
    st.success("Mensagem teste enviada!")

if st.button("Enviar dicas do dia"):
    partidas = pegar_partidas_hoje()
    mensagem = analisar_e_montar_mensagem(partidas)
    enviar_mensagem(mensagem)
    st.success("Dicas enviadas no Telegram!")
