"""Test Smart Links e DuckDuckGo"""

from app.integrations.web_search import WebSearchService
from app.core.smart_links import SmartLinksManager

print("\n" + "=" * 70)
print("🔗 TEST SMART LINKS & DUCKDUCKGO")
print("=" * 70)

# Test 1: WebSearchService diretto
print("\n1. Test WebSearchService diretto...")
print("-" * 70)

try:
    ws = WebSearchService()
    results = ws.search('python tutorial', max_results=3)
    print(f"✅ Risultati trovati: {len(results)}")
    
    if results:
        for i, r in enumerate(results, 1):
            print(f"\n  {i}. {r['title']}")
            print(f"     URL: {r['href']}")
            print(f"     Desc: {r['body'][:80]}...")
    else:
        print("❌ Nessun risultato!")
except Exception as e:
    print(f"❌ ERRORE: {e}")
    import traceback
    traceback.print_exc()

# Test 2: SmartLinksManager
print("\n\n2. Test SmartLinksManager...")
print("-" * 70)

try:
    slm = SmartLinksManager()
    
    test_messages = [
        "cerca machine learning",
        "trova informazioni su python",
        "google flask tutorial",
    ]
    
    for msg in test_messages:
        print(f"\nMessaggio: '{msg}'")
        result = slm.process_message(msg)
        print(f"  Has smart links: {result['has_smart_links']}")
        if result['has_smart_links']:
            print(f"  Risultati: {len(result['results'])}")
            if result['results']:
                print(f"    → {result['results'][0]['title']}")
        else:
            print("  ⚠️  Pattern non riconosciuto")
            
except Exception as e:
    print(f"❌ ERRORE: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ TEST COMPLETATI")
print("=" * 70)

