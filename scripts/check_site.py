#!/usr/bin/env python3
"""Contrôles du site statique, sans dépendance tierce ni accès aux données privées."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.references = []
        self.tags = []
        self.meta = {}
        self.canonical = None
        self.lang = None
        self.controls = []
        self.jsonld = []
        self.jsonld_active = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'meta':
            self.meta[attrs.get('name') or attrs.get('property')] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        for key in ('href', 'src'):
            if attrs.get(key):
                self.references.append(attrs[key])
        if attrs.get('aria-controls'):
            self.controls.extend(attrs['aria-controls'].split())
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.jsonld_active = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.jsonld_active = False

    def handle_data(self, data):
        if self.jsonld_active:
            self.jsonld.append(data)


def main():
    errors = []
    html = (SITE / 'index.html').read_text(encoding='utf-8')
    page = PageParser()
    page.feed(html)
    if page.lang != 'fr':
        errors.append('Langue HTML incorrecte')
    if len(page.ids) != len(set(page.ids)):
        errors.append('Identifiants HTML dupliqués')
    if page.tags.count('h1') != 1:
        errors.append('La page doit avoir un seul H1')
    if not page.meta.get('description'):
        errors.append('Description SEO absente')
    if page.canonical != 'https://nogues.app/these/':
        errors.append('URL canonique incorrecte')
    for key in ('og:title', 'og:url', 'og:image', 'twitter:card'):
        if not page.meta.get(key):
            errors.append('Métadonnée absente : ' + key)
    for reference in page.references:
        parts = urlsplit(reference)
        if parts.scheme or parts.netloc:
            continue
        if parts.fragment and not parts.path and parts.fragment not in page.ids:
            errors.append('Ancre inconnue : ' + reference)
        if parts.path:
            local = SITE / unquote(parts.path)
            if not local.is_file():
                errors.append('Fichier local absent : ' + reference)
    for control in page.controls:
        if control not in page.ids:
            errors.append('Cible aria-controls inconnue : ' + control)
    for needed in ('projet', 'hypothese', 'enquete', 'reperes', 'calendrier'):
        if needed not in page.ids:
            errors.append('Section absente : ' + needed)
    for content in ('Sébastien Noguès', 'TBS Education', 'Recherche à venir', 'Hypothèses indicatives', 'Étienne Ollion', 'Yann Ferguson', 'Samuel Fosso Wamba'):
        if content.lower() not in html.lower():
            errors.append('Contenu obligatoire absent : ' + content)
    try:
        json.loads(''.join(page.jsonld))
        routes = json.loads((SITE / 'manus-routes.json').read_text())
        if routes != {'routes': [{'path': '/', 'title': 'L’effet prothèse — Projet de recherche'}]}:
            errors.append('Manifeste de routes incorrect')
    except (ValueError, FileNotFoundError) as error:
        errors.append('JSON invalide : ' + str(error))
    for asset in ('assets/styles.css', 'assets/site.js', 'assets/signe.svg', 'assets/partage.png', 'documents/synthese-projet.md', 'sitemap.xml', '.htaccess'):
        file = SITE / asset
        if not file.is_file() or file.stat().st_size == 0:
            errors.append('Livrable absent ou vide : ' + asset)
    if not (SITE / 'documents/synthese-projet.md').read_text().rstrip().endswith('Code : [nogseb/these](https://github.com/nogseb/these).'):
        errors.append('Synthèse publique incomplète')
    if errors:
        print('\n'.join('ERREUR : ' + error for error in errors))
        return 1
    print(f'Validation réussie : {len(page.ids)} identifiants uniques, {len(page.references)} liens/ressources, contenu et métadonnées présents.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
