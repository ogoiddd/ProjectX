# Fábrica da Picanha — Website

Website oficial da cadeia de churrascarias **Fábrica Rodízio de Picanha** (Grande Lisboa), focado em reservas de clientes de várias nacionalidades. Design editorial "steakhouse noir" inspirado em referência premium, com a fotografia real dos restaurantes.

## Funcionalidades

- **Multilingue** — PT / EN / ES / FR com deteção automática do idioma do browser, dropdown de idioma na navegação (persistido em `localStorage`)
- **Reservas** — formulário que gera uma mensagem de WhatsApp pré-preenchida e localizada para o número da casa (+351 960 307 895), com alternativas TheFork e Instagram
- **Transições e scroll vivo** — entrada do hero em cascata, Ken Burns na fotografia, reveals no scroll, parallax na secção do bar, carrossel horizontal de cortes guiado pelo scroll, scrollspy com sublinhado cobre, hovers suaves em toda a interface
- **Identidade** — quase-preto quente, acento cobre, títulos Playfair Display, corpo Karla, fotografias reais da Fábrica (tábuas, bar, eventos) fundidas no fundo escuro
- **Acessível e responsivo** — `prefers-reduced-motion` respeitado, foco visível, dropdown navegável por teclado, mobile com scroll-snap nos cortes
- **Sem dependências** — HTML/CSS/JS puro, fontes e imagens auto-hospedadas (WebP otimizado)

## Desenvolvimento

```bash
python3 -m http.server 8123
# abrir http://localhost:8123
```

## Estrutura

```
index.html        página única
css/styles.css    identidade e layout
css/fonts.css     @font-face auto-hospedados (Playfair Display, Karla)
js/i18n.js        dicionários PT/EN/ES/FR
js/app.js         i18n, dropdown, scroll, reservas
fonts/            woff2 (latin + latin-ext)
img/              fotografias e logos oficiais (WebP + originais)
.claude/skills/   skill ui-ux-pro-max usada no design
```

É um site estático — pode ser publicado diretamente na Vercel, Netlify ou qualquer alojamento estático.
