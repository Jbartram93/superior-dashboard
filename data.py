"""Superior EHS Manager Dashboard — Data file.
Edit here. Never touch dashboard.py.
"""
from datetime import date, timedelta
TODAY = date.today()
def d(days_from_today):
    return (TODAY + timedelta(days=days_from_today)).isoformat()

# Company
COMPANY_NAME = "Superior Huntingdon Composites"
ROLE_TITLE = "EHS Manager"
LOCATION = "Vanceburg, KY"
HOME_COORDS = (38.386, -82.604)
HOME_LABEL = "Vanceburg"

# NAICS code for industry benchmark
NAICS_CODE = "32619900"

# INCIDENT MONTHLY COUNTS — Edit these
INCIDENTS_2026 = {
    "Jan": 1,  # Aaron Smith - loss time
    "Feb": 0,
    "Mar": 0,
    "Apr": 0,
    "May": 1,  # Breanna Pauley - recordable
    "Jun": 0,
    "Jul": 0,
    "Aug": 0,
    "Sep": 1,  # David Jordan - lost time
    "Oct": 1,  # Drake Duncan - loss time
    "Nov": 0,
    "Dec": 0,
}
INCIDENTS_2025 = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,"Jun":0,"Jul":0,"Aug":0,"Sep":0,"Oct":0,"Nov":0,"Dec":0}
INDUSTRY_BENCHMARK = 3.3  # NAICS 32619900 — Other Plastics Product Manufacturing
# 2026 YTD Recordable Incidents (from Safety Alert list): 4
# Jan: Aaron Smith (loss time), May: Breanna Pauley (recordable),
# Sep: David Jordan (lost time), Oct: Drake Duncan (loss time)
# UPDATE HOURS when you know 2026 YTD hours worked for TRIR calculation
# NOTE: BLS data could not be directly retrieved (site blocking). This is a
# conservative estimate based on known rates for related plastics NAICS codes
# (326111=2.9, 326121=3.1, all mfg=2.7). Verify exact figure from loss runs.

# DAILY QUOTES — one per day, rotates
LEADERSHIP_QUOTES = [
    {"q":"The first responsibility of a leader is to define reality. The last is to say thank you.","a":"Max DePree"},
    {"q":"Leadership is not about being in charge. It is about taking care of those in your charge.","a":"Simon Sinek"},
    {"q":"People don't care how much you know until they know how much you care.","a":"Theodore Roosevelt"},
    {"q":"Trust is built when someone is vulnerable and not taken advantage of.","a":"Bob Vanourek"},
    {"q":"Leaders eat last.","a":"Simon Sinek"},
    {"q":"Every incident is a failure of leadership somewhere up the chain.","a":"Unknown"},
    {"q":"A safety program is not a binder on a shelf. It is a conversation on the floor.","a":"Justin Bartram"},
    {"q":"The single biggest way to impact an organization is to focus on leadership development.","a":"John Maxwell"},
    {"q":"A culture of safety is created by the people, not by the rulebook.","a":"Unknown"},
    {"q":"Before you are a leader, success is all about growing yourself. When you become a leader, success is all about growing others.","a":"Jack Welch"},
    {"q":"Your most important asset is not in your balance sheet — it is your people.","a":"Jim Sinegal"},
    {"q":"Safety is not a priority — it is a value. Priorities change. Values do not.","a":"Justin Bartram"},
    {"q":"Management is about arranging and telling. Leadership is about nurturing and enhancing.","a":"Tom Peters"},
    {"q":"The best way to find yourself is to lose yourself in the service of others.","a":"Mahatma Gandhi"},
    {"q":"If you want to build a culture of safety, you must first build a culture of trust.","a":"Unknown"},
]

# ACTIONS
THIS_WEEK = [
    "Attend toolbox talks daily (7 AM)",
    "Review 2026 incidents — top 3 patterns",
    "Shadow oven operator training — bring JSAs",
    "Meet each shift supervisor informally",
    "Walk the floor 30+ min daily",
]
THIS_MONTH = [
    "JSA audit & rewrite kickoff meetings",
    "Build training matrix / identify gaps",
    "Take over incident reporting & investigation",
    "Present Month 1 observations to leadership",
    "Establish weekly safety walk cadence",
]
THIS_QUARTER = [
    "Confined space trainer certification",
    "LOTO program review & improvement",
    "HazCom program — binder room first",
    "Expand glove program across jobs",
    "Build automated EHS dashboard",
]

# GREG'S 60-DAY ROADMAP — from plant manager's handwritten plan
ROADMAP = [
    {"period": "Week 1-2", "items": [
        "Orientation & floor time",
        "Watch trainers with JSAs",
        "Take over incident reporting",
        "Lead safety walks",
        "Review 2026 incidents",
        "Toolbox talks — daily",
    ]},
    {"period": "Week 2-4", "items": [
        "Learn to teach orientation",
        "Engage employees on floor",
        "Deep dive training gaps",
    ]},
    {"period": "Month 2", "items": [
        "JSA audit team meetings",
        "Present observations & recommendations",
        "Build incident pattern analysis",
    ]},
    {"period": "Longer-term", "items": [
        "Confined Space trainer cert",
        "LOTO trainer cert",
        "Emergency Response trainer cert",
        "CPR / First Aid trainer cert",
        "OSHA-10 trainer cert",
        "Start HazCom program",
    ]},
]
CORRECTIVE_ACTIONS = [
    {"title":"Complete 2026 incident review & RCA","status":"in-progress","days":2,"owner":"Justin"},
    {"title":"Rebuild Oven Operator JSA — ownership & review structure","status":"open","days":1,"owner":"Justin"},
    {"title":"Build training matrix per role","status":"open","days":1,"owner":"Justin"},
    {"title":"Review LOTO procedures for oven area","status":"open","days":0,"owner":"Justin"},
]

# MEETINGS — Auto-populated (recurring) + manual. Text me to add/edit.
MEETINGS = [
    {"date": "2026-10-28", "time": "12:00 PM", "title": "Chili Cookout", "loc": "Break Room"},
    {"date": "2026-10-28", "time": "9:00 AM", "title": "SCC Production Call (Teams)", "loc": "Teams"},
    {"date": "2026-10-29", "time": "10:30 AM", "title": "Safety Walkthrough"},
    {"date": "2026-10-29", "time": "All Day", "title": "Board of Directors Site Visit"},
    {"date": "2026-10-30", "time": "1:00 PM", "title": "Weekly Planning Meeting", "loc": "Conf Room"},
    {"date": "2026-10-30", "time": "1:30 PM", "title": "Monthly Maintenance Meeting", "loc": "Conf Room"},
    {"date": "2026-10-30", "time": "2:30 PM", "title": "Projects Meeting", "loc": "Conf Room"},
    {"date": "2026-10-31", "time": "", "title": "Trick or Treat"},
]

# SETTINGS
REFRESH_MINUTES = 30  # frame refreshes page every 30 min