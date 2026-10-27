"""Superior EHS Manager Dashboard Builder.
Builds index.html from data.py.
"""
import calendar, json, urllib.request
from datetime import datetime, timedelta, date
from data import *

try:
    from zoneinfo import ZoneInfo
    NOW = datetime.now(ZoneInfo("America/New_York"))
except:
    NOW = datetime.now()
TODAY = NOW.date()
OUTPUT_FILE = "index.html"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=8) as r:
        return json.loads(r.read())

def human_time(dt):
    return dt.strftime("%I:%M %p").lstrip("0")

# Weather
wx_html = ""
try:
    lat, lon = HOME_COORDS
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&temperature_unit=fahrenheit&forecast_days=1&time_zone=America%2FNew_York"
    data = fetch(url)
    temp = round(data["current"]["temperature_2m"])
    hi = round(data["daily"]["temperature_2m_max"][0])
    lo = round(data["daily"]["temperature_2m_min"][0])
    rain = data["daily"]["precipitation_probability_max"][0] or 0
    wx_html = f'<div class="wx-simple"><span class="wx-temp">{temp}°</span> <span class="wx-hilo">{hi}° / {lo}°</span> <span class="wx-rain">{rain}% rain</span></div>'
except:
    wx_html = '<div class="wx-simple">--°</div>'

# Quote of the day
q = LEADERSHIP_QUOTES[TODAY.timetuple().tm_yday % len(LEADERSHIP_QUOTES)]

# Incident chart SVG
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
max_val = max(list(INCIDENTS_2026.values()) + list(INCIDENTS_2025.values()) + [5])
# Build line chart — Power BI style
# Points + lines for 2026, 2025, and a flat benchmark line
def build_line_chart():
    w, h = 520, 200
    pad = {"t": 25, "r": 30, "b": 30, "l": 35}
    cw = w - pad["l"] - pad["r"]
    ch = h - pad["t"] - pad["b"]
    all_vals = list(INCIDENTS_2026.values()) + list(INCIDENTS_2025.values()) + [INDUSTRY_BENCHMARK]
    max_v = max(all_vals) if all_vals else 5
    max_v = max(max_v, 5)
    
    def xpos(i):
        return pad["l"] + (i / 11) * cw
    def ypos(v):
        return pad["t"] + ch - (v / (max_v * 1.2)) * ch
    
    # Grid lines
    grid = ""
    for g in range(0, int(max_v * 1.2) + 2):
        gy = ypos(g)
        grid += f'<line x1="{pad["l"]}" y1="{gy}" x2="{w - pad["r"]}" y2="{gy}" stroke="#475569" stroke-width="0.5"/>'
        grid += f'<text x="{pad["l"] - 4}" y="{gy + 3}" font-size="8" fill="#64748b" text-anchor="end">{g}</text>'
    
    # 2025 line (blue, dashed)
    pts25 = []
    for i, m in enumerate(months):
        pts25.append(f'{xpos(i)},{ypos(INCIDENTS_2025[m] or 0)}')
    line25 = f'<polyline points="{" ".join(pts25)}" fill="none" stroke="#3b82f6" stroke-width="2" stroke-dasharray="4,3" opacity="0.7"/>'
    
    # 2026 line (amber, solid)
    pts26 = []
    for i, m in enumerate(months):
        pts26.append(f'{xpos(i)},{ypos(INCIDENTS_2026[m] or 0)}')
    line26 = f'<polyline points="{" ".join(pts26)}" fill="none" stroke="#f59e0b" stroke-width="2.5"/>'
    
    # 2026 dots
    dots26 = ""
    for i, m in enumerate(months):
        v = INCIDENTS_2026[m] or 0
        dots26 += f'<circle cx="{xpos(i)}" cy="{ypos(v)}" r="3.5" fill="#f59e0b" stroke="#1e293b" stroke-width="1"/>'
    
    # Industry benchmark flat line
    by = ypos(INDUSTRY_BENCHMARK)
    bench_line = f'<line x1="{pad["l"]}" y1="{by}" x2="{w - pad["r"]}" y2="{by}" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="5,3"/>'
    bench_label = f'<text x="{w - pad["r"]}" y="{by - 4}" font-size="9" fill="#ef4444" text-anchor="end">Industry {INDUSTRY_BENCHMARK}</text>'
    
    # Month labels
    month_labels = ""
    for i, m in enumerate(months):
        month_labels += f'<text x="{xpos(i)}" y="{h - 5}" font-size="8" fill="#64748b" text-anchor="middle">{m[:3]}</text>'
    
    # Legend
    legend = f'<rect x="{pad["l"]}" y="6" width="10" height="3" fill="#f59e0b"/><text x="{pad["l"] + 14}" y="10" font-size="8" fill="#94a3b8">2026</text>'
    legend += f'<rect x="{pad["l"] + 60}" y="6" width="10" height="3" fill="#3b82f6"/><text x="{pad["l"] + 74}" y="10" font-size="8" fill="#94a3b8">2025</text>'
    legend += f'<line x1="{pad["l"] + 120}" y1="7" x2="{pad["l"] + 130}" y2="7" stroke="#ef4444" stroke-width="1.5"/><text x="{pad["l"] + 134}" y="10" font-size="8" fill="#94a3b8">Industry</text>'
    
    svg = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{grid}{line25}{line26}{dots26}{bench_line}{bench_label}{month_labels}{legend}</svg>'
    return svg

chart_svg = build_line_chart()

# Action board
def action_list(items, color):
    return "\n".join(f'<div class="action-row" style="border-left:3px solid {color}"><span>{i}</span></div>' for i in items)

# Meetings - manual from MEETINGS
def build_week_calendar(meetings):
    days_html = ""
    for offset in range(7):
        day = TODAY + timedelta(days=offset)
        iso = day.isoformat()
        label = "Today" if offset == 0 else day.strftime("%a")
        date_num = day.day
        day_events = sorted([m for m in meetings if m["date"] == iso], key=lambda m: m["time"])
        events_html = ""
        for m in day_events:
            loc = f' <span class="wloc">({m["loc"]})</span>' if m.get("loc") else ""
            events_html += f'<div class="wevent"><span class="wtime">{m["time"]}</span> {m["title"]}{loc}</div>'
        if not events_html:
            events_html = '<div class="wevent empty">--</div>'
        today_class = ' wday-today' if offset == 0 else ''
        days_html += f'<div class="wday{today_class}"><div class="wday-head">{label}<span class="wdate">{date_num}</span></div>{events_html}</div>'
    return f'<div class="week-grid">{days_html}</div>'

meeting_html = build_week_calendar(MEETINGS)

# Corrective actions
ca_rows = []
for ca in CORRECTIVE_ACTIONS:
    icon = {"open":"\U0001f534","in-progress":"\U0001f7e1","closed":"\U0001f7e2"}.get(ca["status"], "\u26aa")
    ca_rows.append(f'<div class="ca-row">{icon} <b>{ca["owner"]}</b> {ca["title"]} <span class="muted">({ca["days"]}d)</span></div>')
ca_html = "\n".join(ca_rows) if ca_rows else '<div class="empty">No open items</div>'

# Build HTML
date_line = NOW.strftime("%A").upper() + " " + NOW.strftime("%B").upper() + " " + str(NOW.day)

CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{background:#1e293b;color:#e2e8f0;font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-size:16px;padding:20px 24px}
.card{background:#334155;border:1px solid #475569;border-radius:12px;padding:16px 20px;margin-bottom:16px}
h2{font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:#94a3b8;margin-bottom:10px;font-weight:700}
h3{font-size:14px;font-weight:800;margin-bottom:8px;letter-spacing:1px}
.empty{color:#64748b;font-size:14px;margin:4px 0}
.muted{color:#64748b;font-size:12px}
.header{display:flex;align-items:flex-start;margin-bottom:16px}
.header>div:nth-child(1){width:40%}
.header>div:nth-child(2){width:35%}
.header>div:nth-child(3){width:25%;text-align:right}
.clock{font-size:52px;font-weight:800;letter-spacing:-1.5px;color:#f8fafc}
.clock small{font-size:26px;font-weight:700;margin-left:4px}
.date-line{font-size:16px;font-weight:600;letter-spacing:1.5px;color:#94a3b8;margin-top:4px}
.wx-simple{font-size:14px;color:#94a3b8}
.wx-temp{font-size:28px;font-weight:700;color:#f8fafc;margin-right:8px}
.wx-hilo{color:#94a3b8;margin-right:12px}
.wx-rain{color:#38bdf8}
.quote-card{border-left:4px solid #f59e0b}
.quote-icon{font-size:28px;color:#f59e0b;line-height:1;float:left;margin-right:8px}
.quote-text{font-size:18px;font-style:italic;color:#f1f5f9;margin-bottom:4px;line-height:1.35}
.quote-author{font-size:13px;color:#94a3b8;text-align:right}
.chart-card svg{width:100%;height:auto}
.action-grid{display:flex;gap:14px}
.action-col{flex:1;min-width:0}
.action-row{padding:6px 10px 6px 8px;margin:4px 0;font-size:13px;line-height:1.3;border-radius:4px;background:#1e293b}
.week-grid{display:flex;gap:6px}
.wday{flex:1;min-width:0;background:#1e293b;border-radius:8px;padding:8px 6px}
.wday-today{background:#2d3a4f;border:1px solid #f59e0b}
.wday-head{font-size:11px;font-weight:700;color:#94a3b8;text-transform:uppercase;text-align:center;margin-bottom:6px}
.wdate{display:block;font-size:20px;font-weight:800;color:#e2e8f0;margin-top:2px}
.wday-today .wday-head{color:#f59e0b}
.wevent{font-size:10px;line-height:1.25;padding:3px 2px;border-bottom:1px solid #475569;margin-bottom:2px}
.wevent:last-child{border-bottom:none}
.wtime{font-weight:700;color:#38bdf8;display:block;font-size:9px}
.wloc{color:#64748b;font-size:9px}
.ca-row{padding:4px 0;font-size:13px;border-bottom:1px solid #475569}
.ca-row b{color:#f59e0b}
.footer{color:#64748b;font-size:12px;margin-top:12px;text-align:center}
"""

html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="{REFRESH_MINUTES*60}">
<title>Superior Dashboard</title>
<style>{CSS}</style>
</head><body>
<div class="header">
  <div>
    <div class="clock"><span id="c">{NOW.strftime("%I:%M").lstrip("0")}<small>{NOW.strftime("%p")}</small></span></div>
    <div class="date-line">{date_line}</div>
  </div>
  <div class="weather">{wx_html}</div>
  <div>
    <div class="date-line">{LOCATION}</div>
  </div>
</div>

<div class="card">
  <h2>WEEKLY CALENDAR</h2>
  {meeting_html}
</div>

<div class="card chart-card">
  <h2>INCIDENT TREND</h2>
  {chart_svg}
</div>

<div class="card quote-card">
  <span class="quote-icon">"</span>
  <div class="quote-text">{q["q"]}</div>
  <div class="quote-author">- {q["a"]}</div>
</div>

<div class="card">
  <h2>ACTION BOARD</h2>
  <div class="action-grid">
    <div class="action-col"><h3 style="color:#f59e0b">THIS WEEK</h3>{action_list(THIS_WEEK,"#f59e0b")}</div>
    <div class="action-col"><h3 style="color:#3b82f6">THIS MONTH</h3>{action_list(THIS_MONTH,"#3b82f6")}</div>
    <div class="action-col"><h3 style="color:#8b5cf6">THIS QUARTER</h3>{action_list(THIS_QUARTER,"#8b5cf6")}</div>
  </div>
</div>

<div class="card">
  <h2>CORRECTIVE ACTIONS</h2>
  {ca_html}
</div>

<div class="footer">Built {NOW.strftime("%b %d, %I:%M %p")} ET · refreshes every {REFRESH_MINUTES} min · {HOME_LABEL}</div>

<script>
(function(){{
  function t(){{
    var e=document.getElementById("c");if(!e)return;
    var n=new Date(),h=n.getHours(),m=n.getMinutes(),a=h>=12?"PM":"AM";
    h=h%12||12;e.innerHTML=h+":"+(m<10?"0":"")+m+"<small>"+a+"</small>";
  }}
  t();setInterval(t,1000);
}})();
</script>
</body></html>
"""

with open(OUTPUT_FILE, "w") as f:
    f.write(html)
print(f"Built: {OUTPUT_FILE}")