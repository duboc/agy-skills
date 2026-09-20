# Google Docs Engineering Spec (`gdoc-engineering-spec`)

Skill for generating Google-grade, multi-tab technical specifications, API integration guides, Design Docs (RFCs), PRDs, and operational runbooks directly in **Google Docs (Pageless mode)**.

## Key Features
- **Multi-Tab Architecture (`create-tab` / `rename-tab`):** Automatically splits complex specs into clean, navigable Google Docs tabs (`Visão Geral & Ambientes`, `Especificação da API`, `Exemplos de Código`, `Checklist & Homologação`).
- **Native Visual Formatting:** Shaded callout banners (`amber`, `blue`, `green`, `red`), dark-header zebra tables (`#1E3A8A`), inline HTTP/status badges (`POST`, `HTTP 200`), and `Roboto Mono` syntax-styled code containers.
- **UTF-16 Emoji-Safe Indexing:** Computes exact UTF-16 code unit offsets (`len(s.encode('utf-16-le')) // 2`) so emojis never shift text styling ranges.
- **Declarative JSON CLI:** Pass any `spec.json` to `scripts/build_gdoc_spec.py` to create and format a complete multi-tab Google Doc in seconds.
