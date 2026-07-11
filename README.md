# Fábrica da Picanha — Website

Website oficial da cadeia de churrascarias **Fábrica Rodízio de Picanha** (Grande Lisboa), focado em reservas de clientes de várias nacionalidades.

## Funcionalidades

- **Multilingue** — PT / EN / ES / FR com deteção automática do idioma do browser (persistido em `localStorage`)
- **Reservas** — formulário que gera uma mensagem de WhatsApp pré-preenchida e localizada para o número da casa (+351 960 307 895), com alternativas TheFork e Instagram
- **Vivo enquanto se faz scroll** — espeto de progresso com chama, brasas em canvas no hero, carrossel horizontal de cortes guiado pelo scroll, parallax, marquee, contadores e reveals
- **Identidade** — ardósia de churrascaria, laranja "fábrica" do logótipo, ilustrações dos cortes a traço de giz
- **Acessível e responsivo** — `prefers-reduced-motion` respeitado, foco visível, mobile com scroll-snap nos cortes
- **Sem dependências** — HTML/CSS/JS puro, fontes auto-hospedadas (Anton, Archivo, Caveat)

## Desenvolvimento

```bash
python3 -m http.server 8123
# abrir http://localhost:8123
```

## Estrutura

```
index.html        página única
css/styles.css    identidade e layout
css/fonts.css     @font-face auto-hospedados
js/i18n.js        dicionários PT/EN/ES/FR
js/app.js         i18n, scroll, brasas, reservas
fonts/            woff2 (latin + latin-ext)
```

É um site estático — pode ser publicado diretamente na Vercel, Netlify ou qualquer alojamento estático.
