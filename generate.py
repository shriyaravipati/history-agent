import anthropic
import json
import os
from datetime import date
from pathlib import Path

# ── Read state ───────────────────────────────────────────────
with open("entry_count.txt") as f:
    entry_num = int(f.read().strip()) + 1

seen = []
if os.path.exists("seen_events.txt"):
    with open("seen_events.txt") as f:
        seen = [line.strip() for line in f if line.strip()]

recent = seen[-40:] if len(seen) > 40 else seen
avoid_block = ""
if recent:
    avoid_block = "Do NOT generate any of these already-used events:\n" + \
                  "\n".join(f"- {e}" for e in recent)

# ── Prompt ───────────────────────────────────────────────────
prompt = f"""You are a historian specializing in overlooked events. Generate one forgotten but genuinely world-changing historical event.

Rules:
- NOT a famous battle, major war, or well-known leader's death
- NOT something commonly taught in Western high schools
- Must be specific: a real date, real people, a real place
- Rotate across regions and eras — don't focus only on Europe or the US
- Choose events with clear, surprising modern relevance
{avoid_block}

Respond ONLY in valid JSON, no preamble, no markdown:
{{
  "title": "Short evocative title (max 8 words)",
  "date": "Specific date or period, e.g. March 1847 or 664 AD",
  "location": "Country or region",
  "era": "Ancient | Medieval | Early Modern | Modern | Contemporary",
  "topic_tags": ["tag1", "tag2", "tag3"],
  "event_summary": "2-3 vivid sentences describing exactly what happened.",
  "why_forgotten": "2-3 sentences on why historians or powers suppressed or ignored this.",
  "why_it_matters": "2-3 sentences on its lasting hidden influence on the world today.",
  "entry_number": {entry_num}
}}"""

# ── Call Claude ───────────────────────────────────────────────
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

raw = response.content[0].text.strip()
if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()

data = json.loads(raw)
data["date_added"] = date.today().isoformat()

# ── Save entry ────────────────────────────────────────────────
Path("entries").mkdir(exist_ok=True)
filename = f"entries/{str(entry_num).zfill(4)}.json"
with open(filename, "w") as f:
    json.dump(data, f, indent=2)

print(f"✓ Saved: {filename} — {data['title']}")

# ── Update state ──────────────────────────────────────────────
with open("entry_count.txt", "w") as f:
    f.write(str(entry_num))

with open("seen_events.txt", "a") as f:
    f.write(data["title"] + "\n")

print("✓ Done. Run build_site.py to update the website.")