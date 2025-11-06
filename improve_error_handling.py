"""Script per migliorare error handling nell'app"""

import os
import re
from pathlib import Path

print("=" * 70)
print("🛡️ ANALISI ERROR HANDLING")
print("=" * 70)

# Trova tutti i file Python
app_dir = Path("app")
python_files = list(app_dir.rglob("*.py"))

print(f"\n📊 File Python trovati: {len(python_files)}")

# Pattern da cercare
patterns = {
    "bare_except": r"except:\s*\n",  # except: senza Exception
    "pass_silent": r"except.*:\s*pass",  # except che fa pass senza log
    "generic_except": r"except Exception:\s*\n",  # Exception generico
}

findings = {k: [] for k in patterns}

for py_file in python_files:
    try:
        content = py_file.read_text(encoding='utf-8')
        
        for name, pattern in patterns.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                # Trova numero linea
                line_num = content[:match.start()].count('\n') + 1
                findings[name].append({
                    'file': str(py_file),
                    'line': line_num,
                    'match': match.group(0)
                })
    except:
        pass

# Report
print("\n" + "=" * 70)
print("📊 RISULTATI ANALISI")
print("=" * 70)

total = 0
for name, items in findings.items():
    if items:
        print(f"\n⚠️  {name}: {len(items)} occorrenze")
        total += len(items)
        for item in items[:5]:  # Mostra primi 5
            print(f"   - {item['file']}:{item['line']}")

print(f"\n🎯 TOTALE PROBLEMI: {total}")

if total == 0:
    print("\n✅ ERROR HANDLING OTTIMO!")
else:
    print(f"\n⚠️  {total} punti da migliorare")
    print("\n💡 RACCOMANDAZIONE:")
    print("   Sostituire 'except: pass' con logging appropriato")
    print("   Esempio: except Exception as e:")
    print("            logger.error(f'Errore: {e}', exc_info=True)")

print("\n" + "=" * 70)

