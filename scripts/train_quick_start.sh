#!/bin/bash
# Quick start script per iniziare training subito

echo "🚀 QUICK START: Training NLP"
echo "=============================="

# 1. Setup directories
echo "📁 Creando directories..."
mkdir -p data models logs/training app/ai

# 2. Install dependencies
echo "📦 Installando dipendenze..."
pip install spacy spacy-transformers textblob scikit-learn
python -m spacy download it_core_news_lg

# 3. Generate synthetic data
echo "🤖 Generando dataset sintetico..."
python scripts/generate_synthetic_data.py

# 4. Extract real inputs (if available)
echo "🔍 Estraendo input reali..."
python scripts/extract_user_inputs.py || echo "⚠️  Skip (no logs yet)"

# 5. Combine datasets
echo "🔗 Combinando datasets..."
if [ -f "data/dataset_real_inputs.json" ]; then
    jq -s 'add' data/dataset_real_inputs.json data/dataset_synthetic_800.json > data/dataset_combined.json
    echo "✅ Dataset combinato creato (real + synthetic)"
else
    cp data/dataset_synthetic_800.json data/dataset_combined.json
    echo "✅ Usando solo dataset sintetico"
fi

# 6. Create basic training script
echo "📝 Creando training script base..."
cat > train_nlp_model.py << 'EOF'
#!/usr/bin/env python3
"""
Script base per training NLP model.
"""

import spacy
from spacy.training import Example
import json
import random

def load_dataset(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def train_simple(dataset_path, output_path="models/nlp_v1", n_iter=30):
    print(f"🧠 Training model...")
    print(f"   Dataset: {dataset_path}")
    print(f"   Iterations: {n_iter}")
    
    # Load data
    data = load_dataset(dataset_path)
    random.shuffle(data)
    
    # Split
    split = int(len(data) * 0.8)
    train_data = data[:split]
    val_data = data[split:]
    
    print(f"   Train: {len(train_data)}, Val: {len(val_data)}")
    
    # Create model
    nlp = spacy.blank("it")
    textcat = nlp.add_pipe("textcat_multilabel")
    
    # Add labels
    labels = set(item['intent'] for item in train_data)
    for label in labels:
        textcat.add_label(label)
    
    print(f"   Labels: {', '.join(labels)}")
    
    # Prepare training data
    train_examples = []
    for item in train_data:
        doc = nlp.make_doc(item['text'])
        cats = {label: label == item['intent'] for label in labels}
        train_examples.append(Example.from_dict(doc, {"cats": cats}))
    
    # Train
    optimizer = nlp.initialize()
    
    for i in range(n_iter):
        random.shuffle(train_examples)
        losses = {}
        
        # Update in batches
        for batch in spacy.util.minibatch(train_examples, size=8):
            nlp.update(batch, sgd=optimizer, losses=losses)
        
        if (i + 1) % 5 == 0:
            print(f"   Iter {i+1}/{n_iter}: loss={losses['textcat_multilabel']:.4f}")
    
    # Evaluate
    print("\n📊 Evaluating...")
    val_examples = []
    for item in val_data:
        doc = nlp.make_doc(item['text'])
        cats = {label: label == item['intent'] for label in labels}
        val_examples.append(Example.from_dict(doc, {"cats": cats}))
    
    scores = nlp.evaluate(val_examples)
    print(f"   Accuracy: {scores['cats_score']:.2%}")
    
    # Save
    nlp.to_disk(output_path)
    print(f"\n💾 Model saved to {output_path}")
    
    return nlp

if __name__ == "__main__":
    import sys
    
    dataset = sys.argv[1] if len(sys.argv) > 1 else "data/dataset_combined.json"
    
    try:
        model = train_simple(dataset)
        print("\n✅ Training completato con successo!")
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        sys.exit(1)
EOF

chmod +x train_nlp_model.py

# 7. Run training
echo ""
echo "🎯 Vuoi iniziare training ora? (y/n)"
read -r response

if [ "$response" = "y" ]; then
    echo "🏃 Running training..."
    python train_nlp_model.py data/dataset_combined.json
else
    echo "⏸️  Training skipped. Run manualmente:"
    echo "   python train_nlp_model.py data/dataset_combined.json"
fi

echo ""
echo "✅ Setup completo!"
echo ""
echo "📋 Prossimi step:"
echo "   1. Rivedi dataset in data/dataset_combined.json"
echo "   2. Aggiungi esempi reali da logs"
echo "   3. Run training: python train_nlp_model.py"
echo "   4. Test model: python -c 'import spacy; nlp=spacy.load(\"models/nlp_v1\"); print(nlp(\"domani riunione 10-12\").cats)'"
echo "   5. Integra in app/routes/api.py"

