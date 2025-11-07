import requests
import json

r = requests.post(
    'https://assistente-intelligente-agenda.onrender.com/api/chat',
    json={'messaggio': 'Domenica vado al mare dalle 16 alle 20', 'lang': 'it'},
    timeout=20
)

print(f'Status: {r.status_code}')
data = r.json()
print(json.dumps(data, indent=2, ensure_ascii=False))
print()

if r.status_code == 200 and data.get('tipo_riconosciuto') == 'impegno':
    print('🎉 FUNZIONA! IL TUO INPUT È RICONOSCIUTO!')
else:
    print('❌ Ancora errore...')

