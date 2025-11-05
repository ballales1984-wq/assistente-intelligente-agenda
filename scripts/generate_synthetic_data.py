#!/usr/bin/env python3
"""
Script per generare dataset sintetico di training per NLP.
Usa template e variazioni per creare esempi diversificati.
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict

class SyntheticDataGenerator:
    def __init__(self):
        # Template per ogni intent
        self.templates = {
            "obiettivo": [
                "Voglio {verb} {skill} {frequency}",
                "Vorrei imparare {skill} {frequency}",
                "{verb} {skill} {duration} a settimana",
                "Mi piacerebbe {verb} {skill}",
                "Il mio obiettivo è {verb} {skill} {frequency}",
            ],
            "impegno": [
                "{day} {event} {time}",
                "{day} devo {action} alle {time}",
                "{event} {day} dalle {time_start} alle {time_end}",
                "{time} {day} ho {event}",
                "Ricordami {event} {day} ore {time}",
            ],
            "spesa": [
                "Speso {amount} euro per {item}",
                "{amount} euro {item}",
                "Ho pagato {item} {amount}",
                "Comprato {item} {amount} euro",
                "{item} costa {amount}",
            ],
            "diario": [
                "Oggi mi sento {emotion}",
                "È stata una giornata {adjective}",
                "{reflection}",
                "Oggi ho {achievement}",
                "Mi sento {emotion} perché {reason}",
            ],
            "domanda_temporale": [
                "Cosa faccio {when}?",
                "Che impegni ho {when}?",
                "Come sarà {day}?",
                "Cosa devo fare {when}?",
            ],
            "domanda_budget": [
                "Quanto ho speso {period}?",
                "Spese {period}?",
                "Budget {period}?",
                "Quanti soldi ho speso per {category}?",
            ],
        }
        
        # Variabili per riempire template
        self.variables = {
            "verb": ["studiare", "imparare", "praticare", "allenarmi in"],
            "skill": ["Python", "Javascript", "React", "SQL", "chitarra", 
                     "inglese", "tedesco", "yoga", "corsa", "disegno"],
            "frequency": ["ogni giorno", "3 volte a settimana", "2h/settimana"],
            "duration": ["2 ore", "3 ore", "1 ora", "4 ore"],
            "day": ["domani", "lunedì", "martedì", "giovedì", "sabato", "domenica"],
            "event": ["riunione", "meeting", "palestra", "corso", "visita", "appuntamento"],
            "time": ["10:00", "14:30", "9:00", "15:00", "18:00"],
            "time_start": ["10:00", "14:00", "9:00"],
            "time_end": ["12:00", "16:00", "11:00"],
            "action": ["andare in palestra", "studiare", "lavorare"],
            "amount": ["10", "20", "35", "50", "5.50", "12.99"],
            "item": ["caffè", "pranzo", "cena", "libro", "benzina", "abbonamento"],
            "emotion": ["felice", "triste", "stanco", "energico", "ansioso", "rilassato"],
            "adjective": ["bella", "difficile", "produttiva", "stressante"],
            "reflection": [
                "Oggi ho concluso un progetto importante",
                "Ho avuto una bella conversazione con un amico",
                "Mi sono sentito un po' giù",
            ],
            "achievement": ["finito un libro", "fatto sport", "cucinato qualcosa di buono"],
            "reason": ["ho raggiunto un obiettivo", "è andata male una cosa", "sono stanco"],
            "when": ["oggi", "domani", "adesso", "stasera"],
            "period": ["oggi", "questa settimana", "questo mese", "ieri"],
            "category": ["cibo", "trasporti", "casa", "hobby"],
        }
    
    def generate(self, intent: str, count: int = 100) -> List[Dict]:
        """Genera count esempi per un intent."""
        examples = []
        
        if intent not in self.templates:
            print(f"⚠️  Intent '{intent}' non trovato")
            return []
        
        templates = self.templates[intent]
        
        for _ in range(count):
            # Scegli template random
            template = random.choice(templates)
            
            # Riempi variabili
            text = self._fill_template(template)
            
            # Estrai entities
            entities = self._extract_entities(text, intent)
            
            examples.append({
                "text": text,
                "intent": intent,
                "entities": entities,
            })
        
        return examples
    
    def _fill_template(self, template: str) -> str:
        """Riempi template con variabili random."""
        import re
        
        def replace_var(match):
            var_name = match.group(1)
            if var_name in self.variables:
                return random.choice(self.variables[var_name])
            return match.group(0)
        
        return re.sub(r'\{(\w+)\}', replace_var, template)
    
    def _extract_entities(self, text: str, intent: str) -> List[tuple]:
        """
        Pseudo-annotazione automatica (semplificata).
        In produzione, fai annotazione manuale con Label Studio.
        """
        entities = []
        
        # Pattern semplici per entity extraction
        import re
        
        # Giorni
        giorni = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica", "domani", "oggi"]
        for giorno in giorni:
            if giorno in text.lower():
                start = text.lower().find(giorno)
                entities.append((start, start + len(giorno), "GIORNO"))
        
        # Ore (formato HH:MM)
        for match in re.finditer(r'\d{1,2}:\d{2}', text):
            entities.append((match.start(), match.end(), "ORA"))
        
        # Importi (numero + euro)
        for match in re.finditer(r'\d+(?:\.\d+)?\s*euro', text):
            entities.append((match.start(), match.end() - 5, "IMPORTO"))
        
        # Skills comuni
        skills = ["python", "javascript", "react", "sql", "chitarra", "inglese", "yoga"]
        for skill in skills:
            if skill in text.lower():
                start = text.lower().find(skill)
                entities.append((start, start + len(skill), "SKILL"))
        
        return entities
    
    def generate_all(self, counts: Dict[str, int]) -> List[Dict]:
        """
        Genera dataset completo.
        
        Args:
            counts: {"obiettivo": 150, "impegno": 200, ...}
        
        Returns:
            Lista di tutti gli esempi
        """
        all_examples = []
        
        for intent, count in counts.items():
            print(f"📝 Generando {count} esempi per '{intent}'...")
            examples = self.generate(intent, count)
            all_examples.extend(examples)
            print(f"   ✅ {len(examples)} generati")
        
        # Shuffle
        random.shuffle(all_examples)
        
        return all_examples
    
    def save_to_file(self, examples: List[Dict], filename: str):
        """Salva dataset in formato JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(examples, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Salvato {len(examples)} esempi in {filename}")


def main():
    """Genera dataset completo."""
    print("🤖 Generatore Dataset Sintetico")
    print("=" * 50)
    
    generator = SyntheticDataGenerator()
    
    # Configura quanti esempi per intent
    counts = {
        "obiettivo": 150,
        "impegno": 200,
        "spesa": 150,
        "diario": 100,
        "domanda_temporale": 100,
        "domanda_budget": 100,
    }
    
    # Genera
    print(f"\n🎯 Target: {sum(counts.values())} esempi totali\n")
    examples = generator.generate_all(counts)
    
    # Salva
    output_file = "data/dataset_synthetic_800.json"
    generator.save_to_file(examples, output_file)
    
    # Stats
    print("\n📊 Statistiche:")
    from collections import Counter
    intent_counts = Counter(ex['intent'] for ex in examples)
    for intent, count in intent_counts.most_common():
        print(f"   {intent}: {count} esempi")
    
    print("\n✅ Dataset generato con successo!")
    print(f"\n💡 Prossimo step:")
    print(f"   1. Rivedi manualmente alcuni esempi")
    print(f"   2. Aggiungi esempi reali da logs")
    print(f"   3. Annota entities con Label Studio")
    print(f"   4. Run: python train_nlp_model.py --dataset {output_file}")


if __name__ == "__main__":
    # Crea directory se non esiste
    import os
    os.makedirs("data", exist_ok=True)
    
    main()

