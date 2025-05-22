#!/bin/bash

# Script för att skapa webbplatsen Ådala.se med Jekyll och GitHub Pages
# Körs i en tom katalog där webbplatsen ska initieras.

GITHUB_USERNAME="gunnarnordqvist"
REPO_NAME="adalase-website" # Du kan ändra detta om du vill ha ett annat repo-namn

echo "Startar skript för att sätta upp Ådala.se..."
echo "Ditt GitHub-användarnamn: ${GITHUB_USERNAME}"
echo "Namn på GitHub-repositoriet: ${REPO_NAME}"
echo ""

# --- Steg 1: Skapa katalogstruktur ---
echo "1. Skapar katalogstruktur..."
mkdir -p .github/workflows
mkdir -p _layouts
mkdir -p _includes
mkdir -p assets/css

echo "Katalogstruktur skapad."

# --- Steg 2: Skapa Jekyll-konfigurationsfil (_config.yml) ---
echo "2. Skapar _config.yml..."
cat << EOF > _config.yml
title: Ådala Frukt och Grönt AB
description: Officiell webbplats för Ådala Frukt och Grönt AB – Lokala produkter direkt från gården.
url: "https://${GITHUB_USERNAME}.github.io/${REPO_NAME}"
baseurl: "/${REPO_NAME}"
remote_theme: jekyll/minima # Ett enkelt tema för att starta med
plugins:
  - jekyll-feed
EOF
echo "_config.yml skapad."

# --- Steg 3: Skapa Jekyll-layouter och includes ---
echo "3. Skapar Jekyll-layouter och includes..."

cat << 'EOF' > _layouts/default.html
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page.title }} - Ådala Frukt och Grönt</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background-color: #f4f4f4; color: #333; }
        header { background: #5cb85c; color: #fff; padding: 1em 0; text-align: center; }
        nav a { color: #fff; margin: 0 15px; text-decoration: none; }
        main { padding: 20px; max-width: 960px; margin: 20px auto; background: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        footer { text-align: center; padding: 20px; background: #333; color: #fff; position: relative; bottom: 0; width: 100%; }
        h1, h2, h3 { color: #333; }
        ul { list-style: none; padding: 0; }
        ul li { margin-bottom: 10px; }
        ul li a { color: #007bff; text-decoration: none; }
        ul li a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    {% include header.html %}

    <main>
        {{ content }}
    </main>

    {% include footer.html %}
</body>
</html>
EOF

cat << 'EOF' > _includes/header.html
<header>
    <nav>
        <a href="/">Hem</a>
        <a href="/biodling">Biodling</a>
        <a href="/gronsaksodling">Grönsaker</a>
        <a href="/barodling">Bär</a>
        <a href="/fruktodling">Frukt</a>
        <a href="/om-oss">Om oss</a>
        <a href="/kontakt">Kontakt</a>
    </nav>
</header>
EOF

cat << 'EOF' > _includes/footer.html
<footer>
    <p>&copy; {{ site.time | date: "%Y" }} Ådala Frukt och Grönt AB. Alla rättigheter reserverade.</p>
</footer>
EOF

echo "Jekyll-layouter och includes skapade."

# --- Steg 4: Skapa grundläggande CSS-fil ---
echo "4. Skapar assets/css/style.css..."
cat << EOF > assets/css/style.css
/* Grundläggande stil för Ådala.se */
/* Detta är en minimal CSS, mer kan läggas till */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background-color: #f8f8f8;
    color: #333;
}

header {
    background: #4CAF50; /* Grön färg */
    color: white;
    padding: 1em 0;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

header nav {
    display: flex;
    justify-content: center;
    gap: 20px;
}

header nav a {
    color: white;
    text-decoration: none;
    font-weight: bold;
    padding: 5px 10px;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

header nav a:hover {
    background-color: rgba(255,255,255,0.2);
}

main {
    max-width: 960px;
    margin: 20px auto;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 0 15px rgba(0,0,0,0.05);
}

h1, h2, h3 {
    color: #333;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

p {
    margin-bottom: 1em;
}

ul {
    list-style: disc;
    margin-left: 20px;
    margin-bottom: 1em;
}

ul li {
    margin-bottom: 0.5em;
}

a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    background: #333;
    color: white;
    font-size: 0.9em;
}
EOF
echo "assets/css/style.css skapad."


# --- Steg 5: Skapa innehållsfiler i Markdown ---
echo "5. Skapar innehållsfiler i Markdown..."

cat << EOF > index.md
---
layout: default
title: Välkommen till Ådala Frukt och Grönt AB
---

# Välkommen till Ådala Frukt och Grönt AB

Välkommen till Ådala Frukt och Grönt AB – din lokala leverantör av högkvalitativa produkter direkt från gården! Vi är stolta över vår biodling, grönsaksodling, bärodling och fruktodling, där vi med omsorg och hållbarhet i fokus producerar det bästa naturen har att erbjuda.

Vårt mål är att erbjuda färska, närodlade produkter som smakar gott och är bra för dig och vår miljö. Vi tror på att arbeta i harmoni med naturen och strävar efter att minimera vår påverkan på ekosystemet.

Utforska våra verksamheter:

* **[Biodling](/biodling)**: Lär dig mer om våra flitiga bin och den fantastiska honung de producerar. Våra bin bidrar också till pollineringen av våra odlingar.
* **[Grönsaksodling](/gronsaksodling)**: Se vilka färska, säsongsanpassade grönsaker som är i säsong. Vi odlar en mängd olika sorter, anpassade för det nordiska klimatet.
* **[Bärodling](/barodling)**: Upptäck våra söta bär – perfekt för sylt, paj eller att äta som de är. Vi har jordgubbar, hallon och blåbär under sommarmånaderna.
* **[Fruktodling](/fruktodling)**: Smaka på våra saftiga frukter, odlade med kärlek. Från äpplen till päron, direkt från våra fruktträdgårdar.

Vi ser fram emot att dela vår skörd med dig! Följ oss gärna på sociala medier för de senaste uppdateringarna om skörd och evenemang.
EOF

cat << EOF > biodling.md
---
layout: default
title: Biodling hos Ådala Frukt och Grönt AB
---

# Biodling hos Ådala Frukt och Grönt AB

På Ådala Frukt och Grönt AB är biodlingen en central del av vår verksamhet. Våra bin är inte bara producenter av underbar honung, de är också ovärderliga pollinerare för våra grönsaks-, bär- och fruktodlingar. Utan våra flitiga vänner skulle skördarna vara betydligt mindre!

## Vår honung
Vi producerar nyslungad, lokal honung av högsta kvalitet. Smaken och karaktären på honungen varierar beroende på vilka blommor bina har besökt under säsongen. Från ljus och mild försommarhonung till mörkare och fylligare sensommarhonung – varje burk är unik.

* **Säsongsprodukt:** Honung finns tillgänglig under sensommaren och hösten.
* **Användningsområden:** Perfekt i teet, på gröten, i bakning eller som en energiboost direkt från skeden.

## Binas roll för miljön
Vi lägger stor vikt vid att skapa en gynnsam miljö för våra bin. Det innebär att vi arbetar med biologisk mångfald på våra marker och undviker bekämpningsmedel som är skadliga för pollinerare. Binas hälsa är viktig för hela ekosystemet.

Kom gärna förbi vår gårdsbutik för att smaka på vår honung!
EOF

cat << EOF > gronsaksodling.md
---
layout: default
title: Grönsaksodling hos Ådala Frukt och Grönt AB
---

# Grönsaksodling hos Ådala Frukt och Grönt AB

Vår grönsaksodling är hjärtat i Ådala Frukt och Grönt AB. Här odlar vi ett brett utbud av färska, näringsrika grönsaker med fokus på säsong och hållbarhet. Vi arbetar med metoder som berikar jorden och minimerar behovet av yttre insatser.

## Vad vi odlar
Vi strävar efter att erbjuda variation och kvalitet. Bland våra odlade grönsaker hittar du ofta:

* **Sallad:** Flera sorter, krispiga och färska.
* **Rotfrukter:** Morötter, potatis, rödbetor och palsternackor.
* **Kål:** Broccolli, vitkål, grönkål och blomkål.
* **Örter:** Persilja, dill, gräslök och mynta.
* **Mer:** Bönor, ärtor, squash, pumpa (beroende på säsong och år).

## Säsong och tillgänglighet
Våra grönsaker skördas när de är som bäst, vilket betyder att utbudet varierar med säsongen. Håll utkik i vår gårdsbutik eller på vår Facebook-sida för att se vad som finns tillgängligt just nu.

Vi är engagerade i att odla hållbart och erbjuda dig de godaste grönsakerna från vårt närområde.
EOF

cat << EOF > barodling.md
---
layout: default
title: Bärodling hos Ådala Frukt och Grönt AB
---

# Bärodling hos Ådala Frukt och Grönt AB

När sommaren kommer fylls våra fält med söta och saftiga bär! På Ådala Frukt och Grönt AB odlar vi med stor omsorg för att ge dig bär av högsta kvalitet. Bärodlingen är en av våra mest populära verksamheter.

## Våra bär
Vi odlar framför allt:

* **Jordgubbar:** De klassiska sommarbären, perfekta till frukost, dessert eller bara som de är.
* **Hallon:** Söta och aromatiska, utmärkta för sylt, saft eller att frysa in.
* **Blåbär:** Fulla av antioxidanter, både odlade och ibland vilda från närområdet.

## Självplock
Under säsongen erbjuder vi även **självplock** av våra bär! Det är ett fantastiskt sätt att tillbringa en dag utomhus med familj och vänner, och samtidigt fylla frysen med sommarens smaker.

* **Jordgubbar:** Oftast tillgängliga för självplock från mitten av juni till mitten av juli.
* **Hallon:** Självplock brukar vara möjligt från mitten av juli till augusti.

**OBS!** Håll koll på vår hemsida eller sociala medier för aktuella självplockstider och väderförhållanden. Vi meddelar alltid när det är dags!

Välkommen att plocka dina egna bär hos oss!
EOF

cat << EOF > fruktodling.md
---
layout: default
title: Fruktodling hos Ådala Frukt och Grönt AB
---

# Fruktodling hos Ådala Frukt och Grönt AB

I våra fruktträdgårdar på Ådala Frukt och Grönt AB växer saftiga frukter som mognar under sensommaren och hösten. Vi odlar klassiska frukter som är anpassade till vårt klimat och som ger en rik skörd år efter år.

## Vilka frukter odlar vi?
Vår fruktodling fokuserar främst på:

* **Äpplen:** Flera populära sorter som 'Cox Orange', 'Gravensteiner', 'Ingrid Marie' och 'Discovery'. Perfekta att äta direkt, baka med eller pressa till must.
* **Päron:** Söta och saftiga päron som 'Conference' och 'Herzogin Elsa'.

## Från träd till bord
Vi skördar våra frukter för hand när de är som bäst, vilket garanterar högsta kvalitet och smak. En del av skörden säljs färsk i vår gårdsbutik, medan en annan del förädlas till läcker äppelmust.

## Äppelmust
Vår egenpressade äppelmust är en populär produkt, gjord på 100% frukt från våra egna träd. Den är helt utan tillsatser och smakar fantastiskt. Perfekt som törstsläckare eller till maten.

Välkommen att uppleva smaken av färsk frukt från Ådala!
EOF

cat << EOF > om-oss.md
---
layout: default
title: Om Ådala Frukt och Grönt AB
---

# Om Ådala Frukt och Grönt AB

Ådala Frukt och Grönt AB är ett familjeägt företag med rötter djupt i den svenska myllan. Sedan starten har vår passion varit att odla och förädla naturens råvaror med största respekt för miljö och tradition.

## Vår historia
Företaget grundades 20XX av [Grundarens namn/familjenamn] med en vision om att erbjuda närodlade, högkvalitativa produkter direkt till konsumenten. Genom åren har vi utökat vår verksamhet från en liten grönsaksodling till att omfatta biodling, bärodling och fruktodling.

## Vår filosofi
Vi tror på hållbarhet, transparens och kvalitet. Varje dag arbetar vi för att:
* Odla med metoder som värnar om jorden och dess biologiska mångfald.
* Leverera produkter som är färska, smakrika och näringsrika.
* Bygga en nära relation med våra kunder och lokalsamhället.
* Minimera vår miljöpåverkan genom hela produktionskedjan.

## Vårt team
Vi är ett litet, engagerat team som brinner för det vi gör. Från den tidiga våren till den sena hösten arbetar vi hårt för att naturen ska ge oss den bästa skörden.

Tack för att du väljer Ådala Frukt och Grönt AB!
EOF

cat << EOF > kontakt.md
---
layout: default
title: Kontakta Ådala Frukt och Grönt AB
---

# Kontakta Ådala Frukt och Grönt AB

Har du frågor om våra produkter, självplock eller vill du bara säga hej? Tveka inte att kontakta oss!

## Våra kontaktuppgifter

* **Telefon:** 070-123 45 67 (Vardagar kl. 09:00-16:00)
* **E-post:** info@adala.se
* **Gårdsbutikens adress:**
    Ådala Gårdsväg 1
    123 45 Ådala
    Sverige

## Gårdsbutikens öppettider

* **Maj - Augusti:** Tisdag-Fredag 10:00-18:00, Lördag 10:00-15:00
* **September - Oktober:** Torsdag-Fredag 12:00-17:00, Lördag 10:00-14:00
* **November - April:** Stängt (endast onlineförsäljning av vissa produkter och efter överenskommelse)

## Hitta till oss
Vi finns strax utanför Ådala. Se kartan nedan för exakt position:

[Länk till Google Maps eller liknande karta (lägg till här)]

Vi ser fram emot att höra från dig eller välkomna dig till vår gårdsbutik!
EOF

echo "Innehållsfiler skapade."

# --- Steg 6: Skapa GitHub Action Workflow-fil ---
echo "6. Skapar .github/workflows/publish.yml..."
cat << 'EOF' > .github/workflows/publish.yml
name: Deploy Jekyll site to GitHub Pages

on:
  push:
    branches:
      - main # Trigga workflow när kod pushas till main-grenen

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest # Kör jobbet på en Ubuntu-miljö

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4 # Steg 1: Hämta källkoden från repositoriet

    - name: Setup Ruby
      uses: ruby/setup-ruby@v1
      with:
        ruby-version: '3.x' # Använd en kompatibel Ruby-version för Jekyll
        bundler-cache: true # Installera och cachea Gemfile.lock

    - name: Install Jekyll and dependencies
      run: bundle install # Steg 3: Installera Jekyll och dess beroenden

    - name: Build Jekyll site
      run: bundle exec jekyll build # Steg 4: Bygg den statiska Jekyll-webbplatsen

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3 # Steg 5: Använd en populär action för att deploya till GitHub Pages
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }} # Använder GitHubs inbyggda token
        publish_dir: ./_site # Mappen som Jekyll bygger webbplatsen i
EOF
echo ".github/workflows/publish.yml skapad."

# --- Steg 7: Skapa en Gemfile för Jekyll-beroenden ---
echo "7. Skapar Gemfile..."
cat << EOF > Gemfile
source "https://rubygems.org"

gem "jekyll"
gem "jekyll-feed"
gem "minima" # Om du använder minima-temat
# Lägg till andra gems här om du behöver
EOF
echo "Gemfile skapad."

# --- Steg 8: Instruktioner för Git och GitHub ---
echo ""
echo "--------------------------------------------------------"
echo "                   KLART ATT DEPLOYAS!                  "
echo "--------------------------------------------------------"
echo ""
echo "Projektet för Ådala.se är nu skapat lokalt i katalogen:"
echo "-> $(pwd)"
echo ""
echo "Följ dessa steg för att publicera din webbplats på GitHub Pages:"
echo ""
echo "1.  **Initiera Git i denna katalog:**"
echo "    cd $(pwd)"
echo "    git init"
echo "    git add ."
echo "    git commit -m \"Initial commit for Adala.se website\""
echo ""
echo "2.  **Skapa ett nytt TOMT repositorium på GitHub:**"
echo "    Gå till **github.com** och logga in."
echo "    Klicka på '+' (uppe till höger) och välj 'New repository'."
echo "    Ge repositoriet namnet: **${REPO_NAME}**"
echo "    Se till att det är **tomt** (bocka INTE i 'Add a README file', '.gitignore', eller 'Choose a license')."
echo ""
echo "3.  **Koppla ditt lokala repo till GitHub och pusha:**"
echo "    git branch -M main"
echo "    git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
echo "    git push -u origin main"
echo ""
echo "4.  **Konfigurera GitHub Pages (efter att du har pushat):**"
echo "    Gå till ditt nya repositorium på GitHub."
echo "    Klicka på fliken **'Settings'** (Inställningar)."
echo "    I vänstermenyn, klicka på **'Pages'**."
echo "    Under 'Build and deployment', se till att 'Source' är satt till **'Deploy from a branch'**."
echo "    Under 'Branch', välj **'gh-pages'** och **'/(root)'**. Klicka sedan på 'Save'."
echo "    *(Obs: 'gh-pages'-grenen skapas automatiskt av GitHub Action vid första körningen, så den kanske inte syns direkt.)*"
echo ""
echo "5.  **Verifiera GitHub Actions:**"
echo "    Gå till fliken **'Actions'** i ditt repo på GitHub."
echo "    En workflow med namnet 'Deploy Jekyll site to GitHub Pages' ska ha startat automatiskt."
echo "    När den är klar (visas med en grön bock), kommer din webbplats att vara tillgänglig på:"
echo "    **https://${GITHUB_USERNAME}.github.io/${REPO_NAME}**"
echo ""
echo "Lycka till med Ådala.se, Gunnar!"
echo "--------------------------------------------------------"
