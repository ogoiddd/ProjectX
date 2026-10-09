"""Hand-drawn SVG compositions used on the site (no third-party imagery).
Colours follow the concept: cal (lime-wash), pedra (Sé limestone), tinto (Port), tinta (ink)."""

INK = "#211915"
CAL = "#f4eee3"
STONE = "#d8c3a0"
STONE_D = "#c6a978"
WINE = "#6a1d29"
SUN = "#d49a3f"

PLATE = "M0 0H480V640H0Z"   # the composition is printed like an engraved plate, not framed in an arch


def hero_svg(title, uid="h"):
    """The Sé bell-tower seen from the Largo, as an engraved plate (double plate-mark). Hatching, flat tones."""
    return f'''<svg viewBox="0 0 480 640" role="img" aria-labelledby="{uid}-t"><title id="{uid}-t">{title}</title>
<defs>
<clipPath id="{uid}-arch"><path d="{PLATE}"/></clipPath>
<pattern id="{uid}-hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><line x1="0" y1="0" x2="0" y2="5" stroke="{INK}" stroke-width="1" opacity=".38"/></pattern>
<pattern id="{uid}-hatch2" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)"><line x1="0" y1="0" x2="0" y2="7" stroke="{WINE}" stroke-width=".8" opacity=".28"/></pattern>
<pattern id="{uid}-cobble" width="26" height="13" patternUnits="userSpaceOnUse"><path d="M0 .5h26M0 6.5h26M6 .5v6M19 6.5v6.5" fill="none" stroke="{INK}" stroke-width=".7" opacity=".35"/></pattern>
</defs>
<g clip-path="url(#{uid}-arch)">
<rect width="480" height="640" fill="#eadcc2"/>
<g fill="none" stroke="{INK}" stroke-width=".6" opacity=".16"><path d="M0 70h480M0 92h480M0 118h480M0 150h480M0 190h480M0 238h480"/></g>
<circle class="sun" cx="372" cy="214" r="50" fill="{SUN}"/>
<!-- rooftops / houses of the Largo -->
<path d="M-10 640V402h70v-14l30-18 30 18v14h46v238Z" fill="{CAL}" stroke="{INK}" stroke-width="1.4"/>
<path d="M18 432h22v34H18zM78 432h22v34H78z" fill="{INK}" opacity=".78"/>
<path d="M332 640V420l40-26h120v246Z" fill="{CAL}" stroke="{INK}" stroke-width="1.4"/>
<path d="M332 420h160" stroke="{INK}" stroke-width="1.4"/>
<path d="M352 446h18v40h-18zM400 446h18v40h-18zM448 446h18v40h-18z" fill="{INK}" opacity=".78"/>
<path d="M346 440h30M394 440h30M442 440h30" stroke="{INK}" stroke-width="2.5"/>
<!-- nave behind the tower -->
<path d="M116 640V362l8-10h232l8 10v278Z" fill="{CAL}" stroke="{INK}" stroke-width="1.4"/>
<path d="M124 352l-8 10h248l-8-10" fill="none" stroke="{INK}" stroke-width="1.4"/>
<path d="M126 362v278M354 362v278" stroke="{INK}" stroke-width="1" opacity=".5"/>
<!-- tower -->
<g>
<rect x="160" y="200" width="160" height="440" fill="{STONE}" stroke="{INK}" stroke-width="1.6"/>
<rect x="290" y="200" width="30" height="440" fill="url(#{uid}-hatch)"/>
<path d="M160 200h160M156 196h168v8H156z" fill="{STONE_D}" stroke="{INK}" stroke-width="1.4"/>
<path d="M156 330h168" stroke="{INK}" stroke-width="1.2"/>
<path d="M224 262a16 16 0 0 1 32 0v34h-32z" fill="{INK}"/>
<!-- belfry -->
<rect x="182" y="132" width="116" height="64" fill="{STONE}" stroke="{INK}" stroke-width="1.6"/>
<rect x="278" y="132" width="20" height="64" fill="url(#{uid}-hatch)"/>
<path d="M198 196v-36a15 15 0 0 1 30 0v36zM252 196v-36a15 15 0 0 1 30 0v36z" fill="{INK}"/>
<path d="M205 172q8-14 16 0l2 8h-20zM259 172q8-14 16 0l2 8h-20z" fill="{SUN}" opacity=".9"/>
<path d="M176 132h128l-64-38z" fill="{STONE_D}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>
<path d="M240 94l40 24v14h-40z" fill="url(#{uid}-hatch)"/>
<path d="M172 128h8v8h-8zM300 128h8v8h-8z" fill="{INK}"/>
<!-- stork on its nest -->
<g class="stork">
<path d="M220 95q20 7 40 0l-3 6h-34z" fill="#6b5340" stroke="{INK}" stroke-width="1"/>
<path d="M221 95l5-4M232 93l4-5M246 93l-3-5M256 94l-4-4" stroke="#6b5340" stroke-width="1.4"/>
<path d="M238 92v-11M244 92v-11" stroke="#b9572e" stroke-width="1.6" stroke-linecap="round"/>
<path d="M226 74q8-9 22-6q6 2 6 8q-4 6-16 6q-8 0-12-8z" fill="{CAL}" stroke="{INK}" stroke-width="1.1"/>
<path d="M226 74q6 6 15 7l-3-8q-6-2-12 1z" fill="{INK}"/>
<path d="M251 71q4-8 3-17" fill="none" stroke="{INK}" stroke-width="3.6" stroke-linecap="round"/>
<path d="M251 71q4-8 3-17" fill="none" stroke="{CAL}" stroke-width="1.8" stroke-linecap="round"/>
<circle cx="254.5" cy="53" r="3.2" fill="{CAL}" stroke="{INK}" stroke-width="1"/>
<path d="M257 53.5l13 4" stroke="#b9572e" stroke-width="2.2" stroke-linecap="round"/>
</g>
<!-- gothic portal: three archivolts -->
<path d="M176 640V470A128 128 0 0 1 240 359A128 128 0 0 1 304 470V640" fill="{STONE_D}" stroke="{INK}" stroke-width="1.4"/>
<path d="M188 640V470A104 104 0 0 1 240 380A104 104 0 0 1 292 470V640" fill="{STONE}" stroke="{INK}" stroke-width="1.4"/>
<path d="M188 640V470A104 104 0 0 1 240 380" fill="none" stroke="url(#{uid}-hatch)" stroke-width="0"/>
<path d="M200 640V470A80 80 0 0 1 240 401A80 80 0 0 1 280 470V640Z" fill="{WINE}" stroke="{INK}" stroke-width="1.6"/>
<path d="M200 640V470A80 80 0 0 1 240 401A80 80 0 0 1 280 470V640Z" fill="url(#{uid}-hatch2)"/>
<path d="M240 401V640" stroke="{INK}" stroke-width="1" opacity=".6"/>
</g>
<!-- the Largo: cobbles -->
<path d="M-10 572H490V650H-10z" fill="#cdb58d"/>
<path d="M-10 572H490V650H-10z" fill="url(#{uid}-cobble)"/>
<path d="M-10 572H490" stroke="{INK}" stroke-width="1.4"/>
<!-- esplanada: table, chairs, two glasses of red -->
<g stroke="{INK}" stroke-width="2" stroke-linecap="round" fill="none">
<path d="M58 596h92M104 596v40M88 636h32"/>
<path d="M36 640v-48h18v24M30 616h28M172 640v-48h-18v24M150 616h28"/>
</g>
<path d="M58 593h92" stroke="{CAL}" stroke-width="4"/>
<path d="M90 576q-1 9 5 10q6-1 5-10z" fill="{WINE}" stroke="{INK}" stroke-width="1"/>
<path d="M95 586v7M91 593h8" stroke="{INK}" stroke-width="1.2"/>
<path d="M112 578q-1 8 5 9q6-1 5-9z" fill="{WINE}" stroke="{INK}" stroke-width="1"/>
<path d="M117 587v6M113 593h8" stroke="{INK}" stroke-width="1.2"/>
</g>
<rect x="1.25" y="1.25" width="477.5" height="637.5" fill="none" stroke="{INK}" stroke-width="2.5"/>
<rect x="9" y="9" width="462" height="622" fill="none" stroke="{INK}" stroke-width=".8" opacity=".6"/>
</svg>'''


def dom_rodrigo_svg(title):
    """Dom Rodrigo in its twisted foil wrap, with a small glass of Port."""
    return f'''<svg viewBox="0 0 220 180" role="img" aria-labelledby="dr-t"><title id="dr-t">{title}</title>
<ellipse cx="104" cy="165" rx="72" ry="8" fill="#000" opacity=".2"/>
<path d="M40 150C40 116 66 96 94 88h20c28 8 54 28 54 62c0 10-28 15-64 15s-64-5-64-15z" fill="#d9b24f" stroke="{CAL}" stroke-width="1.5" stroke-linejoin="round"/>
<g fill="none" stroke="{CAL}" stroke-width="1" opacity=".6" stroke-linecap="round"><path d="M96 90Q70 118 60 160M100 90Q90 124 86 164M104 90v74M108 90q10 34 14 74M112 90q26 28 36 70"/></g>
<path d="M58 132q10-30 34-40q-18 22-22 52z" fill="#f4d98a" opacity=".55"/>
<path d="M94 88q10 5 20 0l-2-10q-8 4-16 0z" fill="#b8902f" stroke="{CAL}" stroke-width="1.3" stroke-linejoin="round"/>
<path d="M96 78L70 46l14 2l-4-14l14 10l6-16l4 18q2-20 6-18l6 16l14-10l-4 14l14-2l-26 32q-10 5-20 0z" fill="#e3c060" stroke="{CAL}" stroke-width="1.4" stroke-linejoin="round"/>
<g fill="none" stroke="{CAL}" stroke-width=".9" opacity=".6" stroke-linecap="round"><path d="M98 76L82 50M102 76L96 40M106 76l6-36M110 76l16-26"/></g>
<g transform="translate(176 92)">
<path d="M-14 0q0 30 14 32q14-2 14-32z" fill="none" stroke="{CAL}" stroke-width="1.6"/>
<path d="M-12.6 12q1 18 12.6 19q11.6-1 12.6-19z" fill="#3a0d14"/>
<path d="M0 32v32M-12 66h24" stroke="{CAL}" stroke-width="1.6" stroke-linecap="round"/>
</g>
</svg>'''


TOWER = '<path fill-rule="evenodd" d="M10 22L24 7L38 22Z M10 23h28v13H10z M15 36v-7a3 3 0 0 1 6 0v7z M27 36v-7a3 3 0 0 1 6 0v7z M7 37h34v3H7z M10 41h28v37H10z M18 78V63a6 8 0 0 1 6-8a6 8 0 0 1 6 8v15z M22 47a2 2 0 0 1 4 0v4h-4z"/>'
LOGO = f'''<svg viewBox="0 0 48 80" aria-hidden="true" fill="currentColor">{TOWER}</svg>'''

FAVICON = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="6" fill="{CAL}"/><rect x="4.5" y="4.5" width="55" height="55" fill="none" stroke="{WINE}" stroke-width="1.5"/><g transform="translate(18.5 9) scale(.56)" fill="{WINE}">{TOWER}</g></svg>'''

ICONS = {
    "phone": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>',
    "arrow": '<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15M13 6l6 6-6 6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "table": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9h18M12 9v11M8 20h8M6 9l-2 11M18 9l2 11"/><path d="M9 6q3-3 6 0"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 .8a4 4 0 0 1-1.8-1.8l.8-1-1-2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 7l9 6 9-6"/></svg>',
    "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4L2.8 9.5l6.4-.8z"/></svg>',
    "star_part": '<svg viewBox="0 0 24 24" aria-hidden="true"><defs><clipPath id="sp"><rect width="9.6" height="24"/></clipPath></defs><path fill="none" stroke="currentColor" stroke-width="1.2" d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4L2.8 9.5l6.4-.8z"/><path clip-path="url(#sp)" fill="currentColor" d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2l-5.7 3.1 1.2-6.4L2.8 9.5l6.4-.8z"/></svg>',
}
