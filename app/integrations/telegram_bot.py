"""
Telegram Bot Integration
Integrazione completa con Telegram usando webhook
"""

import os
import logging
from datetime import datetime, timedelta, date
from typing import Dict, Any, Optional
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

# Import dei manager esistenti
from app.core.input_manager import InputManager
from app.managers import PassatoManager, PresenteManager, FuturoManager, SpeseManager
from app.models import UserProfile, Obiettivo, Impegno, Spesa, DiarioGiornaliero
from app import db

logger = logging.getLogger(__name__)


class TelegramBotService:
    """Gestisce l'integrazione con Telegram Bot"""
    
    def __init__(self, token: str = None):
        """
        Inizializza il bot Telegram
        
        Args:
            token: Token del bot Telegram (se None, legge da ENV)
        """
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.bot = None
        self.application = None
        
        if self.token:
            try:
                self.bot = Bot(token=self.token)
                self.application = Application.builder().token(self.token).build()
                logger.info("✅ Telegram Bot inizializzato con successo!")
            except Exception as e:
                logger.error(f"❌ Errore inizializzazione Telegram Bot: {e}")
                self.bot = None
                self.application = None
        else:
            logger.warning("⚠️ TELEGRAM_BOT_TOKEN non configurato")
    
    def is_available(self) -> bool:
        """Verifica se il bot è disponibile"""
        return self.bot is not None
    
    async def process_webhook(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa webhook ricevuto da Telegram
        
        Args:
            update_data: Dati del webhook da Telegram
            
        Returns:
            Dizionario con esito e messaggio
        """
        try:
            update = Update.de_json(update_data, self.bot)
            
            if not update.message or not update.message.text:
                return {"success": False, "error": "No message text"}
            
            # Estrai dati messaggio
            telegram_user_id = update.message.from_user.id
            telegram_username = update.message.from_user.username or "Unknown"
            telegram_first_name = update.message.from_user.first_name or ""
            message_text = update.message.text.strip()
            chat_id = update.message.chat_id
            
            logger.info(f"📱 Telegram message from @{telegram_username} ({telegram_user_id}): '{message_text[:50]}...'")
            
            # Gestisci comandi
            if message_text.startswith('/'):
                response = await self._handle_command(message_text, telegram_user_id, telegram_username)
            else:
                # Gestisci messaggio normale (NLP)
                response = await self._handle_message(message_text, telegram_user_id, telegram_username, telegram_first_name)
            
            # Invia risposta
            await self.bot.send_message(chat_id=chat_id, text=response, parse_mode='Markdown')
            
            return {"success": True, "response": response}
            
        except Exception as e:
            logger.error(f"❌ Errore processing webhook: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_command(self, command: str, telegram_user_id: int, telegram_username: str) -> str:
        """Gestisce comandi bot (/start, /help, etc.)"""
        
        command_lower = command.lower()
        
        if command_lower.startswith('/start'):
            return (
                f"👋 *Benvenuto in Wallmind Agenda!*\n\n"
                f"Sono il tuo assistente personale per organizzare vita e obiettivi.\n\n"
                f"✨ *Cosa posso fare:*\n"
                f"• 📚 Creare obiettivi: _\"Voglio studiare Python 3 ore a settimana\"_\n"
                f"• 📅 Gestire impegni: _\"Domani riunione ore 15\"_\n"
                f"• 💰 Tracciare spese: _\"Speso 25€ pranzo\"_\n"
                f"• 📖 Salvare riflessioni: _\"Oggi ho capito che...\"_\n"
                f"• ❓ Rispondere domande: _\"Cosa devo fare oggi?\"_\n\n"
                f"Scrivi liberamente, capisco italiano, inglese, spagnolo, cinese, russo e arabo!\n\n"
                f"Usa /help per vedere tutti i comandi."
            )
        
        elif command_lower.startswith('/help'):
            return (
                f"🤖 *Comandi Disponibili:*\n\n"
                f"/start - Messaggio di benvenuto\n"
                f"/help - Mostra questo aiuto\n"
                f"/oggi - Mostra agenda di oggi\n"
                f"/domani - Mostra agenda di domani\n"
                f"/obiettivi - Mostra i tuoi obiettivi\n"
                f"/spese - Sommario spese recenti\n"
                f"/stats - Statistiche personali\n\n"
                f"💡 *Esempi di cosa scrivere:*\n"
                f"• \"Voglio studiare Python 3 ore a settimana\"\n"
                f"• \"Domani palestra ore 18\"\n"
                f"• \"Speso 15€ caffè\"\n"
                f"• \"Cosa devo fare oggi?\"\n"
                f"• \"Oggi mi sento motivato, ho fatto progressi!\""
            )
        
        elif command_lower.startswith('/oggi'):
            return await self._get_agenda_oggi(telegram_user_id)
        
        elif command_lower.startswith('/domani'):
            return await self._get_agenda_domani(telegram_user_id)
        
        elif command_lower.startswith('/obiettivi'):
            return await self._get_obiettivi(telegram_user_id)
        
        elif command_lower.startswith('/spese'):
            return await self._get_spese(telegram_user_id)
        
        elif command_lower.startswith('/stats'):
            return await self._get_stats(telegram_user_id)
        
        else:
            return f"❓ Comando sconosciuto. Usa /help per vedere i comandi disponibili."
    
    async def _handle_message(self, message_text: str, telegram_user_id: int, telegram_username: str, telegram_first_name: str) -> str:
        """
        Gestisce messaggio normale usando NLP
        
        Args:
            message_text: Testo del messaggio
            telegram_user_id: ID utente Telegram
            telegram_username: Username Telegram
            telegram_first_name: Nome utente
            
        Returns:
            Risposta testuale
        """
        try:
            # Trova o crea utente
            user = self._get_or_create_user(telegram_user_id, telegram_username, telegram_first_name)
            
            # Analizza input con NLP (supporta 6 lingue!)
            risultato = InputManager.analizza_input(message_text)
            
            tipo = risultato.get("tipo")
            dati = risultato.get("dati", {})
            
            # Gestisci in base al tipo riconosciuto
            if tipo == "obiettivo":
                return self._crea_obiettivo(user, dati)
            
            elif tipo == "impegno" or tipo == "impegno_ricorrente":
                return self._crea_impegno(user, dati, tipo)
            
            elif tipo == "spesa":
                return self._crea_spesa(user, dati)
            
            elif tipo == "diario":
                return self._crea_diario(user, dati)
            
            elif tipo == "domanda":
                return self._rispondi_domanda(user, dati)
            
            elif tipo == "completamento":
                return dati.get("messaggio", "✅ Ottimo lavoro!")
            
            elif tipo == "stato":
                return f"📝 Ho annotato: {dati.get('stato', 'stato')}.\n💡 {dati.get('suggerimento', 'Continua così!')}"
            
            elif tipo == "aiuto":
                suggerimenti = dati.get("suggerimenti", [])
                return "💡 *Ecco cosa puoi fare:*\n\n" + "\n".join(f"• {s}" for s in suggerimenti)
            
            elif tipo == "sconosciuto":
                suggerimenti = dati.get("suggerimenti", [])
                return (
                    f"🤔 Non ho capito bene questo formato.\n\n"
                    f"💡 *Prova così:*\n" + "\n".join(f"• {s}" for s in suggerimenti[:3])
                )
            
            else:
                return "✅ Messaggio ricevuto! Usa /help per vedere cosa posso fare."
        
        except Exception as e:
            logger.error(f"❌ Errore gestione messaggio: {e}")
            return f"⚠️ Errore temporaneo. Riprova tra poco! 🔄"
    
    def _get_or_create_user(self, telegram_user_id: int, telegram_username: str, telegram_first_name: str) -> UserProfile:
        """Trova o crea utente in base a Telegram ID"""
        
        # Cerca utente esistente (usa telegram_user_id come identifier unico)
        user = UserProfile.query.filter_by(telegram_id=str(telegram_user_id)).first()
        
        if not user:
            # Crea nuovo utente
            user = UserProfile(
                nome=telegram_first_name or telegram_username or f"User{telegram_user_id}",
                telegram_id=str(telegram_user_id),
                telegram_username=telegram_username,
                livello_energia=80,
                livello_stress=30
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"✅ Nuovo utente Telegram creato: @{telegram_username} ({telegram_user_id})")
        
        return user
    
    def _crea_obiettivo(self, user: UserProfile, dati: Dict[str, Any]) -> str:
        """Crea obiettivo da dati NLP"""
        try:
            obiettivo = Obiettivo(
                user_id=user.id,
                nome=dati.get("nome", "Nuovo Obiettivo"),
                tipo=dati.get("tipo", "personale"),
                durata_settimanale=dati.get("durata_settimanale", 0),
                data_inizio=date.today(),
                data_fine=date.today() + timedelta(weeks=12),  # Default 3 mesi
                completato=False
            )
            db.session.add(obiettivo)
            db.session.commit()
            
            return (
                f"✅ *Obiettivo creato con successo!*\n\n"
                f"📚 *{obiettivo.nome}*\n"
                f"⏱ {obiettivo.durata_settimanale}h a settimana\n"
                f"📅 Fino al {obiettivo.data_fine.strftime('%d/%m/%Y')}\n\n"
                f"Continua così! 🚀"
            )
        except Exception as e:
            logger.error(f"❌ Errore creazione obiettivo: {e}")
            return "⚠️ Errore durante creazione obiettivo. Riprova!"
    
    def _crea_impegno(self, user: UserProfile, dati: Dict[str, Any], tipo: str) -> str:
        """Crea impegno da dati NLP"""
        try:
            # Calcola data impegno
            giorno = dati.get("giorno", "oggi")
            if giorno == "domani":
                data_impegno = date.today() + timedelta(days=1)
            elif giorno == "oggi":
                data_impegno = date.today()
            else:
                # Gestisci giorni della settimana o date specifiche
                data_impegno = dati.get("data_specifica") or date.today()
                if isinstance(data_impegno, str):
                    data_impegno = datetime.strptime(data_impegno, "%Y-%m-%d").date()
            
            impegno = Impegno(
                user_id=user.id,
                nome=dati.get("nome", "Nuovo Impegno"),
                data=data_impegno,
                ora_inizio=dati.get("ora_inizio", "09:00"),
                ora_fine=dati.get("ora_fine", "10:00"),
                completato=False,
                ricorrente=(tipo == "impegno_ricorrente")
            )
            db.session.add(impegno)
            db.session.commit()
            
            return (
                f"✅ *Impegno aggiunto!*\n\n"
                f"📅 {impegno.nome}\n"
                f"📆 {data_impegno.strftime('%d/%m/%Y')}\n"
                f"⏰ {impegno.ora_inizio} - {impegno.ora_fine}\n\n"
                f"Ti ricorderò! 🔔"
            )
        except Exception as e:
            logger.error(f"❌ Errore creazione impegno: {e}")
            return "⚠️ Errore durante creazione impegno. Riprova!"
    
    def _crea_spesa(self, user: UserProfile, dati: Dict[str, Any]) -> str:
        """Crea spesa da dati NLP"""
        try:
            spesa = Spesa(
                user_id=user.id,
                importo=dati.get("importo", 0.0),
                categoria=dati.get("categoria", "Altro"),
                descrizione=dati.get("descrizione", "Spesa"),
                data=dati.get("data", date.today())
            )
            db.session.add(spesa)
            db.session.commit()
            
            return (
                f"✅ *Spesa registrata!*\n\n"
                f"💰 {spesa.importo}€\n"
                f"📁 Categoria: {spesa.categoria}\n"
                f"📝 {spesa.descrizione}\n"
                f"📅 {spesa.data.strftime('%d/%m/%Y')}\n\n"
                f"Budget sotto controllo! 📊"
            )
        except Exception as e:
            logger.error(f"❌ Errore creazione spesa: {e}")
            return "⚠️ Errore durante registrazione spesa. Riprova!"
    
    def _crea_diario(self, user: UserProfile, dati: Dict[str, Any]) -> str:
        """Crea voce diario da dati NLP"""
        try:
            diario = DiarioGiornaliero(
                user_id=user.id,
                data=dati.get("data", date.today()),
                testo=dati.get("testo", ""),
                parole_chiave=",".join(dati.get("parole_chiave", [])),
                sentiment=dati.get("sentiment", {}).get("compound", 0.0)
            )
            db.session.add(diario)
            db.session.commit()
            
            sentiment = dati.get("sentiment", {})
            emoji = "😊" if sentiment.get("compound", 0) > 0.3 else "😐" if sentiment.get("compound", 0) > -0.3 else "😔"
            
            return (
                f"✅ *Salvato nel diario!* {emoji}\n\n"
                f"📖 Riflessione aggiunta al {diario.data.strftime('%d/%m/%Y')}\n"
                f"🏷 Tag: {', '.join(dati.get('parole_chiave', [])[:3])}\n\n"
                f"Continua a scrivere quando vuoi! ✍️"
            )
        except Exception as e:
            logger.error(f"❌ Errore creazione diario: {e}")
            return "⚠️ Errore durante salvataggio diario. Riprova!"
    
    def _rispondi_domanda(self, user: UserProfile, dati: Dict[str, Any]) -> str:
        """Risponde a domande utente"""
        tipo_domanda = dati.get("tipo_domanda")
        
        if tipo_domanda == "domanda_oggi":
            return self._get_agenda_oggi_sync(user.id)
        
        elif tipo_domanda == "domanda_spese":
            return self._get_spese_sync(user.id)
        
        elif tipo_domanda == "domanda_obiettivi":
            return self._get_obiettivi_sync(user.id)
        
        else:
            return "🤔 Domanda interessante! Usa /help per vedere cosa posso fare."
    
    async def _get_agenda_oggi(self, telegram_user_id: int) -> str:
        """Ritorna agenda di oggi"""
        return self._get_agenda_oggi_sync(telegram_user_id)
    
    def _get_agenda_oggi_sync(self, telegram_user_id: int) -> str:
        """Versione sincrona agenda oggi"""
        try:
            user = UserProfile.query.filter_by(telegram_id=str(telegram_user_id)).first()
            if not user:
                return "❌ Utente non trovato. Usa /start per iniziare!"
            
            oggi = date.today()
            impegni = Impegno.query.filter_by(user_id=user.id, data=oggi).order_by(Impegno.ora_inizio).all()
            
            if not impegni:
                return f"📅 *Agenda di Oggi* ({oggi.strftime('%d/%m/%Y')})\n\nNessun impegno! Giornata libera! 🎉"
            
            response = f"📅 *Agenda di Oggi* ({oggi.strftime('%d/%m/%Y')})\n\n"
            for imp in impegni:
                status = "✅" if imp.completato else "⏰"
                response += f"{status} {imp.ora_inizio} - {imp.ora_fine}: *{imp.nome}*\n"
            
            return response
        except Exception as e:
            logger.error(f"❌ Errore agenda oggi: {e}")
            return "⚠️ Errore recupero agenda."
    
    async def _get_agenda_domani(self, telegram_user_id: int) -> str:
        """Ritorna agenda di domani"""
        try:
            user = UserProfile.query.filter_by(telegram_id=str(telegram_user_id)).first()
            if not user:
                return "❌ Utente non trovato. Usa /start per iniziare!"
            
            domani = date.today() + timedelta(days=1)
            impegni = Impegno.query.filter_by(user_id=user.id, data=domani).order_by(Impegno.ora_inizio).all()
            
            if not impegni:
                return f"📅 *Agenda di Domani* ({domani.strftime('%d/%m/%Y')})\n\nNessun impegno! 🎉"
            
            response = f"📅 *Agenda di Domani* ({domani.strftime('%d/%m/%Y')})\n\n"
            for imp in impegni:
                response += f"⏰ {imp.ora_inizio} - {imp.ora_fine}: *{imp.nome}*\n"
            
            return response
        except Exception as e:
            logger.error(f"❌ Errore agenda domani: {e}")
            return "⚠️ Errore recupero agenda."
    
    async def _get_obiettivi(self, telegram_user_id: int) -> str:
        """Ritorna lista obiettivi"""
        return self._get_obiettivi_sync(telegram_user_id)
    
    def _get_obiettivi_sync(self, telegram_user_id: int) -> str:
        """Versione sincrona obiettivi"""
        try:
            user = UserProfile.query.filter_by(telegram_id=str(telegram_user_id)).first()
            if not user:
                return "❌ Utente non trovato. Usa /start per iniziare!"
            
            obiettivi = Obiettivo.query.filter_by(user_id=user.id, completato=False).all()
            
            if not obiettivi:
                return "📚 *I Tuoi Obiettivi*\n\nNessun obiettivo attivo. Creane uno!"
            
            response = "📚 *I Tuoi Obiettivi*\n\n"
            for obj in obiettivi:
                response += f"🎯 *{obj.nome}*\n"
                response += f"   ⏱ {obj.durata_settimanale}h/settimana\n"
                response += f"   📅 Fino al {obj.data_fine.strftime('%d/%m/%Y')}\n\n"
            
            return response
        except Exception as e:
            logger.error(f"❌ Errore obiettivi: {e}")
            return "⚠️ Errore recupero obiettivi."
    
    async def _get_spese(self, telegram_user_id: int) -> str:
        """Ritorna sommario spese"""
        return self._get_spese_sync(telegram_user_id)
    
    def _get_spese_sync(self, telegram_user_id: int) -> str:
        """Versione sincrona spese"""
        try:
            user = UserProfile.query.filter_by(telegram_id=str(telegram_user_id)).first()
            if not user:
                return "❌ Utente non trovato. Usa /start per iniziare!"
            
            # Spese ultimi 7 giorni
            data_limite = date.today() - timedelta(days=7)
            spese = Spesa.query.filter(
                Spesa.user_id == user.id,
                Spesa.data >= data_limite
            ).order_by(Spesa.data.desc()).all()
            
            if not spese:
                return "💰 *Spese Recenti* (7 giorni)\n\nNessuna spesa registrata!"
            
            totale = sum(s.importo for s in spese)
            
            response = f"💰 *Spese Recenti* (7 giorni)\n\n"
            response += f"💵 *Totale: {totale:.2f}€*\n\n"
            
            for spesa in spese[:10]:  # Max 10 spese
                response += f"📅 {spesa.data.strftime('%d/%m')}: {spesa.importo:.2f}€ - {spesa.descrizione}\n"
            
            return response
        except Exception as e:
            logger.error(f"❌ Errore spese: {e}")
            return "⚠️ Errore recupero spese."
    
    async def _get_stats(self, telegram_user_id: int) -> str:
        """Ritorna statistiche personali"""
        try:
            user = UserProfile.query.filter_by(telegram_id=str(telegram_user_id)).first()
            if not user:
                return "❌ Utente non trovato. Usa /start per iniziare!"
            
            # Conta elementi
            obiettivi_count = Obiettivo.query.filter_by(user_id=user.id, completato=False).count()
            impegni_oggi = Impegno.query.filter_by(user_id=user.id, data=date.today()).count()
            
            # Spese mese corrente
            primo_mese = date.today().replace(day=1)
            spese_mese = db.session.query(db.func.sum(Spesa.importo)).filter(
                Spesa.user_id == user.id,
                Spesa.data >= primo_mese
            ).scalar() or 0.0
            
            response = (
                f"📊 *Le Tue Statistiche*\n\n"
                f"👤 {user.nome}\n"
                f"🎯 {obiettivi_count} obiettivi attivi\n"
                f"📅 {impegni_oggi} impegni oggi\n"
                f"💰 {spese_mese:.2f}€ spesi questo mese\n"
                f"⚡ Energia: {user.livello_energia}%\n"
                f"😌 Stress: {user.livello_stress}%\n\n"
                f"Continua così! 🚀"
            )
            
            return response
        except Exception as e:
            logger.error(f"❌ Errore stats: {e}")
            return "⚠️ Errore recupero statistiche."


# Singleton instance
_telegram_bot_service = None


def get_telegram_bot() -> TelegramBotService:
    """Ritorna istanza singleton del Telegram Bot"""
    global _telegram_bot_service
    if _telegram_bot_service is None:
        _telegram_bot_service = TelegramBotService()
    return _telegram_bot_service

