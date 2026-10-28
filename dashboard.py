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
is_pause = q.get("a","").lower() == "pause & think"
quote_icon = "💭" if is_pause else '"'
quote_cls = " quote-card-pause" if is_pause else ""
quote_label = f'<div class="muted" style="font-size:11px;margin-bottom:4px;letter-spacing:1px;text-transform:uppercase;color:#ffcc00">Pause &amp; Think</div>' if is_pause else ""

# Incident chart SVG
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
max_val = max(list(INCIDENTS_2026.values()) + list(INCIDENTS_2025.values()) + [5])
# Build line chart — Power BI style
# Points + lines for 2026, 2025, and a flat benchmark line
def build_line_chart():
    # CUMULATIVE YTD — Power BI style. Each month shows the running total
    # of recordables so far that year. The slope tells you if you're on
    # pace to beat the industry benchmark or not.
    w, h = 520, 200
    pad = {"t": 25, "r": 30, "b": 30, "l": 35}
    cw = w - pad["l"] - pad["r"]
    ch = h - pad["t"] - pad["b"]
    
    # Compute cumulative YTD values
    cum26 = []
    cum25 = []
    total26 = 0
    total25 = 0
    for i, m in enumerate(months):
        total26 += INCIDENTS_2026[m] or 0
        total25 += INCIDENTS_2025[m] or 0
        cum26.append(total26)
        cum25.append(total25)
    
    # Benchmark line = industry benchmark (3.3/yr) * months elapsed
    all_vals = cum26 + cum25 + [INDUSTRY_BENCHMARK]
    max_v = max(all_vals) if all_vals else 5
    max_v = max(max_v, 5)
    
    def xpos(i):
        return pad["l"] + (i / 11) * cw
    def ypos(v):
        return pad["t"] + ch - (v / (max_v * 1.15)) * ch
    
    # Grid lines
    grid = ""
    step = max(1, int(max_v * 1.15 / 6))
    for g in range(0, int(max_v * 1.15) + step, step):
        gy = ypos(g)
        grid += f'<line x1="{pad["l"]}" y1="{gy}" x2="{w - pad["r"]}" y2="{gy}" stroke="#475569" stroke-width="0.5"/>'
        grid += f'<text x="{pad["l"] - 4}" y="{gy + 3}" font-size="8" fill="#64748b" text-anchor="end">{g}</text>'
    
    # 2025 cumulative line (dashed blue)
    pts25 = []
    for i, m in enumerate(months):
        pts25.append(f'{xpos(i)},{ypos(cum25[i])}')
    line25 = f'<polyline points="{" ".join(pts25)}" fill="none" stroke="#3b82f6" stroke-width="2" stroke-dasharray="4,3" opacity="0.7"/>'
    for i, m in enumerate(months):
        if cum25[i] > 0:
            line25 += f'<circle cx="{xpos(i)}" cy="{ypos(cum25[i])}" r="3" fill="#3b82f6" stroke="#1e293b" stroke-width="1"/>'
    
    # 2026 cumulative line (solid amber)
    pts26 = []
    for i, m in enumerate(months):
        pts26.append(f'{xpos(i)},{ypos(cum26[i])}')
    line26 = f'<polyline points="{" ".join(pts26)}" fill="none" stroke="#f59e0b" stroke-width="2.5"/>'
    for i, m in enumerate(months):
        if cum26[i] > 0:
            line26 += f'<circle cx="{xpos(i)}" cy="{ypos(cum26[i])}" r="3.5" fill="#f59e0b" stroke="#1e293b" stroke-width="1"/>'
    
    # Industry benchmark cumulative line (red dashed)
    bench_annual = INDUSTRY_BENCHMARK
    bench_by_month = bench_annual  # This is the annual benchmark, shown as flat line
    by = ypos(bench_annual)
    bench_line = f'<line x1="{pad["l"]}" y1="{by}" x2="{w - pad["r"]}" y2="{by}" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="5,3"/>'
    bench_label = f'<text x="{w - pad["r"]}" y="{by - 4}" font-size="9" fill="#ef4444" text-anchor="end">Benchmark {bench_annual}/yr</text>'
    
    # Month labels
    month_labels = ""
    for i, m in enumerate(months):
        month_labels += f'<text x="{xpos(i)}" y="{h - 5}" font-size="8" fill="#64748b" text-anchor="middle">{m[:3]}</text>'
    
    # Y-axis label
    y_label = '<text x="12" y="15" font-size="9" fill="#94a3b8">YTD</text>'
    
    # Legend
    legend = f'<rect x="{pad["l"]}" y="6" width="10" height="3" fill="#f59e0b"/><text x="{pad["l"] + 14}" y="10" font-size="8" fill="#94a3b8">2026 YTD</text>'
    legend += f'<rect x="{pad["l"] + 80}" y="6" width="10" height="3" fill="#3b82f6"/><text x="{pad["l"] + 94}" y="10" font-size="8" fill="#94a3b8">2025 YTD</text>'
    legend += f'<line x1="{pad["l"] + 160}" y1="7" x2="{pad["l"] + 170}" y2="7" stroke="#ef4444" stroke-width="1.5"/><text x="{pad["l"] + 174}" y="10" font-size="8" fill="#94a3b8">Benchmark</text>'
    
    # Current YTD annotation
    current_ytd = cum26[-1]  # Last month's cumulative (Oct = 4)
    ytd_label = f'<text x="{xpos(9)}" y="{ypos(cum26[9]) - 8}" font-size="10" fill="#f59e0b" font-weight="bold" text-anchor="middle">YTD: {current_ytd}</text>' if current_ytd > 0 else ""
    
    svg = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{grid}{line25}{line26}{bench_line}{bench_label}{y_label}{month_labels}{legend}{ytd_label}</svg>'
    return svg

chart_svg = build_line_chart()

# Action board
def action_list(items, color):
    return "\n".join(f'<div class="action-row" style="border-left:3px solid {color}"><span>{i}</span></div>' for i in items)

# Meetings - manual from MEETINGS
def build_week_calendar(meetings):
    days_html = ""
    # Special day emoji map (month-day -> emoji)
    special_days = {
            (10, 31): "🎃",  # Halloween
            (12, 25): "🎄",  # Christmas
            (1, 1): "🎆",    # New Year
        }
    for offset in range(7):
        day = TODAY + timedelta(days=offset)
        iso = day.isoformat()
        label = "Today" if offset == 0 else day.strftime("%a")
        date_num = day.day
        day_events = sorted([m for m in meetings if m["date"] == iso], key=lambda m: (0 if m["time"] == "All Day" or not m["time"] else 1, m["time"] if m["time"] not in ("All Day", "") else ""), reverse=True)
        events_html = ""
        for m in day_events:
            loc = f' <span class="wloc">({m["loc"]})</span>' if m.get("loc") else ""
            if m["time"] == "All Day" or not m["time"]:
                events_html += f'<div class="wevent all-day"><span class="wtime-all">ALL DAY</span> {m["title"]}</div>'
            else:
                events_html += f'<div class="wevent"><span class="wtime">{m["time"]}</span> {m["title"]}{loc}</div>'
        if not events_html:
            events_html = '<div class="wevent empty">--</div>'
        today_class = ' wday-today' if offset == 0 else ''
        # Check for special day icon
        icon = special_days.get((day.month, day.day), "")
        icon_html = f'<span class="day-icon">{icon}</span>' if icon else ""
        days_html += f'<div class="wday{today_class}"><div class="wday-head">{label}{icon_html}<span class="wdate">{date_num}</span></div>{events_html}</div>'
    return f'<div class="week-grid">{days_html}</div>'

# Top priorities
prio_html = ""
for p in TOP_PRIORITIES:
    icon = "\u2611" if p["status"] == "done" else "\u25a1"
    cls = " prio-done" if p["status"] == "done" else ""
    prio_html += f'<div class="prio-row{cls}"><span class="prio-icon">{icon}</span> {p["task"]}</div>'
if not prio_html:
    prio_html = '<div class="empty">No priorities set. Text me!</div>'

meeting_html = build_week_calendar(MEETINGS)

# Corrective actions
ca_rows = []
for ca in CORRECTIVE_ACTIONS:
    icon = {"open":"\U0001f534","in-progress":"\U0001f7e1","closed":"\U0001f7e2"}.get(ca["status"], "\u26aa")
    ca_rows.append(f'<div class="ca-row">{icon} <b>{ca["owner"]}</b> {ca["title"]} <span class="muted">({ca["days"]}d)</span></div>')
ca_html = "\n".join(ca_rows) if ca_rows else '<div class="empty">No open items</div>'

# Roadmap HTML
roadmap_html = ""
for phase in ROADMAP:
    items_html = "".join(f'<li>{item}</li>' for item in phase["items"])
    roadmap_html += f'<div class="rm-phase"><div class="rm-period">{phase["period"]}</div><ul class="rm-items">{items_html}</ul></div>'

# Build HTML
date_line = NOW.strftime("%A").upper() + " " + NOW.strftime("%B").upper() + " " + str(NOW.day)

CSS = """*{box-sizing:border-box;margin:0;padding:0}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
body{background:#0a0a1a;color:#00ffcc;font-family:'Orbitron',monospace,sans-serif;font-size:15px;padding:20px 24px;position:relative;overflow-x:hidden;text-shadow:0 0 5px rgba(0,255,204,0.3)}
body::after{content:"";position:fixed;top:0;left:0;width:100%;height:100%;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,204,0.03) 2px,rgba(0,255,204,0.03) 4px);pointer-events:none;z-index:9999}
.card{background:rgba(10,5,30,0.88);border:1px solid #ff00ff;border-radius:8px;padding:14px 18px;margin-bottom:14px;position:relative;z-index:1;box-shadow:0 0 12px rgba(255,0,255,0.2),inset 0 0 20px rgba(0,255,204,0.05)}
.card:hover{box-shadow:0 0 25px rgba(255,0,255,0.4),0 0 15px rgba(0,255,204,0.2),inset 0 0 30px rgba(0,255,204,0.1);border-color:#00ffcc}
h2{font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#ff00ff;margin-bottom:10px;font-weight:700;text-shadow:0 0 10px rgba(255,0,255,0.5)}
h3{font-size:13px;font-weight:700;margin-bottom:8px;letter-spacing:2px;text-shadow:0 0 8px currentColor}
.empty{color:#6633cc;font-size:13px;margin:4px 0}
.muted{color:#6633cc;font-size:11px}
.header{display:flex;align-items:flex-start;margin-bottom:16px;border-bottom:2px solid #ff00ff;padding-bottom:12px;box-shadow:0 4px 12px rgba(255,0,255,0.15);background:linear-gradient(90deg,transparent,rgba(255,0,255,0.05),transparent)}
.header>div:nth-child(1){width:40%}
.header>div:nth-child(2){width:35%}
.header>div:nth-child(3){width:25%;text-align:right}
.clock{font-size:52px;font-weight:900;letter-spacing:-1.5px;color:#00ffcc;text-shadow:0 0 15px rgba(0,255,204,0.6),0 0 30px rgba(0,255,204,0.3),0 0 45px rgba(0,255,204,0.1)}
.clock small{font-size:24px;font-weight:700;margin-left:4px;color:#ff00ff;text-shadow:0 0 10px rgba(255,0,255,0.5),0 0 20px rgba(255,0,255,0.2)}
.date-line{font-size:14px;font-weight:700;letter-spacing:2px;color:#ffcc00;text-shadow:0 0 8px rgba(255,204,0,0.4)}
.wx-simple{font-size:13px;color:#00ffcc}
.wx-temp{font-size:28px;font-weight:700;color:#ffcc00;margin-right:8px;text-shadow:0 0 10px rgba(255,204,0,0.4)}
.wx-hilo{color:#00ffcc;margin-right:12px}
.wx-rain{color:#0066ff;text-shadow:0 0 8px rgba(0,102,255,0.4)}
.header-logo{height:36px;opacity:0.6;margin-bottom:4px;filter:drop-shadow(0 0 8px #ff00ff) drop-shadow(0 0 3px #00ffcc)}
.quote-card{border-left:4px solid #ffcc00;background:linear-gradient(135deg,rgba(10,5,30,0.88) 60%,rgba(255,204,0,0.05))}
.quote-card-pause{border-left:4px solid #00ffcc;background:linear-gradient(135deg,rgba(10,5,30,0.88) 55%,rgba(0,255,204,0.08));box-shadow:0 0 18px rgba(0,255,204,0.15)}
.quote-icon{font-size:28px;color:#ffcc00;line-height:1;float:left;margin-right:8px;text-shadow:0 0 10px rgba(255,204,0,0.6)}
.quote-text{font-size:17px;font-style:italic;color:#00ffcc;margin-bottom:4px;line-height:1.35;text-shadow:0 0 8px rgba(0,255,204,0.2)}
.quote-author{font-size:12px;color:#ff00ff;text-align:right}
.chart-card svg{width:100%;height:auto}
.action-grid{display:flex;gap:12px}
.action-col{flex:1;min-width:0}
.action-row{padding:5px 8px;margin:3px 0;font-size:12px;line-height:1.3;border-radius:4px;background:rgba(0,0,0,0.4);border:1px solid rgba(255,0,255,0.15)}
.action-row:hover{border-color:#ffcc00;box-shadow:0 0 10px rgba(255,204,0,0.2)}
.week-grid{display:flex;gap:5px}
.wday{flex:1;min-width:0;background:rgba(0,0,0,0.4);border-radius:6px;padding:6px 4px;border:1px solid rgba(255,0,255,0.1)}
.wday-today{background:rgba(255,0,255,0.08);border:1px solid #ff00ff;box-shadow:0 0 12px rgba(255,0,255,0.2),inset 0 0 20px rgba(0,255,204,0.05)}
.wday-head{font-size:10px;font-weight:700;color:#0066ff;text-transform:uppercase;text-align:center;margin-bottom:5px;text-shadow:0 0 5px rgba(0,102,255,0.3)}
.day-icon{display:block;font-size:22px;line-height:1;margin-bottom:2px}
.wdate{display:block;font-size:18px;font-weight:900;color:#ffcc00;margin-top:2px;text-shadow:0 0 8px rgba(255,204,0,0.3)}
.wday-today .wday-head{color:#ff00ff}
.wevent{font-size:11px;line-height:1.3;padding:3px 2px;border-bottom:1px solid rgba(255,0,255,0.1);margin-bottom:2px}
.wevent:last-child{border-bottom:none}
.wtime{font-weight:700;color:#00ffff;display:block;font-size:8px;text-shadow:0 0 5px rgba(0,255,255,0.4)}
.wtime-all{font-weight:700;color:#ff00ff;display:block;font-size:7px;text-transform:uppercase;letter-spacing:1px}
.wevent.all-day{background:rgba(255,0,255,0.1);border-left:2px solid #ff00ff;padding:3px;margin-bottom:2px;border-radius:2px;font-size:9px}
.wloc{color:#6633cc;font-size:8px}
.prio-row{padding:4px 8px;margin:2px 0;font-size:12px;background:rgba(0,0,0,0.4);border-radius:4px;border-left:3px solid #ff00ff}
.prio-row.prio-done{opacity:0.4;border-left-color:#0066ff}
.prio-icon{margin-right:6px;font-size:13px}
.ca-row{padding:3px 0;font-size:12px;border-bottom:1px solid rgba(255,0,255,0.1)}
.ca-row b{color:#00ffcc}
.roadmap-grid{display:flex;gap:8px;flex-wrap:wrap}
.rm-phase{background:rgba(0,0,0,0.4);border-radius:6px;padding:8px 10px;flex:1;min-width:130px;border:1px solid rgba(255,0,255,0.1)}
.rm-period{font-size:10px;font-weight:700;color:#ff00ff;text-transform:uppercase;letter-spacing:2px;margin-bottom:5px;border-bottom:1px solid rgba(255,0,255,0.2);padding-bottom:3px;text-shadow:0 0 5px rgba(255,0,255,0.4)}
.rm-items{list-style:none;padding:0;margin:0}
.rm-items li{font-size:11px;padding:2px 0;color:#00ffcc;line-height:1.3}
.rm-items li:before{content:"\25B8";color:#ffcc00;margin-right:4px;text-shadow:0 0 5px rgba(255,204,0,0.4)}
.footer{color:#6633cc;font-size:11px;margin-top:12px;text-align:center}
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
  <div style="text-align:right">
    <img src="https://shcomposites.com/wp-content/uploads/superior-huntingdon-composites-265.jpg" class="header-logo" alt="SC">
    <div class="date-line">{LOCATION}</div>
  </div>
</div>

<div class="card">
  <h2>TOP PRIORITIES</h2>
  {prio_html}
</div>

<div class="card">
  <h2>WEEKLY CALENDAR</h2>
  {meeting_html}
</div>

<div class="card quote-card{quote_cls}">
  <span class="quote-icon">{quote_icon}</span>
  {quote_label}
  <div class="quote-text">{q["q"]}</div>
  <div class="quote-author">- {q["a"]}</div>
</div>

<div class="card">
  <h2>60-DAY ROADMAP</h2>
  <div class="roadmap-grid">
{roadmap_html}
  </div>
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