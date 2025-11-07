import requests

r = requests.post(
    'https://assistente-intelligente-agenda.onrender.com/api/chat',
    json={'messaggio': 'Domenica vado al mare dalle 16 alle 20', 'lang': 'it'},
    timeout=20
)

print(f'Status: {r.status_code}')
print(f'Content-Type: {r.headers.get("Content-Type")}')
print(f'\nRisposta:\n{r.text[:500]}')

if r.status_code == 200:
    try:
        data = r.json()
        print(f'\nJSON OK!')
        print(f'Tipo riconosciuto: {data.get("tipo_riconosciuto")}')
        if data.get('tipo_riconosciuto') == 'impegno':
            print('\n🎉 FUNZIONA! IL TUO INPUT È RICONOSCIUTO!')
        else:
            print(f'\n⚠️ Tipo: {data.get("tipo_riconosciuto")} (expected: impegno)')
    except:
        print('\n❌ JSON decode error')
else:
    print('\n❌ Status code non 200')

