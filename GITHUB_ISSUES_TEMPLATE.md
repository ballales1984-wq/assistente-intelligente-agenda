# 📋 GitHub Issues da Creare (Copy-Paste)

Questi sono issue di esempio per iniziare ad attrarre contributor.  
**Copiali su GitHub Issues quando sei pronto!**

---

## 🌱 GOOD FIRST ISSUES (Beginner Friendly)

### Issue #1: Add French Translation (Facile - 2h)

```markdown
**Title:** 🌍 Add French translation (fr.json)

**Description:**

We want to expand from 7 languages to 20+! Let's start with French.

**Task:**
Create `static/i18n/fr.json` with French translations of all UI strings.

**Steps:**
1. Copy `static/i18n/en.json` as template
2. Translate all 61 strings to French
3. Test by temporarily changing `lang="fr"` in `templates/index.html`
4. Submit PR!

**Files to create:**
- `static/i18n/fr.json`

**Difficulty:** Easy  
**Time:** ~2 hours  
**Good for:** Native French speakers, translation enthusiasts

**Labels:** `good-first-issue`, `translations`, `help-wanted`
```

---

### Issue #2: Add German Translation (Facile - 2h)

```markdown
**Title:** 🌍 Add German translation (de.json)

**Description:**

Same as French! Germany has 83M people + Austria + Switzerland = 100M+ potential users.

**Task:**
Create `static/i18n/de.json` with German translations.

**Steps:**
1. Copy `static/i18n/en.json`
2. Translate to German
3. Submit PR!

**Difficulty:** Easy  
**Time:** ~2 hours  
**Labels:** `good-first-issue`, `translations`, `help-wanted`
```

---

### Issue #3: Improve Dark Mode Contrast (Facile - 3h)

```markdown
**Title:** 🎨 Improve dark mode text contrast for accessibility

**Description:**

Current dark mode has some text that's hard to read (low contrast).  
Let's make it WCAG AAA compliant!

**Task:**
Audit dark mode colors and improve contrast ratios.

**Steps:**
1. Enable dark mode on https://assistente-intelligente-agenda.onrender.com/
2. Use browser tools to check contrast ratios
3. Find text with contrast < 7:1
4. Update CSS in `templates/index.html` (search for `body.dark-mode`)
5. Test visually
6. Submit PR!

**Tool to use:**
- Chrome DevTools Lighthouse (accessibility audit)
- https://webaim.org/resources/contrastchecker/

**Difficulty:** Easy  
**Time:** ~3 hours  
**Good for:** Design-minded developers, accessibility advocates

**Labels:** `good-first-issue`, `design`, `accessibility`, `help-wanted`
```

---

### Issue #4: Add More Example Commands to Chat (Facile - 2h)

```markdown
**Title:** 💬 Add 5 more example commands to chat interface

**Description:**

Users don't know all the cool things they can ask!  
Let's add more example buttons.

**Current examples:**
- "Voglio studiare Python 3 ore a settimana"
- "Lunedì riunione dalle 10 alle 12"

**New examples to add:**
- "Quanto ho speso questa settimana?"
- "Mostrami il mio progresso"
- "Crea un report PDF"
- "Come sarà la mia giornata domani?"
- "Ho dormito male, mi sento stanco" (diario)

**Files to modify:**
- `templates/index.html` - Around line 1150 (example buttons section)
- Replicate for all language versions (index_en, index_es, etc.)

**Difficulty:** Easy  
**Time:** ~2 hours  
**Good for:** Frontend beginners

**Labels:** `good-first-issue`, `frontend`, `UX`, `help-wanted`
```

---

## 🛠️ INTERMEDIATE ISSUES

### Issue #5: Add Export to CSV for Goals (Medio - 4h)

```markdown
**Title:** 💾 Add CSV export for goals/objectives

**Description:**

Users can export diary and expenses to CSV, but not goals!  
Let's add it.

**Task:**
Implement CSV export for goals with progress tracking.

**Implementation:**

Backend (Python):
```python
# In app/routes/api.py

@bp.route('/api/export/goals/csv')
def export_goals_csv():
    profilo = UserProfile.query.first()
    obiettivi = profilo.obiettivi.all()
    
    # Create CSV
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Nome', 'Tipo', 'Ore/Settimana', 'Ore Completate', 'Progresso %'])
    
    for obj in obiettivi:
        progresso = (obj.ore_completate / (obj.durata_settimanale * 4)) * 100 if obj.durata_settimanale > 0 else 0
        writer.writerow([
            obj.nome, obj.tipo, obj.durata_settimanale, 
            obj.ore_completate, f"{progresso:.1f}%"
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=goals.csv'}
    )
```

Frontend: Add button in statistics section.

**Difficulty:** Medium  
**Time:** ~4 hours  
**Good for:** Backend developers learning Flask

**Labels:** `enhancement`, `backend`, `export`, `help-wanted`
```

---

### Issue #6: Add Voice Input for Chat (Medio - 6h)

```markdown
**Title:** 🎤 Add voice input for chat messages

**Description:**

Users should be able to speak instead of typing!  
Use Web Speech API (browser native, no costs).

**Task:**
Add microphone button next to chat input for voice-to-text.

**Implementation:**

```javascript
// In templates/index.html - add to chat section

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'it-IT';  // Dynamic based on current language

function startVoiceInput() {
    recognition.start();
    // Show visual feedback (pulsing mic icon)
}

recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById('chatInput').value = transcript;
    // Auto-send or let user edit?
};

recognition.onerror = function(event) {
    console.error('Voice recognition error:', event.error);
    showError('Microfono non disponibile');
};
```

**UI:**
- Mic button next to send button
- Pulse animation while listening
- Toast "Sto ascoltando..."
- Works on Chrome, Edge, Safari (not Firefox yet)

**Difficulty:** Medium  
**Time:** ~6 hours  
**Good for:** Frontend developers, UX enthusiasts

**Labels:** `enhancement`, `frontend`, `AI`, `accessibility`, `help-wanted`
```

---

## 🚀 ADVANCED ISSUES

### Issue #7: Implement Reflection Sharing Backend (Avanzato - 20h)

```markdown
**Title:** 🤝 Backend for community reflection sharing (Phase 1 MVP)

**Description:**

Core feature for community platform! Users need to opt-in share their diary reflections with community.

**See:** [ROADMAP_COMMUNITY.md](ROADMAP_COMMUNITY.md#1-sharing-riflessioni-settimana-1-2)

**Task:**
Implement complete backend for sharing system.

**Requirements:**

1. **New Model:** `app/models/reflection_share.py`
   - See roadmap for schema
   - Visibility levels (private, anonymous, friends, public)
   - Categories
   - Moderation support

2. **API Endpoints:** `app/routes/community.py`
   ```
   POST /api/reflections/share - Share a diary entry
   GET  /api/reflections/feed - Get community feed
   PUT  /api/reflections/:id - Update shared reflection
   DELETE /api/reflections/:id - Delete
   ```

3. **Business Logic:** `app/managers/community_manager.py`
   - Privacy validation
   - Content filtering (basic)
   - Feed algorithm (simple: recent first)

4. **Tests:** `tests/test_community_sharing.py`
   - Test all CRUD operations
   - Test visibility levels
   - Test filtering

**Deliverables:**
- [ ] Models defined
- [ ] API endpoints working
- [ ] Tests passing (>80% coverage)
- [ ] Documentation (docstrings)

**Difficulty:** Hard  
**Time:** ~20 hours  
**Good for:** Experienced Python developers

**Labels:** `Phase-1-MVP`, `backend`, `community`, `priority-high`
```

---

### Issue #8: Design Community Feed UI/UX (Avanzato - 15h)

```markdown
**Title:** 🎨 Design community feed interface (mockups + implementation)

**Description:**

The feed where users see shared reflections. This is THE core UI for community features.

**Requirements:**

**Must have:**
- Clean, calm aesthetic (not attention-grabbing like FB/Twitter)
- Card-based layout
- Sentiment color coding (subtle)
- Category filters
- Anonymous vs named display
- Reaction buttons (4 types, NO counter shown)
- Comment preview
- Mobile-first design

**Should NOT have:**
- Infinite scroll (max 20 items, then "load more")
- Like counters
- Follower counts
- Flashy colors
- Distracting animations

**Deliverables:**
1. Figma mockup (or similar)
2. HTML/CSS implementation in `templates/community_feed.html`
3. Responsive (mobile + desktop)
4. Dark mode support
5. Accessibility (ARIA labels, keyboard nav)

**Inspiration (but better!):**
- Medium article feed (calm)
- Reddit (simple cards)
- Hacker News (minimal)
- NOT: Twitter, FB, Instagram (too flashy)

**Difficulty:** Hard  
**Time:** ~15 hours  
**Good for:** UI/UX designers who code

**Labels:** `Phase-1-MVP`, `design`, `frontend`, `community`, `priority-high`
```

---

## 🎯 EPIC ISSUES (Multi-Feature)

### Issue #9: Build Accountability Circles Feature (Epic - 30h)

```markdown
**Title:** 🔵 Implement Accountability Circles (complete feature)

**Description:**

One of our unique features! Small groups (5-10 people) supporting each other.

**See:** [ROADMAP_COMMUNITY.md](ROADMAP_COMMUNITY.md#5-circles-mvp-settimana-7-8) for full spec

**This is a big one! Includes:**
1. Backend models (Circle, CircleMember)
2. API endpoints (CRUD circles, invite system)
3. Frontend UI (create, join, dashboard)
4. Permissions system
5. Notifications (circle activity)
6. Tests (comprehensive)

**Can be split into sub-tasks!**

**Difficulty:** Epic  
**Time:** ~30 hours  
**Good for:** Full-stack developers ready for challenge

**Labels:** `Phase-1-MVP`, `epic`, `fullstack`, `community`, `priority-high`
```

---

## 📊 ISSUE ORGANIZATION

### Labels da Creare su GitHub

**Priority:**
- `priority-critical` 🔴 - Blockers
- `priority-high` 🟠 - Important
- `priority-medium` 🟡 - Nice to have
- `priority-low` 🟢 - Future

**Type:**
- `bug` 🐛 - Something broken
- `enhancement` ✨ - New feature
- `documentation` 📝 - Docs
- `question` ❓ - Help needed
- `design` 🎨 - UI/UX

**Area:**
- `backend` - Python/Flask
- `frontend` - HTML/CSS/JS
- `ai` - Machine learning
- `community` - Community features
- `mobile` - PWA/Mobile
- `devops` - Infrastructure

**Phase:**
- `Phase-1-MVP` - Foundation (next 3 months)
- `Phase-2-Growth` - Viral features
- `Phase-3-Scale` - Monetization
- `Phase-4-Platform` - Ecosystem

**Difficulty:**
- `good-first-issue` 🌱 - Beginners welcome!
- `easy` - < 4 hours
- `medium` - 4-16 hours
- `hard` - 16-40 hours
- `epic` - 40+ hours

**Status:**
- `help-wanted` 🙋 - Looking for contributor
- `in-progress` 🔄 - Someone working on it
- `blocked` 🚫 - Waiting for something
- `ready-for-review` 👀 - PR submitted

---

## 🎯 MILESTONE ORGANIZATION

### Milestone 1: Community MVP (3 months)
- Reflection sharing
- Community feed
- Reactions
- Comments
- Circles v1

### Milestone 2: Growth Features (6 months)
- Matching algorithm
- Challenges
- Analytics
- Mobile optimization

### Milestone 3: Monetization (12 months)
- Premium tier
- B2B dashboard
- API v1
- 20+ languages

---

## 📝 QUICK COPY-PASTE GUIDE

### Crea Issue su GitHub:

1. Go to: https://github.com/ballales1984-wq/assistente-intelligente-agenda/issues/new
2. Copia uno degli issue sopra
3. Aggiungi labels appropriate
4. Assign a milestone
5. Publish!

**Quanti creare?** Start with 10-15 good first issues per attrarre contributor!

---

## 🎊 TIPS PER CONTRIBUTOR ENGAGEMENT

### 1. Rispondi Velocemente
- Entro 24h a ogni issue/PR
- Anche solo "Thanks! Looking into this"

### 2. Celebra Ogni Win
- First PR merged? Tweet it!
- Milestone raggiunto? Blog post!
- New contributor? Welcome pubblico!

### 3. Sii Accomodante
- Accetta PR imperfetti (puoi migliorare dopo)
- Newcomer sbaglia? Insegna con gentilezza
- Negative feedback? Stay positive

### 4. Show Progress
- Weekly update (anche piccolo)
- Changelog dettagliato
- Screenshots di features nuove

### 5. Make It Fun
- Emoji everywhere! 🎉
- Humor appropriato
- Celebrate silly bugs
- Thank contributors pubblicamente

---

**Ready to attract amazing contributors!** 🚀✨

