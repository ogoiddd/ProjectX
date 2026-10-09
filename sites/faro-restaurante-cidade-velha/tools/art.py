"""Hand-drawn SVG compositions used on the site (no third-party imagery).
Colours follow the concept: cal (lime-wash), pedra (Sé limestone), tinto (Port), tinta (ink)."""

INK = "#211915"
CAL = "#f4eee3"
STONE = "#d8c3a0"
STONE_D = "#c6a978"
WINE = "#6a1d29"
SUN = "#d49a3f"

ARCH = "M0 640V300A300 300 0 0 1 240 6A300 300 0 0 1 480 300V640Z"


def hero_svg(title, uid="h"):
    """The Sé bell-tower seen from the Largo, inside a pointed arch. Engraving-like hatching, flat tones."""
    return f'''<svg viewBox="0 0 480 640" role="img" aria-labelledby="{uid}-t"><title id="{uid}-t">{title}</title>
<defs>
<clipPath id="{uid}-arch"><path d="{ARCH}"/></clipPath>
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
<path d="M222 94q18 6 36 0l-4 6h-28z" fill="#6b5340" stroke="{INK}" stroke-width="1"/>
<path d="M236 88q-2-10 8-12q10-1 13 6l-6 8z" fill="{CAL}" stroke="{INK}" stroke-width="1.1"/>
<path d="M249 82q1-14-3-22" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>
<path d="M249 82q1-14-3-22" fill="none" stroke="{CAL}" stroke-width="1.2" stroke-linecap="round"/>
<path d="M246 60l12-4" stroke="#b9572e" stroke-width="2.4" stroke-linecap="round"/>
<path d="M238 84q8 6 16 2" fill="none" stroke="{INK}" stroke-width="2.2"/>
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
<path d="{ARCH}" fill="none" stroke="{INK}" stroke-width="2.5"/>
<path d="M14 640V302A286 286 0 0 1 240 22A286 286 0 0 1 466 302V640" fill="none" stroke="{INK}" stroke-width="1" opacity=".55"/>
</svg>'''


def dom_rodrigo_svg(title):
    """Dom Rodrigo in its twisted foil wrap, with a small glass of Port."""
    return f'''<svg viewBox="0 0 220 180" role="img" aria-labelledby="dr-t"><title id="dr-t">{title}</title>
<ellipse cx="104" cy="164" rx="86" ry="9" fill="#000" opacity=".18"/>
<path d="M46 160l10-58h96l10 58z" fill="#c9a24a" stroke="{CAL}" stroke-width="1.5" stroke-linejoin="round"/>
<path d="M60 108l-8 50M78 104l-4 56M98 104v56M118 104l2 56M138 106l6 54M152 110l8 46" stroke="{CAL}" stroke-width=".9" opacity=".55"/>
<path d="M56 102q48-22 96 0q-10-24-30-34q-18-6-36 0q-20 10-30 34z" fill="#f2c94c" stroke="{CAL}" stroke-width="1.2"/>
<g fill="none" stroke="#b47d12" stroke-width=".9" opacity=".8"><path d="M70 94q10-8 20 0t20 0t20 0t14-2"/><path d="M76 86q8-6 16 0t16 0t16 0t12 0"/><path d="M86 78q6-5 12 0t12 0t12 0"/></g>
<path d="M88 66q16-30 32 0" fill="#c9a24a" stroke="{CAL}" stroke-width="1.4"/>
<path d="M104 40q-22-14-30-4q12 6 30 22q18-16 30-22q-8-10-30 4z" fill="#d9b24f" stroke="{CAL}" stroke-width="1.4" stroke-linejoin="round"/>
<path d="M96 60l8 6l8-6" fill="none" stroke="{CAL}" stroke-width="1.4"/>
<g transform="translate(176 92)">
<path d="M-14 0q0 30 14 32q14-2 14-32z" fill="none" stroke="{CAL}" stroke-width="1.6"/>
<path d="M-12.6 12q1 18 12.6 19q11.6-1 12.6-19z" fill="#3a0d14"/>
<path d="M0 32v32M-12 66h24" stroke="{CAL}" stroke-width="1.6" stroke-linecap="round"/>
</g>
</svg>'''


LOGO = f'''<svg viewBox="0 0 64 80" aria-hidden="true"><path d="M4 78V38A30 30 0 0 1 32 3A30 30 0 0 1 60 38V78" fill="none" stroke="currentColor" stroke-width="3"/><path d="M14 78V44A20 20 0 0 1 32 20A20 20 0 0 1 50 44V78Z" fill="currentColor"/><path d="M32 20V78" stroke="{CAL}" stroke-width="1.6"/></svg>'''

FAVICON = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="{CAL}"/><path d="M12 60V32A22 22 0 0 1 32 7A22 22 0 0 1 52 32V60" fill="none" stroke="{WINE}" stroke-width="4"/><path d="M20 60V36A14 14 0 0 1 32 19A14 14 0 0 1 44 36V60Z" fill="{WINE}"/></svg>'''

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
