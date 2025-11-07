#!/usr/bin/env python
"""
Script di monitoraggio continuo dell'app
Controlla ogni 5 minuti e registra tutto in un log
Esegue test automatici e segnala problemi
"""

import requests
import time
from datetime import datetime, timedelta
import sys
import os

BASE_URL = "https://assistente-intelligente-agenda.onrender.com"
LOG_FILE = "monitor_log.txt"
CHECK_INTERVAL = 300  # 5 minuti
END_TIME = datetime.now().replace(hour=16, minute=0, second=0)

def log(message):
    """Scrivi nel log e stampa"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def test_homepage():
    """Test homepage"""
    try:
        r = requests.get(f"{BASE_URL}/", timeout=15)
        return r.status_code == 200
    except:
        return False

def test_chat():
    """Test chat NLP"""
    try:
        payload = {"messaggio": "Voglio studiare Python 3 ore", "lang": "it"}
        r = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=15)
        if r.status_code != 200:
            return False
        data = r.json()
        return data.get('tipo_riconosciuto') == 'obiettivo'
    except Exception as e:
        log(f"   ⚠️ Errore chat: {e}")
        return False

def test_profilo():
    """Test profilo"""
    try:
        r = requests.get(f"{BASE_URL}/api/profilo", timeout=15)
        return r.status_code == 200
    except:
        return False

def check_render_status():
    """Controlla se app è live"""
    try:
        r = requests.get(BASE_URL, timeout=15)
        return True, r.status_code
    except requests.exceptions.Timeout:
        return False, "TIMEOUT"
    except requests.exceptions.ConnectionError:
        return False, "DOWN"
    except Exception as e:
        return False, str(e)

def full_check():
    """Esegui check completo"""
    log("=" * 60)
    log("🔍 CONTROLLO APP")
    
    # 1. Controlla se app è raggiungibile
    is_live, status = check_render_status()
    
    if not is_live:
        log(f"❌ APP NON RAGGIUNGIBILE: {status}")
        log("   Possibili cause:")
        log("   - Deploy in corso")
        log("   - App sospesa (free tier)")
        log("   - Errore critico")
        return False
    
    log(f"✅ App raggiungibile (HTTP {status})")
    
    # 2. Test homepage
    if test_homepage():
        log("✅ Homepage funziona")
    else:
        log("❌ Homepage non risponde")
        return False
    
    # 3. Test profilo
    if test_profilo():
        log("✅ API Profilo funziona")
    else:
        log("❌ API Profilo fallita")
        return False
    
    # 4. Test chat (il più importante!)
    log("🧪 Test chat NLP...")
    if test_chat():
        log("✅ CHAT FUNZIONA! NLP riconosce obiettivi!")
        log("🎉 APP COMPLETAMENTE FUNZIONANTE!")
        return True
    else:
        log("❌ Chat non funziona correttamente")
        return False

def main():
    """Loop di monitoraggio"""
    log("\n" + "=" * 60)
    log("🚀 AVVIO MONITORAGGIO APP")
    log(f"🌐 Target: {BASE_URL}")
    log(f"⏰ Inizio: {datetime.now().strftime('%H:%M:%S')}")
    log(f"🛑 Fine prevista: 16:00")
    log(f"📊 Check ogni: {CHECK_INTERVAL // 60} minuti")
    log("=" * 60)
    
    check_count = 0
    success_count = 0
    first_success = None
    
    try:
        while datetime.now() < END_TIME:
            check_count += 1
            
            # Esegui check completo
            success = full_check()
            
            if success:
                success_count += 1
                if first_success is None:
                    first_success = datetime.now()
                    log(f"🎉 PRIMA VOLTA FUNZIONANTE: {first_success.strftime('%H:%M:%S')}")
            
            # Statistiche
            success_rate = (success_count / check_count) * 100
            log(f"📊 Check #{check_count} - Success rate: {success_rate:.1f}%")
            
            # Attendi prossimo check
            next_check = datetime.now() + timedelta(seconds=CHECK_INTERVAL)
            if next_check < END_TIME:
                log(f"⏰ Prossimo check: {next_check.strftime('%H:%M:%S')}")
                log("💤 Sleeping...\n")
                time.sleep(CHECK_INTERVAL)
            else:
                break
        
        # Report finale
        log("\n" + "=" * 60)
        log("📊 REPORT FINALE")
        log("=" * 60)
        log(f"✅ Check completati: {check_count}")
        log(f"✅ Check riusciti: {success_count}")
        log(f"📈 Success rate: {(success_count / check_count * 100):.1f}%")
        if first_success:
            log(f"🎉 Prima volta funzionante: {first_success.strftime('%H:%M:%S')}")
            deploy_time = (first_success - datetime.now().replace(hour=5, minute=30, second=0)).total_seconds() / 60
            if deploy_time > 0:
                log(f"⏱️ Tempo deploy: ~{deploy_time:.0f} minuti")
        log("=" * 60)
        
        if success_count == check_count:
            log("🎉 APP SEMPRE FUNZIONANTE! TUTTO OK! ✅")
        elif success_count > 0:
            log(f"⚠️ App funzionante ma con {check_count - success_count} fallimenti")
        else:
            log("❌ APP MAI FUNZIONANTE - PROBLEMA CRITICO!")
        
    except KeyboardInterrupt:
        log("\n⚠️ Monitoraggio interrotto dall'utente")
    except Exception as e:
        log(f"\n❌ ERRORE CRITICO: {e}")

if __name__ == "__main__":
    # Crea/pulisci log file
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")
    
    main()
    
    log("\n💤 MONITORAGGIO TERMINATO")
    log("📄 Leggi monitor_log.txt per il report completo")

