import json
from pathlib import Path

entries = []
for f in sorted(Path("entries").glob("*.json"), reverse=True):
    with open(f) as fh:
        entries.append(json.load(fh))

entries_json = json.dumps(entries, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Quiet Archive</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink:       #1a1714;
    --ink-soft:  #4a4540;
    --ink-mute:  #9a9088;
    --paper:     #f7f4ee;
    --paper-warm:#ede8df;
    --rule:      #d8d0c4;
    --red:       #9b2335;
    --red-light: #f0e4e7;
    --serif:     'Playfair Display', Georgia, serif;
    --sans:      'Source Sans 3', system-ui, sans-serif;
  }}

  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    background: var(--paper);
    color: var(--ink);
    font-family: var(--sans);
    font-weight: 300;
    min-height: 100vh;
  }}

  .masthead {{
    border-bottom: 3px double var(--ink);
    padding: 2.5rem 2rem 1.5rem;
    text-align: center;
  }}
  .masthead-eyebrow {{
    font-family: var(--sans);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--ink-mute);
    margin-bottom: 0.6rem;
  }}
  .masthead h1 {{
    font-family: var(--serif);
    font-size: clamp(2.4rem, 6vw, 4rem);
    font-weight: 700;
    line-height: 1;
    letter-spacing: -0.02em;
  }}
  .masthead-sub {{
    font-family: var(--serif);
    font-style: italic;
    font-size: 1rem;
    color: var(--ink-soft);
    margin-top: 0.5rem;
  }}
  .masthead-count {{
    display: inline-block;
    margin-top: 1.2rem;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--red);
    border: 1px solid var(--red);
    padding: 0.3rem 0.8rem;
  }}

  .controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    align-items: center;
    padding: 1rem 2rem;
    border-bottom: 1px solid var(--rule);
    background: var(--paper-warm);
  }}
  .search-wrap {{
    flex: 1;
    min-width: 180px;
    position: relative;
  }}
  .search-wrap input {{
    width: 100%;
    font-family: var(--sans);
    font-size: 0.85rem;
    padding: 0.5rem 0.75rem 0.5rem 2rem;
    border: 1px solid var(--rule);
    background: var(--paper);
    color: var(--ink);
    outline: none;
  }}
  .search-wrap input:focus {{ border-color: var(--ink-soft); }}
  .search-icon {{
    position: absolute;
    left: 0.6rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--ink-mute);
    font-size: 0.9rem;
    pointer-events: none;
  }}
  .filter-group {{
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
  }}
  .filter-btn {{
    font-family: var(--sans);
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.35rem 0.7rem;
    border: 1px solid var(--rule);
    background: transparent;
    color: var(--ink-soft);
    cursor: pointer;
    transition: all 0.15s;
  }}
  .filter-btn:hover, .filter-btn.active {{
    background: var(--ink);
    color: var(--paper);
    border-color: var(--ink);
  }}
  .sort-select {{
    font-family: var(--sans);
    font-size: 0.75rem;
    padding: 0.4rem 0.6rem;
    border: 1px solid var(--rule);
    background: var(--paper);
    color: var(--ink);
    cursor: pointer;
    outline: none;
  }}

  .layout {{
    display: grid;
    grid-template-columns: 1fr 360px;
    min-height: calc(100vh - 200px);
  }}

  .entry-list {{
    border-right: 1px solid var(--rule);
    overflow-y: auto;
  }}
  .entry-item {{
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid var(--rule);
    cursor: pointer;
    transition: background 0.1s;
  }}
  .entry-item:hover {{ background: var(--paper-warm); }}
  .entry-item.selected {{ background: var(--red-light); border-left: 3px solid var(--red); }}
  .entry-num {{
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--ink-mute);
  }}
  .entry-title {{
    font-family: var(--serif);
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.3;
    margin: 0.2rem 0;
  }}
  .entry-meta {{
    font-size: 0.72rem;
    color: var(--ink-mute);
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 0.25rem;
  }}
  .entry-meta span::before {{ content: '·'; margin-right: 0.4rem; }}
  .entry-meta span:first-child::before {{ content: ''; margin-right: 0; }}
  .tag {{
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.15rem 0.4rem;
    border: 1px solid var(--rule);
    color: var(--ink-soft);
    margin-right: 0.25rem;
    margin-top: 0.3rem;
  }}

  .detail-pane {{
    padding: 2rem 1.75rem;
    overflow-y: auto;
    position: sticky;
    top: 0;
    max-height: 100vh;
  }}
  .detail-empty {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 60%;
    text-align: center;
    color: var(--ink-mute);
  }}
  .detail-empty-glyph {{
    font-family: var(--serif);
    font-size: 4rem;
    line-height: 1;
    margin-bottom: 1rem;
    opacity: 0.3;
  }}
  .detail-empty p {{ font-style: italic; font-size: 0.9rem; }}
  .detail-eyebrow {{
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 0.5rem;
  }}
  .detail-title {{
    font-family: var(--serif);
    font-size: clamp(1.3rem, 2.5vw, 1.7rem);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 0.75rem;
  }}
  .detail-dateline {{
    font-family: var(--serif);
    font-style: italic;
    font-size: 0.85rem;
    color: var(--ink-soft);
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--rule);
    margin-bottom: 1.25rem;
  }}
  .detail-section-label {{
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--ink-mute);
    margin-bottom: 0.4rem;
    margin-top: 1.25rem;
  }}
  .detail-section-label:first-of-type {{ margin-top: 0; }}
  .detail-text {{
    font-size: 0.9rem;
    line-height: 1.75;
    color: var(--ink-soft);
  }}
  .detail-tags {{
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--rule);
  }}
  .no-results {{
    padding: 3rem 2rem;
    text-align: center;
    color: var(--ink-mute);
    font-style: italic;
  }}

  @media (max-width: 700px) {{
    .layout {{ grid-template-columns: 1fr; }}
    .detail-pane {{
      position: fixed;
      inset: 0;
      background: var(--paper);
      z-index: 100;
      transform: translateX(100%);
      transition: transform 0.25s ease;
      padding: 1.5rem 1.25rem;
      max-height: 100vh;
    }}
    .detail-pane.open {{ transform: translateX(0); }}
    .detail-close {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.75rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--ink-mute);
      background: none;
      border: none;
      cursor: pointer;
      padding: 0;
      margin-bottom: 1.5rem;
    }}
  }}
  @media (min-width: 701px) {{ .detail-close {{ display: none; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>
</head>
<body>

<header class="masthead">
  <p class="masthead-eyebrow">A daily archive of overlooked history</p>
  <h1>The Quiet Archive</h1>
  <p class="masthead-sub">The moments that changed everything — and were forgotten anyway</p>
  <span class="masthead-count" id="entry-count"></span>
</header>

<div class="controls">
  <div class="search-wrap">
    <span class="search-icon">⌕</span>
    <input type="text" id="search" placeholder="Search events, places, topics…" oninput="applyFilters()">
  </div>
  <div class="filter-group" id="era-filters">
    <button class="filter-btn active" onclick="setEra('all', this)">All eras</button>
    <button class="filter-btn" onclick="setEra('Ancient', this)">Ancient</button>
    <button class="filter-btn" onclick="setEra('Medieval', this)">Medieval</button>
    <button class="filter-btn" onclick="setEra('Early Modern', this)">Early Modern</button>
    <button class="filter-btn" onclick="setEra('Modern', this)">Modern</button>
    <button class="filter-btn" onclick="setEra('Contemporary', this)">Contemporary</button>
  </div>
  <select class="sort-select" id="sort-select" onchange="applyFilters()">
    <option value="newest">Newest first</option>
    <option value="oldest">Oldest first</option>
    <option value="az">A–Z</option>
  </select>
</div>

<div class="layout">
  <div class="entry-list" id="entry-list"></div>
  <div class="detail-pane" id="detail-pane">
    <button class="detail-close" onclick="closeDetail()">← Back to list</button>
    <div id="detail-content">
      <div class="detail-empty">
        <div class="detail-empty-glyph">§</div>
        <p>Select an entry to read</p>
      </div>
    </div>
  </div>
</div>

<script>
const ALL_ENTRIES = {entries_json};

let currentEra = 'all';
let selectedIndex = null;

function setEra(era, btn) {{
  currentEra = era;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  applyFilters();
}}

function applyFilters() {{
  const q = document.getElementById('search').value.toLowerCase();
  const sort = document.getElementById('sort-select').value;

  let filtered = ALL_ENTRIES.filter(e => {{
    const matchEra = currentEra === 'all' || e.era === currentEra;
    const matchQ = !q ||
      e.title.toLowerCase().includes(q) ||
      e.location.toLowerCase().includes(q) ||
      e.event_summary.toLowerCase().includes(q) ||
      (e.topic_tags || []).some(t => t.toLowerCase().includes(q));
    return matchEra && matchQ;
  }});

  if (sort === 'oldest') filtered = [...filtered].reverse();
  else if (sort === 'az') filtered = [...filtered].sort((a,b) => a.title.localeCompare(b.title));

  renderList(filtered);
}}

function renderList(entries) {{
  const list = document.getElementById('entry-list');
  document.getElementById('entry-count').textContent =
    ALL_ENTRIES.length === 1
      ? '1 entry in the archive'
      : ALL_ENTRIES.length + ' entries in the archive';

  if (!entries.length) {{
    list.innerHTML = '<p class="no-results">No entries match your search.</p>';
    return;
  }}

  list.innerHTML = entries.map((e) => `
    <div class="entry-item ${{selectedIndex === e.entry_number ? 'selected' : ''}}"
         onclick="showDetail(${{JSON.stringify(e).replace(/'/g, '&apos;')}}, ${{e.entry_number}})">
      <div class="entry-num">#${{String(e.entry_number).padStart(3,'0')}} &nbsp;·&nbsp; ${{e.date_added || ''}}</div>
      <div class="entry-title">${{e.title}}</div>
      <div class="entry-meta">
        <span>${{e.date}}</span>
        <span>${{e.location}}</span>
        <span>${{e.era}}</span>
      </div>
      <div>${{(e.topic_tags || []).map(t => `<span class="tag">${{t}}</span>`).join('')}}</div>
    </div>
  `).join('');
}}

function showDetail(entry, num) {{
  selectedIndex = num;
  document.querySelectorAll('.entry-item').forEach(el => el.classList.remove('selected'));
  event.currentTarget.classList.add('selected');

  document.getElementById('detail-content').innerHTML = `
    <div class="detail-eyebrow">Entry #${{String(entry.entry_number).padStart(3,'0')}}</div>
    <h2 class="detail-title">${{entry.title}}</h2>
    <p class="detail-dateline">${{entry.date}} &nbsp;·&nbsp; ${{entry.location}} &nbsp;·&nbsp; ${{entry.era}}</p>
    <p class="detail-section-label">What happened</p>
    <p class="detail-text">${{entry.event_summary}}</p>
    <p class="detail-section-label">Why it was forgotten</p>
    <p class="detail-text">${{entry.why_forgotten}}</p>
    <p class="detail-section-label">Why it actually matters</p>
    <p class="detail-text">${{entry.why_it_matters}}</p>
    <div class="detail-tags">
      ${{(entry.topic_tags || []).map(t => `<span class="tag">${{t}}</span>`).join('')}}
    </div>
  `;

  document.getElementById('detail-pane').classList.add('open');
}}

function closeDetail() {{
  document.getElementById('detail-pane').classList.remove('open');
}}

applyFilters();
</script>
</body>
</html>"""

Path("docs").mkdir(exist_ok=True)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✓ Site built with {{len(entries)}} entries → docs/index.html")