#!/usr/bin/env python3
"""
🌍 MULTILANGUAGE SYNC SCRIPT
Sincronizza automaticamente tutte le versioni linguistiche con la versione base italiana.

Author: Assistente AI
Date: 5 Nov 2025
"""

import re
import os
from datetime import datetime
from pathlib import Path

# ========================================
# CONFIGURAZIONE
# ========================================

TEMPLATES_DIR = Path("templates")
BACKUP_DIR = Path("backup_multilang_" + datetime.now().strftime("%Y%m%d_%H%M%S"))

# File base (versioni italiane - fonte di verità)
BASE_FILES = {
    "index": "index.html",
    "community": "community.html",
    "about": "about.html"
}

# Versioni tradotte da sincronizzare
TRANSLATED_FILES = {
    "index": [
        "index_en_full.html",
        "index_es.html",
        "index_zh.html",
        "index_hi.html",
        "index_ru.html",
        "index_ar.html"
    ],
    "community": [
        "community_en.html",
        "community_es.html"
    ],
    "about": [
        "about_en.html"
    ]
}

# ========================================
# FUNZIONI UTILITY
# ========================================

def extract_js_functions(html_content):
    """
    Estrae tutte le funzioni JavaScript da un file HTML.
    Ritorna dict: {"function_name": "full_function_code"}
    """
    functions = {}
    
    # Pattern per funzioni async/sync
    patterns = [
        r'(async\s+function\s+(\w+)\s*\([^)]*\)\s*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})',
        r'(function\s+(\w+)\s*\([^)]*\)\s*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})',
        r'(const\s+(\w+)\s*=\s*async\s*\([^)]*\)\s*=>\s*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})',
        r'(const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, html_content, re.DOTALL)
        for match in matches:
            func_code = match.group(1)
            func_name = match.group(2)
            functions[func_name] = func_code
    
    return functions

def extract_script_section(html_content):
    """Estrae l'intera sezione <script>...</script>"""
    match = re.search(r'<script>(.*?)</script>', html_content, re.DOTALL)
    return match.group(1) if match else ""

def get_file_stats(filepath):
    """Ritorna statistiche file"""
    if not filepath.exists():
        return {"exists": False}
    
    content = filepath.read_text(encoding='utf-8')
    functions = extract_js_functions(content)
    
    return {
        "exists": True,
        "size_kb": filepath.stat().st_size / 1024,
        "lines": len(content.split('\n')),
        "functions_count": len(functions),
        "functions": list(functions.keys()),
        "last_modified": datetime.fromtimestamp(filepath.stat().st_mtime)
    }

def backup_file(filepath):
    """Crea backup di un file"""
    if not filepath.exists():
        return None
    
    BACKUP_DIR.mkdir(exist_ok=True)
    backup_path = BACKUP_DIR / filepath.name
    backup_path.write_text(filepath.read_text(encoding='utf-8'), encoding='utf-8')
    return backup_path

def compare_functions(base_funcs, translated_funcs):
    """Confronta funzioni e trova differenze"""
    base_names = set(base_funcs.keys())
    translated_names = set(translated_funcs.keys())
    
    return {
        "missing": base_names - translated_names,
        "extra": translated_names - base_names,
        "common": base_names & translated_names
    }

def insert_missing_functions(html_content, missing_functions, base_functions):
    """
    Inserisce le funzioni mancanti nel file HTML tradotto.
    Cerca il blocco <script> e inserisce prima del </script>
    """
    if not missing_functions:
        return html_content
    
    # Trova il tag </script> finale
    script_end_match = re.search(r'(\s*)</script>', html_content, re.DOTALL)
    if not script_end_match:
        print("⚠️  WARNING: No </script> tag found!")
        return html_content
    
    insert_position = script_end_match.start(1)
    
    # Costruisci il codice da inserire
    functions_code = "\n\n        // ========================================\n"
    functions_code += "        // 🔄 AUTO-SYNCED FUNCTIONS (sync_multilang.py)\n"
    functions_code += f"        // Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    functions_code += "        // ========================================\n\n"
    
    for func_name in sorted(missing_functions):
        if func_name in base_functions:
            functions_code += f"        // Function: {func_name}\n"
            functions_code += "        " + base_functions[func_name].replace("\n", "\n        ") + "\n\n"
    
    # Inserisci il codice
    new_content = html_content[:insert_position] + functions_code + html_content[insert_position:]
    
    return new_content

# ========================================
# FUNZIONE PRINCIPALE DI SYNC
# ========================================

def sync_file_group(group_name, base_filename, translated_filenames):
    """
    Sincronizza un gruppo di file (es. tutti gli index_*.html)
    """
    print(f"\n{'='*70}")
    print(f"🔄 SYNCING: {group_name.upper()}")
    print(f"{'='*70}")
    
    base_path = TEMPLATES_DIR / base_filename
    
    if not base_path.exists():
        print(f"❌ Base file not found: {base_path}")
        return
    
    # Analizza file base
    print(f"\n📊 BASE FILE: {base_filename}")
    base_stats = get_file_stats(base_path)
    print(f"   Size: {base_stats['size_kb']:.1f} KB")
    print(f"   Lines: {base_stats['lines']}")
    print(f"   Functions: {base_stats['functions_count']}")
    print(f"   Last Modified: {base_stats['last_modified'].strftime('%Y-%m-%d %H:%M')}")
    
    base_content = base_path.read_text(encoding='utf-8')
    base_functions = extract_js_functions(base_content)
    
    # Sincronizza ogni file tradotto
    results = []
    
    for translated_filename in translated_filenames:
        translated_path = TEMPLATES_DIR / translated_filename
        
        print(f"\n🌍 TRANSLATING: {translated_filename}")
        
        if not translated_path.exists():
            print(f"   ⚠️  File not found - SKIP")
            results.append({"file": translated_filename, "status": "NOT_FOUND"})
            continue
        
        # Stats prima della sync
        before_stats = get_file_stats(translated_path)
        print(f"   BEFORE: {before_stats['size_kb']:.1f} KB, {before_stats['functions_count']} functions")
        
        # Confronta funzioni
        translated_content = translated_path.read_text(encoding='utf-8')
        translated_functions = extract_js_functions(translated_content)
        
        comparison = compare_functions(base_functions, translated_functions)
        
        print(f"   Missing: {len(comparison['missing'])} functions")
        if comparison['missing']:
            print(f"      → {', '.join(sorted(comparison['missing']))}")
        
        if len(comparison['missing']) == 0:
            print(f"   ✅ ALREADY UP-TO-DATE")
            results.append({"file": translated_filename, "status": "UP_TO_DATE"})
            continue
        
        # Backup
        backup_path = backup_file(translated_path)
        print(f"   💾 Backup: {backup_path.name}")
        
        # Inserisci funzioni mancanti
        new_content = insert_missing_functions(translated_content, comparison['missing'], base_functions)
        
        # Salva file aggiornato
        translated_path.write_text(new_content, encoding='utf-8')
        
        # Stats dopo la sync
        after_stats = get_file_stats(translated_path)
        print(f"   AFTER:  {after_stats['size_kb']:.1f} KB, {after_stats['functions_count']} functions")
        print(f"   ✅ SYNCED (+{len(comparison['missing'])} functions)")
        
        results.append({
            "file": translated_filename,
            "status": "SYNCED",
            "added_functions": len(comparison['missing']),
            "size_before": before_stats['size_kb'],
            "size_after": after_stats['size_kb']
        })
    
    return results

# ========================================
# MAIN
# ========================================

def main():
    print("=" * 70)
    print("🌍 MULTILANGUAGE SYNC TOOL")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Backup dir: {BACKUP_DIR}")
    
    all_results = {}
    
    # Sincronizza ogni gruppo
    for group_name in ["index", "community", "about"]:
        if group_name not in BASE_FILES:
            continue
        
        base_file = BASE_FILES[group_name]
        translated_files = TRANSLATED_FILES.get(group_name, [])
        
        if not translated_files:
            continue
        
        results = sync_file_group(group_name, base_file, translated_files)
        all_results[group_name] = results
    
    # Report finale
    print(f"\n{'='*70}")
    print("📊 FINAL REPORT")
    print(f"{'='*70}")
    
    total_synced = 0
    total_uptodate = 0
    total_notfound = 0
    
    for group_name, results in all_results.items():
        print(f"\n{group_name.upper()}:")
        for result in results:
            status = result['status']
            if status == "SYNCED":
                total_synced += 1
                print(f"  ✅ {result['file']}: +{result['added_functions']} functions")
            elif status == "UP_TO_DATE":
                total_uptodate += 1
                print(f"  ✅ {result['file']}: Already up-to-date")
            elif status == "NOT_FOUND":
                total_notfound += 1
                print(f"  ⚠️  {result['file']}: File not found")
    
    print(f"\n{'='*70}")
    print(f"SUMMARY:")
    print(f"  ✅ Synced: {total_synced} files")
    print(f"  ✅ Up-to-date: {total_uptodate} files")
    print(f"  ⚠️  Not found: {total_notfound} files")
    print(f"  💾 Backups: {BACKUP_DIR}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()

