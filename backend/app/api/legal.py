"""Legal pages - Privacy & Terms"""
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AI Trading System</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
            line-height: 1.7;
            padding: 2rem;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .subtitle {{ color: #94a3b8; margin-bottom: 2rem; }}
        section {{ margin-bottom: 2rem; }}
        h2 {{ font-size: 1.5rem; margin-bottom: 1rem; color: #a5b4fc; }}
        p {{ color: #cbd5e1; margin-bottom: 1rem; }}
        ul {{ margin-left: 1.5rem; color: #cbd5e1; }}
        li {{ margin-bottom: 0.5rem; }}
        a {{ color: #818cf8; }}
        .footer {{ margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #334155; text-align: center; color: #64748b; }}
    </style>
</head>
<body>
    <div class="container">
        {content}
        <div class="footer">
            <p>&copy; 2026 AI Trading System. All rights reserved. | <a href="/terms">Terms</a> | <a href="/">Home</a></p>
        </div>
    </div>
</body>
</html>
"""

PRIVACY_HTML = """
<h1>Privacy Policy</h1>
<p class="subtitle">Last updated: April 2, 2026</p>

<section>
    <h2>1. Introduction</h2>
    <p>AI Trading System ("we", "us", "our") provides an intelligent agenda and productivity platform. This Privacy Policy explains how we collect, use, and safeguard your information.</p>
</section>

<section>
    <h2>2. Information We Collect</h2>
    <ul>
        <li><strong>Personal Data:</strong> Name, email (if provided)</li>
        <li><strong>Usage Data:</strong> IP address, browser type, pages visited</li>
        <li><strong>Your Data:</strong> Agenda entries, goals, diary entries, expenses you create</li>
    </ul>
</section>

<section>
    <h2>3. How We Use Your Information</h2>
    <ul>
        <li>Provide agenda and diary services</li>
        <li>AI-powered suggestions and analysis</li>
        <li>Improve user experience</li>
    </ul>
</section>

<section>
    <h2>4. Data Storage</h2>
    <p>Your data is stored securely. We implement encryption and security measures to protect your information.</p>
</section>

<section>
    <h2>5. Your Rights (GDPR)</h2>
    <p>You may request deletion of your data at any time by contacting us.</p>
</section>

<section>
    <h2>6. Contact</h2>
    <p>Email: <a href="mailto:ballales1984@yahoo.it">ballales1984&#64;yahoo.it</a></p>
</section>
"""

TERMS_HTML = """
<h1>Terms of Service</h1>
<p class="subtitle">Last updated: April 2, 2026</p>

<section>
    <h2>1. Acceptance</h2>
    <p>By using this service, you agree to these terms. If you do not agree, please do not use the service.</p>
</section>

<section>
    <h2>2. Description</h2>
    <p>AI Trading System provides intelligent agenda management, diary, goal tracking, expense tracking, and AI-powered features.</p>
</section>

<section>
    <h2>3. Acceptable Use</h2>
    <p>You agree NOT to:</p>
    <ul>
        <li>Use for illegal purposes</li>
        <li>Attempt to compromise the service</li>
        <li>Resell the service without authorization</li>
    </ul>
</section>

<section>
    <h2>4. Limitation of Liability</h2>
    <p>The service is provided "as is" without warranties. We are not liable for any damages.</p>
</section>

<section>
    <h2>5. Contact</h2>
    <p>Email: <a href="mailto:ballales1984@yahoo.it">ballales1984&#64;yahoo.it</a></p>
</section>
"""

@router.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return HTML_TEMPLATE.format(title="Privacy Policy", content=PRIVACY_HTML)

@router.get("/terms", response_class=HTMLResponse)
async def terms():
    return HTML_TEMPLATE.format(title="Terms of Service", content=TERMS_HTML)
