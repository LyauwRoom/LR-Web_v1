# Lyauw Room CMS Preview

**Status:** CMS Preview — not the production website

This repository is the CMS-driven preview environment for the Lyauw Room website.

- Preview website: https://lyauwroom.github.io/LR-Web_v1/
- Production website: https://lyauw.me
- Production repository: [LR-Web](https://github.com/LyauwRoom/LR-Web)
- Working branch: `main`

## How content synchronization works

The `LR CMS Sync` GitHub Actions workflow runs on:

- Manual dispatch
- Pushes to `main`
- A scheduled interval

The workflow runs `sync_data.py`, reads the configured published Google Sheets CSV feeds, and writes generated CMS data to `web_v1/data.json`. It creates a new commit only when the generated data changes.

## Repository structure

- `.github/workflows/sync.yml` — CMS synchronization workflow
- `sync_data.py` — spreadsheet-to-JSON synchronization script
- `web_v1/data.json` — generated CMS data
- `index.html` and page-specific HTML files — preview pages
- `style.css` — shared preview styling
- Image files — preview visual assets

## Change policy

Use this repository for preview and CMS integration work. A push to `main` starts the synchronization workflow, so review workflow and data-source changes carefully. Do not treat preview approval as authorization to publish changes to the production repository.
