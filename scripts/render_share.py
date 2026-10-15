#!/usr/bin/env python3
"""Génère l’image sociale. Outil de maintenance facultatif : pip install playwright."""
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
with sync_playwright() as playwright:
    browser = None
    for options in ({}, {'executable_path': '/usr/bin/chromium'}, {'channel': 'chrome'}):
        try:
            browser = playwright.chromium.launch(**options)
            break
        except Exception:
            pass
    if browser is None:
        raise RuntimeError('Chromium indisponible pour générer l’image de partage')
    page = browser.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
    page.goto((root / 'scripts/partage.html').as_uri())
    page.locator('main').screenshot(path=str(root / 'site/assets/partage.png'))
    print(root / 'site/assets/partage.png')
    browser.close()
