import os
import io # Used for handling string as file
import zipfile

def create_file(path, content):
    """Creates a file with the given content."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def create_placeholder_image(path, content):
    """Creates a simple placeholder image file (can be a tiny transparent GIF or just a dummy file)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Using a tiny transparent GIF base64 encoded as a placeholder
    # This is a very small, valid GIF image (1x1 pixel, transparent)
    gif_data = b'R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
    try:
        with open(path, 'wb') as f:
            f.write(io.BytesIO(gif_data).getvalue())
        print(f"Created placeholder image: {path}")
    except Exception as e:
        print(f"Could not create placeholder image {path}: {e}")


def create_project_structure(root_dir="adalapages"):
    """Creates the entire project directory and files."""
    print(f"Creating project '{root_dir}'...")

    # Create root directory
    os.makedirs(root_dir, exist_ok=True)
    os.chdir(root_dir) # Change into the root directory for easier path management

    # 1. GitHub Actions Workflow
    create_file(
        ".github/workflows/build-and-deploy.yml",
        """name: Deploy Ådala.se to GitHub Pages

on:
  push:
    branches:
      - main  # Trigger workflow on pushes to the main branch

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.x'

    - name: Install Markdown parser and templating engine
      run: pip install markdown jinja2 # markdown for parsing, jinja2 for templating HTML

    - name: Generate HTML from Markdown
      run: python ./.github/scripts/generate_pages.py # Executes our custom script

    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: './' # Upload the entire repository root as the artifact, containing generated HTML files

  deploy:
    needs: build
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
    )

    # 2. Python Script for Markdown rendering
    create_file(
        ".github/scripts/generate_pages.py",
        """import os
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Define paths
SOURCE_DIR = 'docs'
OUTPUT_DIR = '.' # Output to root for GitHub Pages
TEMPLATE_FILE = 'template.html'
NAV_LINKS = [
    {"text": "Hem", "url": "index.html"},
    {"text": "Om Ådala", "url": "about.html"},
    {"text": "Våra Produkter", "url": "products.html"},
    {"text": "Café", "url": "cafe.html"},
    {"text": "Besök Oss", "url": "contact.html"},
]

def generate_pages():
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))
    # Add now() function to Jinja2 environment for dynamic year in footer
    env.globals['now'] = datetime.now
    template = env.get_template(TEMPLATE_FILE)

    # Process Markdown files
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(SOURCE_DIR, filename)

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Separate front matter (metadata) from content
            # Simple parsing: assumes front matter is at the very beginning, enclosed by ---
            parts = content.split('---', 2)
            if len(parts) > 2:
                front_matter_str = parts[1]
                md_content = parts[2]
                metadata = parse_front_matter(front_matter_str)
            else:
                md_content = content
                metadata = {}

            # Convert Markdown to HTML
            html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

            # Determine output filename
            # Example: article-biodling.md -> biodling.html
            output_filename = filename.replace('article-', '').replace('.md', '.html')

            # Render HTML using template
            rendered_html = template.render(
                title=metadata.get('title', 'Ådala Frukt och Grönt'),
                description=metadata.get('description', 'Välkommen till Ådala Frukt och Grönt!'),
                content=html_content,
                nav_links=NAV_LINKS,
                current_page=output_filename
            )

            # Save the new HTML file
            output_filepath = os.path.join(OUTPUT_DIR, output_filename)
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            print(f"Generated {output_filepath}")

    # Ensure main static pages exist, creating them from template if not
    static_pages = ['index.html', 'about.html', 'cafe.html', 'contact.html', 'products.html', '404.html']
    for page in static_pages:
        # Check if the page was *not* generated from a Markdown file
        if not os.path.exists(os.path.join(OUTPUT_DIR, page)):
             # Create a very basic version for testing. In a real scenario, these would have specific content.
             # This part will be handled by the manual creation of index.html etc. below,
             # so this loop primarily ensures that if new static pages are added to NAV_LINKS, they get a placeholder.
             # For the current setup, we create the content for these files explicitly later.
             pass

def parse_front_matter(front_matter_str):
    metadata = {}
    for line in front_matter_str.strip().split('\\n'): # Changed to \\n for script generation
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip().strip('"\'') # Remove quotes
    return metadata

if __name__ == '__main__':
    generate_pages()
"""
    )


    # 3. Example Markdown Articles
    create_file(
        "docs/article-om-oss.md",
        """---
title: "Om Ådala Frukt och Grönt AB"
description: "Lär dig mer om vår historia, vision och hållbarhetsarbete på Ådala."
image: "/assets/img/adalagard.jpg"
date: "2025-05-21"
author: "Ådala Teamet"
---

# Om Ådala Frukt och Grönt AB

Välkommen till Ådala Frukt och Grönt AB, en plats där passion för naturen och hållbarhet går hand i hand med kärleken till god mat och dryck. Vi är en familjeägd gård som har odlat och vårdat marken i generationer, med rötter djupt i den lokala myllan.

## Vår Historia och Vision

Ådala Frukt och Grönt grundades med en enkel men kraftfull vision: att förse lokalsamhället med färska, närproducerade råvaror av högsta kvalitet, direkt från vår gård. Det som började som en liten odling har vuxit till en mångfacetterad verksamhet som omfattar allt från biodling och äppelodling till grönsaksland och ett mysigt gårdskafé.

Vi strävar efter att vara en förebild inom hållbar odling och ett levande bevis på att det går att driva ett framgångsrikt lantbruk i samklang med naturen. Varje beslut vi fattar, från hur vi sköter våra grödor till hur vi väljer våra samarbetspartners, är genomsyrat av ett ekologiskt tänkande och en djup respekt för miljön.

## Vårt Hållbarhetsarbete

På Ådala är hållbarhet inte bara ett modeord, det är grunden i allt vi gör.
* **Ekologisk Odling:** Vi använder inga kemiska bekämpningsmedel eller konstgödsel. Istället förlitar vi oss på naturens egna processer och smarta odlingsmetoder för att främja biologisk mångfald och jordhälsa.
* **Vattenförvaltning:** Vi arbetar aktivt med att optimera vår vattenförbrukning och återanvänder regnvatten när det är möjligt.
* **Energi:** Vårt mål är att på sikt vara helt självförsörjande på förnybar energi.
* **Biologisk Mångfald:** Vi har planterat vildängar och buskar för att locka till oss pollinerare och nyttodjur, vilket gynnar både våra grödor och den lokala ekologin.

## Möt Teamet Bakom Ådala

Vi är ett litet, men engagerat team som delar en gemensam passion för mat, odling och gästfrihet. Varje dag arbetar vi med hängivenhet för att du ska få uppleva det bästa Ådala har att erbjuda. Kom gärna förbi och säg hej nästa gång du besöker oss!

---

*Läs mer om våra specifika odlingar:*
* [Biodling på Ådala](/biodling.html)
* [Våra Äpplen](/applen.html)
"""
    )
    # Create other placeholder markdown files
    md_files = [
        "article-biodling.md", "article-appeltra.md", "article-hallon.md",
        "article-blabar.md", "article-gronsaksodling.md", "article-cafe.md"
    ]
    for md_file in md_files:
        title = md_file.replace('article-', '').replace('.md', '').replace('-', ' ').capitalize()
        create_file(f"docs/{md_file}", f"""---
title: "{title} på Ådala"
description: "Allt du behöver veta om vår {title.lower()}."
image: "/assets/img/{title.lower()}.jpg"
date: "2025-05-21"
author: "Ådala Teamet"
---

# {title} på Ådala

Här kan du läsa mer om vår verksamhet med {title.lower()}. Vi är stolta över att odla {title.lower()} med omsorg och respekt för naturen.

## Våra Metoder

Vi använder hållbara metoder för att säkerställa att våra {title.lower()} är av högsta kvalitet och producerade på ett miljövänligt sätt.

## Säsong och Tillgång

{title} är i säsong under [Ange månader]. Under denna period kan du [beskriv vad man kan göra, t.ex. självplocka eller köpa i gårdsbutiken].

---

*Besök oss gärna för att se mer!*
""")


    # 4. CSS File
    create_file(
        "assets/css/style.css",
        """/* Grundläggande stil för Ådala.se */

:root {
    /* Färgpalett */
    --color-primary-green: #4CAF50; /* Grön, t.ex. löv */
    --color-secondary-green: #8BC34A; /* Ljusare grön, t.ex. frisk grönska */
    --color-brown: #795548; /* Jord/träbrun */
    --color-yellow: #FFEB3B; /* Solgul/honungsgul */
    --color-blue: #2196F3; /* Himmelsblå/blåbärsblå */
    --color-accent-red: #F44336; /* Hallon/äppelröd */
    --color-text-dark: #333;
    --color-text-light: #f9f9f9;
    --color-background-light: #f9f9f9;
    --color-background-dark: #eee;
    --color-border: #ccc;

    /* Typografi */
    --font-heading: 'Lato', sans-serif; /* Exempel, behöver inkluderas via Google Fonts */
    --font-body: 'Merriweather', serif; /* Exempel, behöver inkluderas via Google Fonts */
}

/* Grundläggande reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-body);
    line-height: 1.6;
    color: var(--color-text-dark);
    background-color: var(--color-background-light);
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Header */
header {
    background-color: var(--color-primary-green);
    color: var(--color-text-light);
    padding: 1rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-family: var(--font-heading);
    font-size: 1.8rem;
    font-weight: bold;
    color: var(--color-text-light);
    text-decoration: none;
}

/* Navigering */
nav ul {
    list-style: none;
    display: flex;
}

nav ul li {
    margin-left: 20px;
}

nav ul li a {
    color: var(--color-text-light);
    text-decoration: none;
    font-weight: bold;
    padding: 5px 0;
    transition: color 0.3s ease;
}

nav ul li a:hover,
nav ul li a.active {
    color: var(--color-yellow);
}

/* Main Content */
main {
    flex: 1; /* Låter main expandera för att fylla ut utrymmet */
    padding: 20px 0;
}

article {
    background-color: #fff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading);
    color: var(--color-brown);
    margin-bottom: 15px;
}

h1 {
    font-size: 2.5rem;
    color: var(--color-primary-green);
}

h2 {
    font-size: 2rem;
    border-bottom: 2px solid var(--color-border);
    padding-bottom: 5px;
    margin-top: 30px;
}

p {
    margin-bottom: 15px;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px 0;
    border-radius: 5px;
}

ul, ol {
    margin-left: 20px;
    margin-bottom: 15px;
}

/* Footer */
footer {
    background-color: var(--color-brown);
    color: var(--color-text-light);
    text-align: center;
    padding: 1.5rem 0;
    margin-top: 40px;
}

footer p {
    margin: 0;
}

footer a {
    color: var(--color-yellow);
    text-decoration: none;
}

/* Responsiv design */
@media (max-width: 768px) {
    header .container {
        flex-direction: column;
        align-items: flex-start;
    }

    nav ul {
        flex-direction: column;
        width: 100%;
        margin-top: 10px;
    }

    nav ul li {
        margin: 5px 0;
        width: 100%;
    }

    nav ul li a {
        display: block;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }

    /* Hero section for index.html */
    .hero {
        text-align: center;
    }

    .hero h1 {
        font-size: 2.2rem;
    }

    .hero p {
        font-size: 1.1rem;
    }

    .cta-button {
        display: block;
        width: fit-content;
        margin: 20px auto;
        padding: 12px 25px;
        background-color: var(--color-accent-red);
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }

    .cta-button:hover {
        background-color: #d32f2f; /* Darker red */
    }

    .highlights {
        margin-top: 40px;
    }

    .highlights h2 {
        text-align: center;
        margin-bottom: 30px;
    }

    .grid-container {
        display: grid;
        grid-template-columns: 1fr; /* Single column on small screens */
        gap: 20px;
    }

    .grid-item {
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }

    .grid-item img {
        max-width: 100%;
        height: 150px; /* Fixed height for consistency */
        object-fit: cover;
        border-radius: 5px;
        margin-bottom: 15px;
    }

    .grid-item h3 {
        color: var(--color-primary-green);
        margin-bottom: 10px;
    }

    .cta-button-small {
        display: inline-block;
        background-color: var(--color-primary-green);
        color: white;
        padding: 8px 15px;
        text-decoration: none;
        border-radius: 5px;
        font-size: 0.9rem;
        transition: background-color 0.3s ease;
    }

    .cta-button-small:hover {
        background-color: var(--color-secondary-green);
    }
}

/* Desktop styles for grid-container */
@media (min-width: 769px) {
    .grid-container {
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); /* 2-4 columns */
    }
}

.error-container {
    text-align: center;
    padding: 50px 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 50px auto;
    max-width: 600px;
}
.error-container h1 {
    font-size: 4rem;
    color: var(--color-accent-red);
    margin-bottom: 20px;
}
.error-container p {
    font-size: 1.2rem;
    margin-bottom: 30px;
}
.error-container a {
    display: inline-block;
    background-color: var(--color-primary-green);
    color: white;
    padding: 10px 20px;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}
.error-container a:hover {
    background-color: var(--color-secondary-green);
}

"""
    )

    # 5. JavaScript File
    create_file(
        "assets/js/main.js",
        """document.addEventListener('DOMContentLoaded', function() {
    // Exempel: Markera aktiv länk i navigeringen
    const currentPath = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('nav ul li a');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href').split('/').pop(); // Get filename from href
        if (linkPath === currentPath) {
            link.classList.add('active');
        }
    });

    // Här kan du lägga till JavaScript för en hamburgermeny om du vill
    // För en GitHub Pages-lösning utan komplexa frameworks är detta en enkel metod.
    // Exempel på enkel hamburgermeny (kräver också CSS för .menu-toggle och .nav.show)
    /*
    const nav = document.querySelector('nav ul');
    const headerContainer = document.querySelector('header .container');
    const menuToggle = document.createElement('button');
    menuToggle.textContent = '☰';
    menuToggle.classList.add('menu-toggle');
    if (headerContainer) {
        headerContainer.appendChild(menuToggle);
    }


    menuToggle.addEventListener('click', function() {
        if (nav) {
            nav.classList.toggle('show');
        }
    });
    */
});
"""
    )

    # 6. HTML Template
    create_file(
        "template.html",
        """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Ådala Frukt och Grönt</title>
    <meta name="description" content="{{ description }}">
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <div class="container">
            <a href="/index.html" class="logo">Ådala Frukt & Grönt</a>
            <nav>
                <ul>
                    {% for link in nav_links %}
                    <li><a href="{{ link.url }}" {% if link.url == current_page %}class="active"{% endif %}>{{ link.text }}</a></li>
                    {% endfor %}
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <article>
                {{ content | safe }} {# 'safe' is crucial for Jinja2 to render HTML from Markdown #}
            </article>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© {{ now().year }} Ådala Frukt och Grönt AB. Alla rättigheter reserverade.</p>
            <p><a href="/contact.html">Kontakta oss</a></p>
        </div>
    </footer>

    <script src="/assets/js/main.js"></script>
</body>
</html>
"""
    )

    # 7. Index HTML
    create_file(
        "index.html",
        """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Välkommen till Ådala Frukt och Grönt</title>
    <meta name="description" content="Upptäck Ådala Frukt och Grönt AB – din lokala källa för färska frukter, grönsaker, honung och ett mysigt gårdskafé.">
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <div class="container">
            <a href="/index.html" class="logo">Ådala Frukt & Grönt</a>
            <nav>
                <ul>
                    <li><a href="/index.html" class="active">Hem</a></li>
                    <li><a href="/about.html">Om Ådala</a></li>
                    <li><a href="/products.html">Våra Produkter</a></li>
                    <li><a href="/cafe.html">Café</a></li>
                    <li><a href="/contact.html">Besök Oss</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <section class="hero">
                <h1>Välkommen till Ådala Frukt och Grönt AB</h1>
                <p>Din lokala pärla för närproducerade läckerheter direkt från gården.</p>
                <img src="/assets/img/main-hero.jpg" alt="Färsk frukt och grönt på en gård">
                <p>Vi erbjuder allt från söt honung till krispiga äpplen, saftiga hallon, solmogna blåbär och ett brett utbud av ekologiska grönsaker. Koppla av i vårt enkla café och njut av lugnet på landsbygden.</p>
                <a href="/products.html" class="cta-button">Utforska Våra Produkter</a>
            </section>

            <section class="highlights">
                <h2>Vad vi erbjuder</h2>
                <div class="grid-container">
                    <div class="grid-item">
                        <img src="/assets/img/biodling-thumb.jpg" alt="Bikupa och bin">
                        <h3>Biodling & Honung</h3>
                        <p>Vår egen honung från glada bin som pollinerar våra odlingar.</p>
                        <a href="/biodling.html" class="cta-button-small">Läs mer</a>
                    </div>
                    <div class="grid-item">
                        <img src="/assets/img/appeltra-thumb.jpg" alt="Äppelträd med äpplen">
                        <h3>Fruktodlingar</h3>
                        <p>Äpplen, hallon och blåbär – direkt från våra buskar och träd.</p>
                        <a href="/products.html" class="cta-button-small">Se vårt utbud</a>
                    </div>
                    <div class="grid-item">
                        <img src="/assets/img/gronsaker-thumb.jpg" alt="Grönsaksland">
                        <h3>Grönsaksland</h3>
                        <p>Säsongsbetonade grönsaker odlade med omsorg och respekt för naturen.</p>
                        <a href="/gronsaksodling.html" class="cta-button-small">Upptäck grönsakerna</a>
                    </div>
                    <div class="grid-item">
                        <img src="/assets/img/cafe-thumb.jpg" alt="Caféinteriör">
                        <h3>Ådala Café</h3>
                        <p>Enkel fika och avkoppling i en charmig lantlig miljö.</p>
                        <a href="/cafe.html" class="cta-button-small">Besök caféet</a>
                    </div>
                </div>
            </section>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2025 Ådala Frukt och Grönt AB. Alla rättigheter reserverade.</p>
            <p><a href="/contact.html">Kontakta oss</a></p>
        </div>
    </footer>

    <script src="/assets/js/main.js"></script>
</body>
</html>
"""
    )

    # 8. About HTML
    create_file(
        "about.html",
        """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Om Ådala - Ådala Frukt och Grönt</title>
    <meta name="description" content="Lär dig mer om vår historia, vision och hållbarhetsarbete på Ådala.">
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <div class="container">
            <a href="/index.html" class="logo">Ådala Frukt & Grönt</a>
            <nav>
                <ul>
                    <li><a href="/index.html">Hem</a></li>
                    <li><a href="/about.html" class="active">Om Ådala</a></li>
                    <li><a href="/products.html">Våra Produkter</a></li>
                    <li><a href="/cafe.html">Café</a></li>
                    <li><a href="/contact.html">Besök Oss</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <article>
                <h1>Om Ådala Frukt och Grönt AB</h1>
                <p>Ådala Frukt och Grönt AB är mer än bara en gård – det är ett arv, en passion och ett åtagande för hållbarhet. Vår resa började för flera generationer sedan, när våra förfäder först bruka den frodiga jorden här i Ådala.</p>
                <img src="/assets/img/adalagard.jpg" alt="Ådala Gård">
                <h2>Vår Vision</h2>
                <p>Vår vision är att vara en plats där människor kan återknyta kontakten med naturen, förstå var maten kommer ifrån och njuta av äkta smaker. Vi strävar efter att odla med respekt för jorden och dess ekosystem, och att inspirera andra till en mer hållbar livsstil.</p>
                <h2>Hållbarhet i Praktiken</h2>
                <p>På Ådala Frukt och Grönt tar vi hållbarhet på allvar. Vi arbetar aktivt med:
                <ul>
                    <li>**Ekologisk odling:** Inga kemiska bekämpningsmedel eller konstgödsel.</li>
                    <li>**Vattenhushållning:** Effektiv bevattning och insamling av regnvatten.</li>
                    <li>**Biologisk mångfald:** Skapa livsmiljöer för pollinerare och nyttodjur.</li>
                    <li>**Korta led:** Minimera transporter genom att sälja direkt från gården och till lokala butiker.</li>
                </ul>
                </p>
                <h2>Vårt Team</h2>
                <p>Bakom Ådala finns ett dedikerat team som delar en gemensam passion för odling och gästfrihet. Vi älskar det vi gör och ser fram emot att välkomna dig till vår gård!</p>
            </article>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2025 Ådala Frukt och Grönt AB. Alla rättigheter reserverade.</p>
            <p><a href="/contact.html">Kontakta oss</a></p>
        </div>
    </footer>

    <script src="/assets/js/main.js"></script>
</body>
</html>
"""
    )

    # 9. Cafe HTML
    create_file(
        "cafe.html",
        """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ådala Café - Ådala Frukt och Grönt</title>
    <meta name="description" content="Besök Ådala Café för en enkel fika och avkoppling i en charmig lantlig miljö.">
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <div class="container">
            <a href="/index.html" class="logo">Ådala Frukt & Grönt</a>
            <nav>
                <ul>
                    <li><a href="/index.html">Hem</a></li>
                    <li><a href="/about.html">Om Ådala</a></li>
                    <li><a href="/products.html">Våra Produkter</a></li>
                    <li><a href="/cafe.html" class="active">Café</a></li>
                    <li><a href="/contact.html">Besök Oss</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <article>
                <h1>Välkommen till Ådala Café</h1>
                <p>Efter en härlig promenad bland odlingarna eller en tur i vår gårdsbutik, varför inte slå dig ner i vårt enkla men charmiga gårdskafé? Här kan du koppla av med en kopp kaffe och hembakat, ofta med ingredienser direkt från vår egen gård.</p>
                <img src="/assets/img/cafe-interior.jpg" alt="Interiör i Ådala Café">
                <h2>Öppettider</h2>
                <p>Vi har öppet:</p>
                <ul>
                    <li>Lördag-Söndag: 10:00 - 16:00 (under säsong)</li>
                    <li>Under vardagar: Se våra sociala medier för aktuella öppettider vid evenemang.</li>
                </ul>
                <p>Kontakta oss gärna vid större sällskap eller frågor.</p>
                <h2>Vårt Utbud</h2>
                <p>Vi fokuserar på enkelhet och kvalitet. På menyn hittar du vanligtvis:</p>
                <ul>
                    <li>Nybryggt kaffe och te</li>
                    <li>Hembakad äppelkaka (med äpplen från gården, såklart!)</li>
                    <li>Hallon- och blåbärspajer (i säsong)</li>
                    <li>Enklare smörgåsar</li>
                    <li>Vår egen honungslimpa</li>
                </ul>
                <p>Utbudet kan variera beroende på säsong och tillgång på råvaror från gården.</p>
                <a href="/contact.html" class="cta-button">Hitta till oss och kontakta oss</a>
            </article>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2025 Ådala Frukt och Grönt AB. Alla rättigheter reserverade.</p>
            <p><a href="/contact.html">Kontakta oss</a></p>
        </div>
    </footer>

    <script src="/assets/js/main.js"></script>
</body>
</html>
"""
    )

    # 10. Contact HTML
    create_file(
        "contact.html",
        """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kontakta Oss - Ådala Frukt och Grönt</title>
    <meta name="description" content="Hitta till Ådala Frukt och Grönt AB eller kontakta oss med dina frågor.">
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <div class="container">
            <a href="/index.html" class="logo">Ådala Frukt & Grönt</a>
            <nav>
                <ul>
                    <li><a href="/index.html">Hem</a></li>
                    <li><a href="/about.html">Om Ådala</a></li>
                    <li><a href="/products.html">Våra Produkter</a></li>
                    <li><a href="/cafe.html">Café</a></li>
                    <li><a href="/contact.html" class="active">Besök Oss</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <article>
                <h1>Besök Oss / Kontakta Oss</h1>
                <p>Vi ser fram emot att höra från dig eller välkomna dig till vår gård!</p>

                <h2>Hitta till Ådala</h2>
                <p>Ådala Frukt och Grönt AB<br>
                Ådalavägen 123<br>
                573 XX Tranås</p>
                <p>Vi ligger naturskönt beläget strax utanför Tranås. Följ skyltarna från väg XX.</p>
                <img src="/assets/img/map-placeholder.png" alt="Platshållare för karta" style="max-width: 100%;">

                <h2>Kontakta oss</h2>
                <p>Har du frågor om våra produkter, caféet eller vill boka ett besök? Tveka inte att höra av dig!</p>
                <ul>
                    <li>**Telefon:** <a href="tel:+46123456789">0123-45 67 89</a></li>
                    <li>**E-post:** <a href="mailto:info@adala.se">info@adala.se</a></li>
                </ul>

                <h2>Följ oss i sociala medier</h2>
                <p>Håll dig uppdaterad med det senaste från Ådala! Följ oss på:</p>
                <ul>
                    <li><a href="https://www.facebook.com/adala" target="_blank">Facebook</a></li>
                    <li><a href="https://www.instagram.com/adala" target="_blank">Instagram</a></li>
                </ul>
            </article>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2025 Ådala Frukt och Grönt AB. Alla rättigheter reserverade.</p>
            <p><a href="/contact.html">Kontakta oss</a></p>
        </div>
    </footer>

    <script src="/assets/js/main.js"></script>
</body>
</html>
"""
    )

    # 11. Products HTML
    create_file(
        "products.html",
        """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Våra Produkter - Ådala Frukt och Grönt</title>
    <meta name="description" content="Utforska det breda utbudet av närproducerade frukter, grönsaker och honung från Ådala Frukt och Grönt.">
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <div class="container">
            <a href="/index.html" class="logo">Ådala Frukt & Grönt</a>
            <nav>
                <ul>
                    <li><a href="/index.html">Hem</a></li>
                    <li><a href="/about.html">Om Ådala</a></li>
                    <li><a href="/products.html" class="active">Våra Produkter</a></li>
                    <li><a href="/cafe.html">Café</a></li>
                    <li><a href="/contact.html">Besök Oss</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <article>
                <h1>Våra Produkter</h1>
                <p>På Ådala Frukt och Grönt är vi stolta över att kunna erbjuda en mångfald av färska, närproducerade produkter direkt från vår gård. Vårt fokus ligger på kvalitet, smak och hållbarhet.</p>

                <div class="grid-container">
                    <div class="grid-item">
                        <img src="/assets/img/biodling-thumb.jpg" alt="Bikupa och bin">
                        <h3>Biodling & Honung</h3>
                        <p>Våra flitiga bin producerar en fantastisk, nyslungad honung med smak av traktens blommor.</p>
                        <a href="/biodling.html" class="cta-button-small">Läs mer</a>
                    </div>
                    <div class="grid-item">
                        <img src="/assets/img/appeltra-thumb.jpg" alt="Äppelträd med äpplen">
                        <h3>Äpplen</h3>
                        <p>Från våra äppelträd skördar vi flera sorters äpplen som passar perfekt för både att äta som de är eller till must och bakning.</p>
                        <a href="/applen.html" class="cta-button-small">Läs mer</a>
                    </div>
                    <div class="grid-item">
                        <img src="/assets/img/hallon-thumb.jpg" alt="Hallonbuskar">
                        <h3>Hallon</h3>
                        <p>Under sommaren kan du njuta av söta, saftiga hallon. Perfekta för självplock!</p>
                        <a href="/hallon.html" class="cta-button-small">Läs mer</a>
                    </div>
                    <div class="grid-item">
                        <img src="/assets/img/blabar-thumb.jpg" alt="Blåbärsbuskar">
                        <h3>Blåbär</h3>
                        <p>Våra blåbärsbuskar ger riklig skörd av hälsobringande blåbär som är underbara att plocka.</p>
                        <a href="/blabar.html" class="cta-button-small">Läs mer</a>
                    </div>
                    <div class="grid-item">
                        <img src="/assets/img/gronsaker-thumb.jpg" alt="Grönsaksland">
                        <h3>Grönsaker</h3>
                        <p>Ett varierat utbud av säsongsgrönsaker, odlade ekologiskt och med kärlek.</p>
                        <a href="/gronsaksodling.html" class="cta-button-small">Läs mer</a>
                    </div>
                </div>
            </article>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2025 Ådala Frukt och Grönt AB. Alla rättigheter reserverade.</p>
            <p><a href="/contact.html">Kontakta oss</a></p>
        </div>
    </footer>

    <script src="/assets/js/main.js"></script>
</body>
</html>
"""
    )

    # 12. 404 HTML
    create_file(
        "404.html",
        """<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sidan kunde inte hittas (404) - Ådala Frukt och Grönt</title>
    <meta name="description" content="Sidan du sökte kunde inte hittas på Ådala Frukt och Grönt AB.">
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
    <style>
        .error-container {
            text-align: center;
            padding: 50px 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 50px auto;
            max-width: 600px;
        }
        .error-container h1 {
            font-size: 4rem;
            color: var(--color-accent-red);
            margin-bottom: 20px;
        }
        .error-container p {
            font-size: 1.2rem;
            margin-bottom: 30px;
        }
        .error-container a {
            display: inline-block;
            background-color: var(--color-primary-green);
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .error-container a:hover {
            background-color: var(--color-secondary-green);
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <a href="/index.html" class="logo">Ådala Frukt & Grönt</a>
            <nav>
                <ul>
                    <li><a href="/index.html">Hem</a></li>
                    <li><a href="/about.html">Om Ådala</a></li>
                    <li><a href="/products.html">Våra Produkter</a></li>
                    <li><a href="/cafe.html">Café</a></li>
                    <li><a href="/contact.html">Besök Oss</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <div class="error-container">
                <h1>404</h1>
                <h2>Sidan kunde inte hittas</h2>
                <p>Tyvärr, sidan du försöker nå finns inte. Kanske har den flyttats eller så är det en felskrivning?</p>
                <a href="/index.html">Gå till startsidan</a>
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>© 2025 Ådala Frukt och Grönt AB. Alla rättigheter reserverade.</p>
            <p><a href="/contact.html">Kontakta oss</a></p>
        </div>
    </footer>

    <script src="/assets/js/main.js"></script>
</body>
</html>
"""
    )

    # 13. README.md
    create_file(
        "README.md",
        """# Ådala Frukt och Grönt AB - Webbplats

Detta repository innehåller webbplatsen för Ådala Frukt och Grönt AB, byggd för att vara enkel att hantera och hosta via GitHub Pages.

## Projektmål

Syftet med denna webbplats är att presentera Ådalas verksamheter – biodling, äppelträd, hallonbuskar, blåbärsbuskar, grönsaksodling och ett enkelt café – på ett trevligt och användarvänligt sätt.

## Teknisk Stack

* **HTML5, CSS3, Ren JavaScript:** För att säkerställa kompatibilitet med GitHub Pages utan krav på lokal kompilering.
* **Markdown:** För att enkelt kunna skapa och hantera artiklar och innehåll.
* **GitHub Pages:** För hosting av den statiska webbplatsen.
* **GitHub Actions:** Används för att automatiskt omvandla Markdown-filer till HTML och deploya webbplatsen vid varje push till `main`-grenen.

## Mappstruktur

