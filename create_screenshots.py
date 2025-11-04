#!/usr/bin/env python3
"""
Script per creare screenshot automatici dell'app
Richiede: pip install playwright
Poi: playwright install chromium
"""
import asyncio
from playwright.async_api import async_playwright
import os

# URL dell'app
APP_URL = "https://assistente-intelligente-agenda.onrender.com/"

async def take_screenshots():
    """Crea screenshot automatici delle varie sezioni"""
    
    async with async_playwright() as p:
        # Lancia browser
        print("🚀 Avvio browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        
        # Crea directory per screenshot
        os.makedirs("static/screenshots/demo", exist_ok=True)
        
        print(f"📱 Carico {APP_URL}...")
        await page.goto(APP_URL, wait_until="networkidle")
        await asyncio.sleep(3)  # Attendi caricamento completo
        
        # Screenshot 1: Homepage completa
        print("📸 Screenshot 1: Homepage...")
        await page.screenshot(path="static/screenshots/demo/01-homepage.png", full_page=False)
        
        # Screenshot 2: Sezione GIF Showcase
        print("📸 Screenshot 2: GIF Showcase...")
        gif_section = page.locator(".gif-showcase").first
        if await gif_section.count() > 0:
            await gif_section.screenshot(path="static/screenshots/demo/02-gif-showcase.png")
        
        # Screenshot 3: Chat con esempio
        print("📸 Screenshot 3: Chat...")
        chat_input = page.locator("#chatInput")
        await chat_input.fill("Voglio studiare Python 3 ore a settimana")
        await asyncio.sleep(1)
        await page.screenshot(path="static/screenshots/demo/03-chat-example.png")
        
        # Invia messaggio
        print("📸 Screenshot 4: Chat dopo invio...")
        await chat_input.press("Enter")
        await asyncio.sleep(3)  # Attendi risposta
        await page.screenshot(path="static/screenshots/demo/04-chat-response.png")
        
        # Screenshot 5: Calendario
        print("📸 Screenshot 5: Calendario...")
        calendar = page.locator("#pianoSettimanale").first
        if await calendar.count() > 0:
            await calendar.screenshot(path="static/screenshots/demo/05-calendar.png")
        
        # Screenshot 6: Dashboard Analytics
        print("📸 Screenshot 6: Analytics...")
        analytics = page.locator(".dashboard-card").first
        if await analytics.count() > 0:
            await analytics.screenshot(path="static/screenshots/demo/06-analytics.png")
        
        print("\n✅ Screenshot completati!")
        print("📁 Salvati in: static/screenshots/demo/")
        
        await browser.close()

# Esegui
if __name__ == "__main__":
    print("🎬 Screenshot Automatici - Assistente Intelligente\n")
    try:
        asyncio.run(take_screenshots())
    except ImportError:
        print("\n❌ Errore: Playwright non installato!")
        print("\n📦 Installa con:")
        print("   pip install playwright")
        print("   playwright install chromium")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        print("\n💡 Assicurati che l'app sia online:")
        print("   https://assistente-intelligente-agenda.onrender.com/")

