#!/usr/bin/env python3
"""
Script per creare GIF animate da screenshot
Richiede: pip install pillow
"""
from PIL import Image
import os
import glob

def create_gif(image_folder, output_path, duration=1000):
    """
    Crea una GIF da una serie di immagini
    
    Args:
        image_folder: Cartella con le immagini
        output_path: Path dove salvare la GIF
        duration: Durata di ogni frame in millisecondi
    """
    # Trova tutte le immagini PNG nella cartella
    images = sorted(glob.glob(f"{image_folder}/*.png"))
    
    if not images:
        print(f"❌ Nessuna immagine trovata in {image_folder}")
        return
    
    print(f"📸 Trovate {len(images)} immagini")
    
    # Carica le immagini
    frames = []
    for img_path in images:
        print(f"  Caricando: {os.path.basename(img_path)}")
        img = Image.open(img_path)
        # Ridimensiona se troppo grande
        if img.width > 1200:
            ratio = 1200 / img.width
            new_size = (1200, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        frames.append(img)
    
    # Salva come GIF
    print(f"\n💾 Creazione GIF: {output_path}")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=True
    )
    
    # Controlla dimensione
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ GIF creata! Dimensione: {size_mb:.2f} MB")
    
    if size_mb > 3:
        print("⚠️ GIF troppo grande! Comprimi con ezgif.com")

def main():
    """Crea tutte le GIF necessarie"""
    print("🎬 Creazione GIF Animate\n")
    
    # Assicurati che la directory esista
    os.makedirs("static/gifs", exist_ok=True)
    
    # GIF 1: Chat to Goal (usa screenshot 3-4)
    print("\n1️⃣ GIF: Chat → Obiettivo")
    if os.path.exists("static/screenshots/demo/03-chat-example.png"):
        create_gif(
            "static/screenshots/demo",
            "static/gifs/chat-to-goal.gif",
            duration=1500  # 1.5 secondi per frame
        )
    
    # GIF 2: Plan Generation (usa screenshot calendario)
    print("\n2️⃣ GIF: Genera Piano")
    if os.path.exists("static/screenshots/demo/05-calendar.png"):
        # Per questa GIF servirebbe una sequenza, usiamo placeholder
        print("⚠️ Serve registrazione manuale per questa GIF")
    
    # GIF 3: Diary Sentiment
    print("\n3️⃣ GIF: Diario Sentiment")
    print("⚠️ Serve registrazione manuale per questa GIF")
    
    # GIF 4: Full Dashboard
    print("\n4️⃣ GIF: Dashboard Completa")
    print("⚠️ Serve registrazione manuale per questa GIF")
    
    print("\n\n💡 Per GIF migliori, usa ScreenToGif:")
    print("   https://www.screentogif.com/")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Errore: Pillow non installato!")
        print("\n📦 Installa con:")
        print("   pip install pillow")
    except Exception as e:
        print(f"❌ Errore: {e}")

