#!/usr/bin/env python3
"""
Script per estrarre input utente reali dai logs dell'app.
Serve per creare dataset di training basato su dati veri.
"""

import json
import re
from collections import Counter
from datetime import datetime
from typing import List, Dict

class UserInputExtractor:
    def __init__(self):
        self.patterns = {
            "obiettivo": [
                r"voglio\s+(?:studiare|imparare|praticare)",
                r"(?:studiare|imparare)\s+\w+\s+\d+\s+ore",
            ],
            "impegno": [
                r"(?:domani|lunedì|martedì|giovedì)\s+.+\s+\d{1,2}(?::\d{2})?",
                r"\d{1,2}:\d{2}\s+.+",
            ],
            "spesa": [
                r"speso\s+\d+(?:\.\d+)?\s+euro",
                r"\d+(?:\.\d+)?\s+euro\s+\w+",
            ],
            "diario": [
                r"oggi\s+mi\s+sento",
                r"è\s+stata\s+una\s+giornata",
            ],
        }
    
    def extract_from_db(self, db_path: str = None) -> List[Dict]:
        """
        Estrae input da database PostgreSQL/SQLite.
        
        IMPORTANTE: In produzione, aggiungi logging degli input in una tabella dedicata.
        """
        examples = []
        
        try:
            # Connetti al DB
            if db_path:
                import sqlite3
                conn = sqlite3.connect(db_path)
            else:
                # PostgreSQL (Render)
                import psycopg2
                import os
                conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            
            cursor = conn.cursor()
            
            # Query per trovare input utente (se hai una tabella chat_logs)
            # Se non hai ancora logging, salta questa parte
            try:
                cursor.execute("""
                    SELECT input_text, intent_detected, timestamp, user_ip
                    FROM chat_logs
                    WHERE timestamp > NOW() - INTERVAL '30 days'
                    ORDER BY timestamp DESC
                """)
                
                rows = cursor.fetchall()
                
                for row in rows:
                    text, intent, timestamp, user_ip = row
                    examples.append({
                        "text": text,
                        "intent": intent,
                        "source": "database",
                        "timestamp": str(timestamp),
                    })
                
                print(f"✅ Estratti {len(examples)} esempi dal database")
            
            except Exception as e:
                print(f"⚠️  Tabella chat_logs non trovata: {e}")
                print("   Suggerimento: Crea tabella per logging:")
                print("""
                CREATE TABLE chat_logs (
                    id SERIAL PRIMARY KEY,
                    user_ip VARCHAR(64),
                    input_text TEXT,
                    intent_detected VARCHAR(50),
                    confidence FLOAT,
                    timestamp TIMESTAMP DEFAULT NOW()
                );
                """)
            
            conn.close()
        
        except Exception as e:
            print(f"❌ Errore connessione DB: {e}")
        
        return examples
    
    def extract_from_logs(self, log_file: str = "logs/app.log") -> List[Dict]:
        """
        Estrae input da file log (se hai logging attivo).
        
        Cerca pattern come:
        [INFO] User input: "domani riunione 10-12"
        """
        examples = []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    # Pattern per trovare user input
                    match = re.search(r'User input:\s*"([^"]+)"', line)
                    if match:
                        text = match.group(1)
                        
                        # Classifica intent con regex semplice
                        intent = self._classify_intent(text)
                        
                        examples.append({
                            "text": text,
                            "intent": intent,
                            "source": "logs",
                        })
            
            print(f"✅ Estratti {len(examples)} esempi dai logs")
        
        except FileNotFoundError:
            print(f"⚠️  File log non trovato: {log_file}")
        
        return examples
    
    def _classify_intent(self, text: str) -> str:
        """Classifica intent con regex semplice (fallback)."""
        text_lower = text.lower()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        
        return "sconosciuto"
    
    def manual_examples(self) -> List[Dict]:
        """
        Esempi scritti manualmente (gold standard).
        Usa questi per validation set.
        """
        return [
            {"text": "domani riunione 10-12", "intent": "impegno"},
            {"text": "voglio studiare python 3 ore a settimana", "intent": "obiettivo"},
            {"text": "speso 35 euro cena", "intent": "spesa"},
            {"text": "oggi mi sento felice", "intent": "diario"},
            {"text": "cosa faccio domani?", "intent": "domanda_temporale"},
            {"text": "quanto ho speso oggi?", "intent": "domanda_budget"},
            # Aggiungi altri 50-100 esempi gold standard
        ]
    
    def combine_all(self) -> List[Dict]:
        """Combina tutte le fonti."""
        all_examples = []
        
        # 1. Database
        db_examples = self.extract_from_db()
        all_examples.extend(db_examples)
        
        # 2. Logs
        log_examples = self.extract_from_logs()
        all_examples.extend(log_examples)
        
        # 3. Manual (gold)
        manual = self.manual_examples()
        all_examples.extend(manual)
        
        # Deduplica
        seen = set()
        unique_examples = []
        for ex in all_examples:
            if ex['text'] not in seen:
                seen.add(ex['text'])
                unique_examples.append(ex)
        
        return unique_examples
    
    def save_to_file(self, examples: List[Dict], filename: str):
        """Salva in formato JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(examples, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Salvato {len(examples)} esempi in {filename}")


def main():
    """Estrai tutti gli input utente disponibili."""
    print("🔍 Extractor Input Utente Reali")
    print("=" * 50)
    
    extractor = UserInputExtractor()
    
    # Combina tutte le fonti
    examples = extractor.combine_all()
    
    if not examples:
        print("\n⚠️  Nessun esempio trovato!")
        print("\n💡 Suggerimenti:")
        print("   1. Implementa logging in app/routes/api.py:")
        print("      logger.info(f'User input: \"{text}\"')")
        print("   2. Crea tabella chat_logs nel DB")
        print("   3. Aggiungi esempi manuali in manual_examples()")
        return
    
    # Stats
    print(f"\n📊 Trovati {len(examples)} esempi:")
    intent_counts = Counter(ex['intent'] for ex in examples)
    for intent, count in intent_counts.most_common():
        print(f"   {intent}: {count}")
    
    # Salva
    output_file = "data/dataset_real_inputs.json"
    extractor.save_to_file(examples, output_file)
    
    print("\n✅ Estrazione completata!")
    print(f"\n💡 Prossimo step:")
    print(f"   1. Combina con dataset sintetico:")
    print(f"      cat data/dataset_real_inputs.json data/dataset_synthetic_800.json > data/dataset_combined.json")
    print(f"   2. Annota entities mancanti")
    print(f"   3. Split train/val/test")


if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    main()

