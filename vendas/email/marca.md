# Zarpa: marca, tom e campos dos emails

## Nome
**zarpa** (escrito em minúsculas, como a Vercel). Vem de *zarpar*: levantar âncora, partir. Promessa: **o site da sua clínica no ar em 14 dias, e só paga quando estiver aprovado.**

- **Logótipo:** um triângulo ▲ como vela, preto sobre branco, e o nome em sans geométrica (Geist, Inter Display). Sem gradientes nem ícones de "web".
- **Domínio:** só `zarpa.pt`. O cold email sai de 10 caixas próprias (`clinicas@`, `sites@`, `estudio@`, `digital@`, `parcerias@`, `contacto@`, `novosprojetos@`, `atendimento@`, `consultoria@`, `crescer@`); `ola@`, `equipa@`, `projetos@` e `faturacao@` ficam para clientes.
- **Por confirmar antes de usar:** registo no INPI (marca, classes 35 e 42) e certificado de admissibilidade no RNPC.

## Tom
- Português de Portugal, frases curtas, **sem jargão** ("SEO", "responsivo", "landing page"). Fala-se de pacientes, marcações e Google.
- Calmo e direto, como um profissional a escrever a outro. Nunca entusiasmo de vendedor nem pontos de exclamação.
- Um facto concreto vale mais do que três elogios.
- Tratamento: "a {{clinica}}" e "o senhor / a senhora" implícitos (3.ª pessoa). Nunca "tu".

## Remetente e assinatura
Os emails são de uma **equipa**, nunca de uma pessoa: o nome de remetente é "Equipa Zarpa", todos os endereços terminam em `@zarpa.pt` e o texto usa a 1.ª pessoa do plural ("fizemos", "preparamos").

```
Equipa Zarpa
sites para clínicas · zarpa.pt
{{telefone_zarpa}}
```

## Rodapé legal (obrigatório em todos os emails frios)
```
—
Encontrámos o contacto da {{clinica}} em {{fonte_contacto}}.
Zarpa · [DENOMINAÇÃO SOCIAL] · NIF [NIF] · [MORADA]
Para não receber mais emails, responda SAIR.
```
`[…]` = dados legais da empresa, por preencher. **Sem eles não se envia.**

## Campos (colunas do `envio.csv`)
| Campo | Exemplo | Regra |
|---|---|---|
| `saudacao` | "Bom dia, Marta" / "Bom dia" | Com o primeiro nome só se o decisor estiver confirmado. Senão, "Bom dia". "Dr./Dra." só se a clínica usar esse título publicamente para essa pessoa, **nunca deduzido do nome** |
| `clinica` | "Clínica Sorriso Algarve" | Nome comercial, sem "Lda" |
| `cidade` | "Loulé" | |
| `especialidade` | "dentista" | O termo que as pessoas pesquisam no Google, não o técnico |
| `icebreaker` | "Vi que a Clínica X tem 4,8 em 212 avaliações no Google, mas o botão 'website' leva ao Facebook." | ≤ 25 palavras, facto verificável, com `icebreaker_fonte` |
| `concorrente` | "Clínica Y" | Só se for verificado (aparece acima na pesquisa e tem marcação online). Senão, a variante sem concorrente |
| `fonte_contacto` | "na vossa ficha do Google" | De onde veio o email |
| `link_maquete` | — | Só nos emails 13 e seguintes |
| `variante` | A / B | Atribuída aleatoriamente |
