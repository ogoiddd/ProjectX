# -*- coding: utf-8 -*-
"""Privacy policy and legal information: /privacidade/ (PT) and /en/privacy/ (EN). FR and DE link to the EN page.
[[...]] = placeholder to confirm with the client (rendered as the yellow badge). Not legal advice: the client
should have this text validated before publishing (see LEGAL.md)."""

PRIV_PATH = {"pt": "/privacidade/", "en": "/en/privacy/", "fr": "/en/privacy/", "de": "/en/privacy/"}

TEL_LINK = '<a href="tel:+351289827145">+351 289 827 145</a>'
CIMAAL = ('<dl>'
          '<dt>{ral_body}</dt><dd>CIMAAL – Centro de Informação, Mediação e Arbitragem de Conflitos de Consumo do Algarve</dd>'
          '<dt>{addr}</dt><dd>Av. 5 de Outubro, 55, r/c, 8000-075 Faro</dd>'
          '<dt>{phone}</dt><dd><a href="tel:+351289823135">+351 289 823 135</a></dd>'
          '<dt>{site}</dt><dd><a href="https://www.consumoalgarve.pt/" rel="noopener">www.consumoalgarve.pt</a></dd>'
          '</dl>')

L = {}

L["pt"] = dict(
    title="Privacidade e informação legal · Restaurante Cidade Velha, Faro",
    desc="Como o Restaurante Cidade Velha (R. Domingos Guieiro 19, Faro) trata dados pessoais, cookies, Livro de Reclamações e resolução alternativa de litígios.",
    h1="Privacidade e informação legal",
    updated="Última atualização: 9 de outubro de 2026",
    back="Voltar ao início",
    body=f"""
<h2 id="responsavel">1. Quem somos</h2>
<dl>
<dt>Responsável pelo tratamento</dt><dd>[[CONFIRMAR COM CLIENTE: denominação social]], que explora o Restaurante Cidade Velha</dd>
<dt>NIF / NIPC</dt><dd>[[CONFIRMAR COM CLIENTE]]</dd>
<dt>Morada</dt><dd>Rua Domingos Guieiro, 19, 8000-311 Faro, Portugal</dd>
<dt>Contactos</dt><dd>{TEL_LINK} (chamada para a rede fixa nacional) · email [[CONFIRMAR COM CLIENTE]]</dd>
</dl>

<h2 id="dados">2. Que dados tratamos e porquê</h2>
<p>Esta política segue o Regulamento (UE) 2016/679 (RGPD) e a Lei n.º 58/2019.</p>
<ul>
<li><b>Pedidos de reserva.</b> O formulário de reserva não envia nada para nós nem para nenhum servidor: apenas escreve, no seu próprio aparelho, uma mensagem que é o visitante a enviar pelo WhatsApp ou por email. Recebemos o que escrever (nome, dia, hora, número de pessoas, preferência de lugar, telefone se o indicar, notas e a língua em que fala) e o número de WhatsApp ou endereço de email de onde envia. Usamos estes dados só para responder ao pedido e gerir a reserva. Fundamento: diligências pré-contratuais a seu pedido (artigo 6.º, n.º 1, alínea b), do RGPD).</li>
<li><b>Alergias e intolerâncias.</b> Se as indicar nas notas, tratamos essa informação de saúde apenas para preparar a sua refeição em segurança, com base no seu consentimento explícito ao no-la comunicar (artigo 9.º, n.º 2, alínea a), do RGPD). Pode retirá-lo a qualquer momento; nesse caso, diga-nos à mesa.</li>
<li><b>Chamadas e mensagens.</b> Se nos ligar ou escrever, usamos o seu contacto apenas para responder.</li>
<li><b>Registos técnicos do alojamento.</b> O fornecedor de alojamento do site (Vercel Inc.) regista dados técnicos de cada pedido, como o endereço IP, a data e hora e o tipo de navegador, para entregar as páginas e proteger o serviço contra abusos. Fundamento: interesse legítimo em manter o site seguro (artigo 6.º, n.º 1, alínea f), do RGPD). [[CONFIRMAR COM CLIENTE: alojamento]]</li>
</ul>
<p>Não tomamos decisões automatizadas nem fazemos perfis.</p>

<h2 id="prazos">3. Durante quanto tempo</h2>
<p>Apagamos as mensagens de reserva e a informação sobre alergias até 30 dias depois da data da reserva, salvo se a lei nos obrigar a guardá-las mais tempo. [[CONFIRMAR COM CLIENTE: prazo]] Os registos técnicos do alojamento são guardados pelo fornecedor por um período curto, segundo a política dele.</p>

<h2 id="partilha">4. Com quem partilhamos</h2>
<p>Não vendemos nem cedemos dados pessoais. Ao enviar a reserva pelo WhatsApp, a mensagem passa pelo serviço do WhatsApp (WhatsApp Ireland Ltd., grupo Meta), segundo as condições que aceitou com esse serviço; por email, passa pelo seu fornecedor de email e pelo nosso [[CONFIRMAR COM CLIENTE: fornecedor de email]]. O fornecedor de alojamento (Vercel Inc., EUA) atua como subcontratante; as transferências para fora do Espaço Económico Europeu fazem-se com as garantias do RGPD (Quadro de Privacidade de Dados UE-EUA e/ou cláusulas contratuais-tipo).</p>

<h2 id="cookies">5. Cookies e serviços de terceiros</h2>
<p>Este site não usa cookies, não guarda nada no seu navegador e não tem ferramentas de estatística, publicidade ou redes sociais. Os tipos de letra e as imagens são servidos pelo próprio site, e o mapa é um desenho estático feito a partir de dados do OpenStreetMap: não há Google Maps, vídeos nem outros conteúdos de terceiros embebidos. Por isso não lhe pedimos consentimento para cookies.</p>
<p>As ligações para o Google Maps, Apple Maps, WhatsApp, Instagram, Facebook, Livro de Reclamações Eletrónico e outros sites só abrem quando carrega nelas, e essas páginas têm as suas próprias políticas de privacidade e de cookies.</p>

<h2 id="direitos">6. Os seus direitos</h2>
<p>Pode pedir acesso, retificação, apagamento, limitação ou portabilidade dos seus dados, opor-se ao tratamento baseado em interesse legítimo e retirar o consentimento a qualquer momento, pelos contactos do ponto 1. Respondemos no prazo de um mês. Tem também o direito de apresentar reclamação à Comissão Nacional de Proteção de Dados (CNPD), <a href="https://www.cnpd.pt/" rel="noopener">www.cnpd.pt</a>.</p>

<h2 id="reclamacoes">7. Livro de Reclamações e resolução de litígios</h2>
<p>Pode apresentar reclamação no <a href="https://www.livroreclamacoes.pt/Inicio/" rel="noopener">Livro de Reclamações Eletrónico</a> ou pedir o livro físico no restaurante.</p>
<p>Em caso de litígio de consumo, pode recorrer a uma entidade de resolução alternativa de litígios (Lei n.º 144/2015). Para Faro, a entidade competente é:</p>
{CIMAAL.format(ral_body="Entidade RAL", addr="Morada", phone="Telefone", site="Site")}
<p>Mais informação no Portal do Consumidor, <a href="https://www.consumidor.gov.pt/" rel="noopener">www.consumidor.gov.pt</a>. [[CONFIRMAR COM CLIENTE: adesão a outra entidade RAL]]</p>

<h2 id="conteudos">8. Sobre os conteúdos deste site</h2>
<ul>
<li>Horário, pratos e disponibilidade podem mudar. Os preços praticados são os da carta do restaurante, com IVA incluído. A informação sobre os 14 alergénios de cada prato está disponível por escrito no restaurante.</li>
<li>As opiniões de clientes são excertos curtos de avaliações públicas no Google e no TheFork (lidas no Trip.com), sem o nome dos autores. A citação da revista NiT é identificada com autor e data.</li>
<li>Os desenhos são originais deste site. Mapa: dados © colaboradores do <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap</a> (ODbL). Tipos de letra Bodoni Moda, Marcellus SC e Jost, licença SIL Open Font License.</li>
</ul>
""",
)

L["en"] = dict(
    title="Privacy and legal information · Restaurante Cidade Velha, Faro",
    desc="How Restaurante Cidade Velha (R. Domingos Guieiro 19, Faro) handles personal data, cookies, the complaints book and alternative dispute resolution.",
    h1="Privacy and legal information",
    updated="Last updated: 9 October 2026",
    back="Back to the home page",
    body=f"""
<h2 id="controller">1. Who we are</h2>
<dl>
<dt>Data controller</dt><dd>[[CONFIRM WITH CLIENT: company name]], operator of Restaurante Cidade Velha</dd>
<dt>Tax number (NIF / NIPC)</dt><dd>[[CONFIRM WITH CLIENT]]</dd>
<dt>Address</dt><dd>Rua Domingos Guieiro, 19, 8000-311 Faro, Portugal</dd>
<dt>Contact</dt><dd>{TEL_LINK} (call to a Portuguese landline) · email [[CONFIRM WITH CLIENT]]</dd>
</dl>

<h2 id="data">2. What data we process and why</h2>
<p>This policy follows Regulation (EU) 2016/679 (GDPR) and Portuguese Law 58/2019.</p>
<ul>
<li><b>Booking requests.</b> The booking form does not send anything to us or to any server: it only writes, on your own device, a message that you then send by WhatsApp or email. We receive what you type (name, date, time, number of guests, seating preference, phone number if you give one, notes and the language you speak) and the WhatsApp number or email address you send it from. We use this only to reply to your request and manage your booking. Legal basis: steps taken at your request before entering into a contract (Article 6(1)(b) GDPR).</li>
<li><b>Allergies and intolerances.</b> If you mention them in the notes, we use that health information only to prepare your meal safely, based on your explicit consent when you share it (Article 9(2)(a) GDPR). You can withdraw it at any time; just tell us at the table.</li>
<li><b>Calls and messages.</b> If you call or write to us, we use your contact details only to reply.</li>
<li><b>Hosting logs.</b> The site's hosting provider (Vercel Inc.) logs technical data for each request, such as IP address, date and time and browser type, to deliver the pages and protect the service against abuse. Legal basis: legitimate interest in keeping the site secure (Article 6(1)(f) GDPR). [[CONFIRM WITH CLIENT: hosting]]</li>
</ul>
<p>We make no automated decisions and do no profiling.</p>

<h2 id="retention">3. How long we keep it</h2>
<p>We delete booking messages and allergy information within 30 days of the booking date, unless the law requires us to keep them longer. [[CONFIRM WITH CLIENT: retention period]] Hosting logs are kept by the provider for a short period, under its own policy.</p>

<h2 id="sharing">4. Who we share it with</h2>
<p>We do not sell or hand over personal data. If you send your booking by WhatsApp, the message goes through WhatsApp's service (WhatsApp Ireland Ltd., Meta group) under the terms you accepted with them; by email, it goes through your email provider and ours [[CONFIRM WITH CLIENT: email provider]]. The hosting provider (Vercel Inc., USA) acts as our processor; transfers outside the European Economic Area rely on GDPR safeguards (EU-US Data Privacy Framework and/or standard contractual clauses).</p>

<h2 id="cookies">5. Cookies and third-party services</h2>
<p>This site uses no cookies, stores nothing in your browser, and has no analytics, advertising or social media tools. Fonts and images are served by the site itself, and the map is a static drawing made from OpenStreetMap data: no Google Maps, videos or other third-party content is embedded. That is why we do not ask for cookie consent.</p>
<p>Links to Google Maps, Apple Maps, WhatsApp, Instagram, Facebook, the Electronic Complaints Book and other sites only open when you click them, and those pages have their own privacy and cookie policies.</p>

<h2 id="rights">6. Your rights</h2>
<p>You can ask to access, correct, erase, restrict or port your data, object to processing based on legitimate interest and withdraw consent at any time, using the contact details in section 1. We reply within one month. You also have the right to complain to the Portuguese data protection authority (CNPD), <a href="https://www.cnpd.pt/" rel="noopener">www.cnpd.pt</a>, or to the authority of the EU country where you live.</p>

<h2 id="complaints">7. Complaints book and dispute resolution</h2>
<p>You can file a complaint in the <a href="https://www.livroreclamacoes.pt/Inicio/" rel="noopener">Electronic Complaints Book (Livro de Reclamações)</a> or ask for the paper book in the restaurant.</p>
<p>In a consumer dispute, you can turn to an alternative dispute resolution body (Portuguese Law 144/2015). For Faro, the competent body is:</p>
{CIMAAL.format(ral_body="ADR body", addr="Address", phone="Phone", site="Website")}
<p>More information on the Portuguese Consumer Portal, <a href="https://www.consumidor.gov.pt/" rel="noopener">www.consumidor.gov.pt</a>. [[CONFIRM WITH CLIENT: membership of another ADR body]]</p>

<h2 id="content">8. About this site's content</h2>
<ul>
<li>Opening hours, dishes and availability may change. Prices are those on the restaurant's menu, VAT included. Written information on the 14 allergens in each dish is available in the restaurant.</li>
<li>Guest opinions are short excerpts from public reviews on Google and TheFork (as shown on Trip.com), without the authors' names. The quote from NiT magazine is credited with author and date.</li>
<li>The drawings are original to this site. Map data © <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap</a> contributors (ODbL). Bodoni Moda, Marcellus SC and Jost typefaces, SIL Open Font License.</li>
</ul>
""",
)

NOT_FOUND = [
    # lang, heading, text, link label, link
    ("pt-PT", "Esta rua não vai dar ao Largo.", "A página que procura não existe ou mudou de sítio.", "Voltar ao Cidade Velha", "/"),
    ("en", "This street doesn't lead to the square.", "The page you are looking for doesn't exist or has moved.", "Back to Cidade Velha in English", "/en/"),
    ("fr", "Cette rue ne mène pas à la place.", "La page que vous cherchez n'existe pas ou a été déplacée.", "Retour à Cidade Velha en français", "/fr/"),
    ("de", "Diese Gasse führt nicht zum Platz.", "Die gesuchte Seite gibt es nicht oder sie wurde verschoben.", "Zurück zu Cidade Velha auf Deutsch", "/de/"),
]
