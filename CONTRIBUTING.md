# 🤝 Contributing to Assistente Intelligente

**First off, thank you!** ❤️

We're building the first social network that actually makes you better. Your contribution matters!

---

## 🌟 Ways to Contribute

### 1. 💻 Code Contributions

**Areas we need help:**
- Backend (Python/Flask)
- Frontend (JavaScript/HTML/CSS)
- Mobile (PWA optimization, future native apps)
- AI/ML (sentiment analysis, matching algorithms)
- DevOps (deployment, monitoring, scaling)
- Security (audits, best practices)

### 2. 🎨 Design Contributions

**What we need:**
- UI/UX improvements
- Community features mockups
- Branding & identity
- Illustrations
- Icons
- Animations

### 3. 🌍 Translations

**Current languages:** IT, EN, ES, ZH, RU, HI, AR  
**Target:** 20+ languages

Help us reach billions!

### 4. 📝 Documentation

**Always needed:**
- Code documentation
- User guides
- API docs
- Video tutorials
- Blog posts

### 5. 🧪 Testing & Bug Reports

- Test new features
- Report bugs
- Suggest improvements
- Beta testing community features

### 6. 💬 Community Management

- Welcome new contributors
- Answer questions
- Moderate community (when launched)
- Create content

---

## 🚀 Getting Started

### Step 1: Setup Development Environment

**Prerequisites:**
- Python 3.11+
- Git
- PostgreSQL (for advanced features, SQLite works for basics)

**Clone & Install:**
```bash
# Fork the repo on GitHub first!
git clone https://github.com/YOUR_USERNAME/assistente-intelligente-agenda.git
cd assistente-intelligente-agenda

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Testing tools

# Run the app
python run.py

# Visit http://localhost:5000
```

### Step 2: Find an Issue

**Good First Issues:**
- Look for label `good-first-issue`
- These are beginner-friendly (< 4 hours work)
- Well documented with context

**Browse by Phase:**
- `Phase-1-MVP` - Foundation features (current priority!)
- `Phase-2-Growth` - Viral features
- `Phase-3-Scale` - Monetization
- `Phase-4-Platform` - Ecosystem

**Comment on Issue:**
"I'd like to work on this!" and we'll assign it to you.

### Step 3: Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code improvements
- `test/` - Testing

### Step 4: Make Your Changes

**Code Style:**
- Python: Follow PEP 8
- JavaScript: Use ES6+, semicolons optional but consistent
- Comments: Explain WHY, not WHAT
- Functions: Max 50 lines, single responsibility

**Testing:**
```bash
# Run tests
pytest

# Run specific test
pytest tests/test_community.py

# Coverage
pytest --cov=app tests/
```

### Step 5: Commit

**Commit Messages:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance

**Examples:**
```bash
git commit -m "feat(community): add reflection sharing"

git commit -m "fix(diary): sentiment analysis not working for Arabic"

git commit -m "docs(api): add examples for /api/reflections endpoint"
```

### Step 6: Push & Pull Request

```bash
git push origin feature/your-feature-name
```

**On GitHub:**
1. Go to your fork
2. Click "Compare & pull request"
3. Fill in the template:
   - What does this PR do?
   - Why is it needed?
   - How to test?
   - Screenshots (if UI)
4. Link related issue: "Closes #123"
5. Submit!

**PR Review:**
- We'll review within 48 hours
- May request changes
- Once approved, we'll merge!
- You'll be added to contributors list 🎉

---

## 📋 Pull Request Checklist

Before submitting:

- [ ] Code follows project style
- [ ] Tests pass (`pytest`)
- [ ] New tests added (if new feature)
- [ ] Documentation updated
- [ ] No lint errors
- [ ] Commit messages are clear
- [ ] PR description is complete
- [ ] Screenshots added (if UI change)

---

## 🎯 Development Guidelines

### Philosophy

**1. User First**
- Every feature must help the user
- No dark patterns
- No manipulation
- Privacy sacred

**2. Simplicity**
- Simple > complex
- Do one thing well
- Progressive disclosure

**3. Performance**
- Fast load times (< 2s)
- Optimize for mobile
- Minimize JS

**4. Accessibility**
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader friendly

**5. Security**
- Never trust client input
- Sanitize everything
- HTTPS everywhere
- Rate limiting

### Code Organization

```
app/
├── ai/              # AI/ML logic
├── core/            # Core business logic
├── managers/        # Feature managers
├── models/          # Database models
├── routes/          # API endpoints
└── utils/           # Helpers

static/              # CSS, JS, images
templates/           # HTML templates
tests/               # All tests
```

### Database Migrations

```bash
# Create migration
flask db migrate -m "Add reflections table"

# Apply migration
flask db upgrade

# Rollback
flask db downgrade
```

### API Design

**REST Conventions:**
```
GET    /api/resource       # List
GET    /api/resource/:id   # Get one
POST   /api/resource       # Create
PUT    /api/resource/:id   # Update
DELETE /api/resource/:id   # Delete
```

**Response Format:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message",
  "error": null
}
```

**Error Format:**
```json
{
  "success": false,
  "data": null,
  "message": "Human readable error",
  "error": {
    "code": "ERROR_CODE",
    "details": { ... }
  }
}
```

### Frontend Guidelines

**HTML:**
- Semantic tags (`<article>`, `<section>`, `<nav>`)
- Accessible (alt text, labels, ARIA)
- Valid HTML5

**CSS:**
- Mobile-first
- CSS variables for theming
- BEM naming (optional but nice)
- Dark mode support

**JavaScript:**
- ES6+ features
- Async/await > callbacks
- No jQuery (vanilla JS)
- Comment non-obvious code

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_community.py

# Specific test
pytest tests/test_community.py::test_share_reflection

# With coverage
pytest --cov=app --cov-report=html tests/
```

### Writing Tests

```python
# tests/test_community.py
import pytest
from app import create_app, db
from app.models import User, ReflectionShare

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_share_reflection(client):
    """Test user can share a reflection"""
    # Create user
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()
    
    # Share reflection
    response = client.post('/api/reflections', json={
        'text': 'Today I learned something amazing',
        'visibility': 'public',
        'category': 'personal_growth'
    })
    
    assert response.status_code == 201
    assert 'id' in response.json['data']
```

---

## 🐛 Bug Reports

**Use the Bug Report template on GitHub Issues**

**Include:**
1. What happened?
2. What should have happened?
3. Steps to reproduce
4. Environment (OS, browser, Python version)
5. Screenshots/logs

**Example:**
```
Title: Sentiment analysis fails for Arabic text

Description:
When I write a diary entry in Arabic and share it,
the sentiment shows as "neutral" even for clearly positive text.

Steps:
1. Switch to Arabic language
2. Write positive diary entry: "اليوم كان يوم رائع"
3. Share with community
4. Sentiment shows "neutral" instead of "positive"

Environment:
- OS: Windows 11
- Browser: Chrome 120
- Language: Arabic

Expected: Sentiment should be "positive"
Actual: Sentiment is "neutral"
```

---

## ✨ Feature Requests

**Use the Feature Request template**

**Include:**
1. Problem: What problem does this solve?
2. Solution: How should it work?
3. Alternatives: Any other ways to solve it?
4. Impact: Who benefits?

**Example:**
```
Title: Dark mode scheduling

Problem:
I want dark mode during night but light mode during day.
Switching manually is annoying.

Solution:
Auto-switch based on time or system preference.
Settings:
- [ ] Auto (follow system)
- [ ] Light
- [ ] Dark
- [ ] Scheduled (custom times)

Alternatives:
- Browser extension
- Always one mode

Impact:
- Every user (quality of life)
- Especially night users (eye strain)
```

---

## 💬 Communication Channels

### GitHub
- Issues: Bug reports, feature requests
- Discussions: Questions, ideas, show & tell
- Pull Requests: Code contributions

### Discord (Coming Soon)
- Real-time chat
- Help & questions
- Pair programming
- Community events

### Email
[To be added]

---

## 🏆 Recognition

### Contributors

Everyone who contributes gets:
- ✨ Name in CONTRIBUTORS.md
- 🎉 Mention in release notes
- 💎 Special badge in app (when launched)
- 🙏 Eternal gratitude!

### Top Contributors

Monthly recognition:
- 🥇 Most commits
- 🥈 Most helpful in community
- 🥉 Best feature contribution

### Hall of Fame

Major contributors:
- Core team invite
- Decision-making input
- Revenue share (if/when profitable)
- Co-ownership feeling

---

## ⚖️ Code of Conduct

### Our Pledge

We pledge to make participation in our project harassment-free for everyone, regardless of:
- Age, body size, disability
- Ethnicity, gender identity
- Experience level
- Nationality, personal appearance
- Race, religion, sexual identity

### Our Standards

**Positive behavior:**
- ✅ Using welcoming language
- ✅ Being respectful of differing viewpoints
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what's best for the community
- ✅ Showing empathy towards others

**Unacceptable:**
- ❌ Trolling, insulting, derogatory comments
- ❌ Public or private harassment
- ❌ Publishing others' private information
- ❌ Unprofessional conduct

### Enforcement

Violations will result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report to: [To be added]

---

## 🎓 Learning Resources

**New to Open Source?**
- [First Contributions](https://firstcontributions.github.io/)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)

**Python/Flask:**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Best Practices](https://docs.python-guide.org/)

**Git:**
- [Learn Git Branching](https://learngitbranching.js.org/)
- [Oh Shit, Git!?!](https://ohshitgit.com/)

**Testing:**
- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://testdriven.io/blog/testing-best-practices/)

---

## ❓ FAQ

**Q: I'm a beginner, can I contribute?**  
A: YES! Look for `good-first-issue` label. We mentor newcomers.

**Q: How long to review my PR?**  
A: Usually 24-48 hours. Be patient!

**Q: Can I work on multiple issues?**  
A: One at a time until first PR merged. Then go wild!

**Q: My PR was rejected, what now?**  
A: Don't be discouraged! Ask for feedback, improve, resubmit.

**Q: Can I suggest big changes?**  
A: Yes! Open a Discussion first to align on direction.

**Q: Will I get paid?**  
A: Not yet (we're pre-revenue). But top contributors will share in success!

**Q: How to become core team?**  
A: Contribute consistently for 3+ months, show commitment, we'll invite you.

---

## 🙏 Thank You!

Every contribution, no matter how small, makes this project better.

Together, we're building a social network that doesn't suck.

**Let's make the internet a better place!** ✨

---

**Made with ❤️ by contributors around the world 🌍**

[View all contributors](CONTRIBUTORS.md)

