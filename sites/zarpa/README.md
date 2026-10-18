# zarpa.pt — site da Zarpa

Site da própria Zarpa: apresenta o serviço (sites para clínicas, no ar em cerca de 14 dias, pagamento só na entrega aprovada) e recolhe pedidos de maquete. Estático, sem build, pronto para o Vercel (`public/` é a raiz).

- `public/` — o site: `index.html`, `privacidade.html`, `404.html`, `styles.css`, `app.js`, `assets/`, `fonts/` (Geist, OFL).
- `tools/qa/shots.mjs` — capturas desktop + mobile para `qa/`, testa o pré-preenchimento e a validação do formulário, e gera `public/assets/og.png` a partir de `tools/og/og.html`.

```bash
python3 -m http.server 8622 --directory sites/zarpa/public &
node sites/zarpa/tools/qa/shots.mjs
```

## Conceito

1. **A maquete é a prova.** No primeiro ecrã a clínica escreve o nome, a cidade e a especialidade e vê o próprio site a ganhar forma num telemóvel; o botão leva o pedido já preenchido para o formulário.
2. **Zarpar = partir.** A vela ▲ da marca percorre a rota do dia 0 ao dia 14 à medida que se lê "Como funciona".
3. **Preto sobre branco**, como pede `vendas/email/marca.md`, com o azul das cartas náuticas (água baixa `#dcedf4`, linhas de profundidade `#1f5e7e`) como única cor. Uma só família: Geist.

## De onde vem o conteúdo

| Conteúdo | Fonte |
|---|---|
| Promessa (14 dias, só paga quando aprovar, nada adiantado, 8 dias para pagar, 2 rondas de alterações) | `vendas/email/marca.md`, `vendas/email/plano.md` §2 |
| Processo (maquete + vídeo curto, chamada de 20 min, proposta, pré-visualização) | `plano.md` §2, emails 03 e 07 |
| Pacotes Completo / Profissional / Essencial e o que incluem, do mais caro para o mais barato | `plano.md` §2 ("conteúdo a confirmar") |
| Lista do que é verificado em cada clínica | evidências do `icebreaker-writer` (`plano.md` §3, passo 5) |
| Maquete em 48 h | `plano.md` §3, passo 7 |
| Privacidade: fontes e subcontratantes dos contactos frios | `plano.md` §1 e §3 |

**Preços não aparecem no site**, de propósito: `vendas/conhecimento/psicologia-venda.md` diz que o preço só aparece depois de verem a maquete. O texto diz que o valor vai na proposta e que não se paga nada adiantado. Se quiserem mostrar "a partir de 910", é uma linha em `.pk-note`.

## Por preencher antes de publicar

- `[DENOMINAÇÃO SOCIAL]`, `[NIF]`, `[MORADA]` no rodapé de `index.html` e `privacidade.html`, e a entidade RAL competente em `privacidade.html#litigios`.
- WhatsApp/telefone do Diogo: preencher `CONTACTO.whatsapp` em `app.js` (formato `3519XXXXXXXX`) para aparecer o botão "Enviar por WhatsApp".
- "Feitos no Algarve" no rodapé — confirmar.
- Domínio `zarpa.pt` e registo da marca (INPI/RNPC), como em `marca.md`.

## Notas técnicas

- Sem cookies, sem estatísticas, sem pedidos a terceiros; CSP restritiva em `vercel.json` (nada inline).
- O formulário não tem servidor: valida e abre um `mailto:` (ou `wa.me`) com a mensagem escrita. Para receber pedidos sem depender do email do visitante, ligar a um endpoint (ex.: função do Vercel) e acrescentá-lo a `connect-src`/`form-action` na CSP.
- `prefers-reduced-motion`: a rota aparece completa e sem animação.
