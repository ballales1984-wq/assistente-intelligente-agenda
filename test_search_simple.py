# -*- coding: utf-8 -*-
"""Test semplice Smart Links senza emoji"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.smart_links import SmartLinksManager

print("="*50)
print("TEST SMART LINKS SEMPLICE")
print("="*50)

slm = SmartLinksManager()

# Test 1
msg = "cerca python tutorial"
print(f"\n1. Test: '{msg}'")

intent = slm.detect_search_intent(msg)
print(f"   Intent detected: {intent['is_search']}")
print(f"   Query: {intent['query']}")

if intent['is_search']:
    result = slm.process_message(msg)
    print(f"   Has links: {result['has_smart_links']}")
    print(f"   Results: {len(result['results']) if result['results'] else 0}")
    
    if result['results']:
        print(f"\n   Primo risultato:")
        print(f"     Title: {result['results'][0]['title']}")
        print(f"     URL: {result['results'][0]['href']}")
    else:
        print("   PROBLEMA: 0 risultati!")
        print(f"   Response: {result['response'][:100]}")

print("\n" + "="*50)
print("FINE TEST")
print("="*50)

