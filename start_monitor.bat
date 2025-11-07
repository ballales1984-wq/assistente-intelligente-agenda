@echo off
chcp 65001 >nul
echo.
echo ═══════════════════════════════════════════════
echo 🚀 AVVIO MONITORAGGIO APP
echo ═══════════════════════════════════════════════
echo.
echo ⏰ Monitorerà l'app fino alle 16:00
echo 📊 Check ogni 5 minuti
echo 📄 Log salvato in: monitor_log.txt
echo.
echo ═══════════════════════════════════════════════
echo.
echo 💡 Per interrompere: CTRL+C
echo.
echo ═══════════════════════════════════════════════
echo.

python monitor_app.py

echo.
echo ═══════════════════════════════════════════════
echo ✅ MONITORAGGIO COMPLETATO
echo ═══════════════════════════════════════════════
echo.
echo 📄 Leggi il report: monitor_log.txt
echo.
pause

