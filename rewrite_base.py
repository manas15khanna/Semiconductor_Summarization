import re

with open('Phase(FutureSite)/index.html', 'r') as f:
    html = f.read()

# Extract head content
head_match = re.search(r'<head>(.*?)</head>', html, re.DOTALL | re.IGNORECASE)
head_content = head_match.group(1) if head_match else ""

# Extract header
header_match = re.search(r'<header>(.*?)</header>', html, re.DOTALL | re.IGNORECASE)
header_content = header_match.group(0) if header_match else ""

# Extract footer
footer_match = re.search(r'<footer>(.*?)</footer>', html, re.DOTALL | re.IGNORECASE)
footer_content = footer_match.group(0) if footer_match else ""

# Fix paths to /static/
def fix_paths(text):
    text = re.sub(r'\./img1\.digitallocker\.gov\.in', '/static/img1.digitallocker.gov.in', text)
    text = re.sub(r'\./www\.ux4g\.gov\.in', '/static/www.ux4g.gov.in', text)
    text = re.sub(r'\./doc\.ux4g\.gov\.in', '/static/doc.ux4g.gov.in', text)
    return text

head_content = fix_paths(head_content)
header_content = fix_paths(header_content)
footer_content = fix_paths(footer_content)

# Modify header navigation to include our pages
# We will inject our links into the nav
nav_html = """
<ul class="navbar-nav ms-auto mb-2 mb-lg-0 pr-25">
  <li class="nav-item"><a class="nav-link {% if page_name == 'Dashboard' %}active{% endif %}" href="/">Dashboard</a></li>
  <li class="nav-item"><a class="nav-link {% if page_name == 'Projects' %}active{% endif %}" href="/projects">Projects</a></li>
  <li class="nav-item"><a class="nav-link {% if page_name == 'Search' %}active{% endif %}" href="/search">Search</a></li>
  <li class="nav-item"><a class="nav-link {% if page_name == 'Decisions' %}active{% endif %}" href="/decisions">Decisions</a></li>
  <li class="nav-item"><a class="nav-link {% if page_name == 'Risks' %}active{% endif %}" href="/risks">Risks</a></li>
  <li class="nav-item"><a class="nav-link {% if page_name == 'Actions' %}active{% endif %}" href="/actions">Actions</a></li>
</ul>
"""

header_content = re.sub(r'<ul class="navbar-nav .*?</ul>', nav_html, header_content, flags=re.DOTALL)

# Add custom CSS for overlay and spacing
head_content += """
    <link rel="stylesheet" href="/static/css/styles.css">
    <style>
        .page-shell { padding: 2rem 0; min-height: 60vh; }
        .hidden { display: none; }
    </style>
"""

base_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_content}
    <title>{{{{ page_name or "SCL Traceability System" }}}}</title>
</head>
<body>
    {header_content}
    
    <main id="main-content" class="container page-shell">
        {{% block content %}}{{% endblock %}}
    </main>

    {footer_content}

    <div id="processing-overlay" class="overlay hidden" aria-live="polite">
        <div class="overlay-panel">
            <div class="overlay-header">
                <h2>Processing Documents</h2>
                <button type="button" id="overlay-close" class="ghost-button">Hide</button>
            </div>
            <div id="overlay-jobs" class="overlay-jobs"></div>
        </div>
    </div>
    
    <script src="/static/www.ux4g.gov.in/templates/html-template-5/assets/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/app.js"></script>
</body>
</html>
"""

with open('app/templates/base.html', 'w') as f:
    f.write(base_html)

print("Updated base.html")
