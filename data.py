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

# INCIDENT MONTHLY COUNTS — Edit these
INCIDENTS_2026 = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,"Jun":0,"Jul":0,"Aug":0,"Sep":0,"Oct":0,"Nov":0,"Dec":0}
INCIDENTS_2025 = {"Jan":0,"Feb":0,"Mar":0,"Apr":0,"May":0,"Jun":0,"Jul":0,"Aug":0,"Sep":0,"Oct":0,"Nov":0,"Dec":0}
INDUSTRY_BENCHMARK = 3.5

# DAILY QUOTES — one per day, rotates
LEADERSHIP_QUOTES = [
    {"q":"The first responsibility of a leader is to define reality. The last is to say thank you.","a":"Max DePree"},
    {"q":"Leadership is not about being in charge. It is about taking care of those in your charge.","a":"Simon Sinek"},
    {"q":"People don\'t care how much you know until they know how much you care.","a":"Theodore Roosevelt"},
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

# CORRECTIVE ACTIONS
CORRECTIVE_ACTIONS = [
    {"title":"Complete 2026 incident review & RCA","status":"in-progress","days":2,"owner":"Justin"},
    {"title":"Rebuild Oven Operator JSA — ownership & review structure","status":"open","days":1,"owner":"Justin"},
    {"title":"Build training matrix per role","status":"open","days":1,"owner":"Justin"},
    {"title":"Review LOTO procedures for oven area","status":"open","days":0,"owner":"Justin"},
]

# MEETINGS — Manual entries (auto-sync via ICS + GitHub Actions rebuild coming)
MEETINGS = [
    {"date":"2026-10-27","time":"7:00 AM","title":"Toolbox Talk — Day shift","loc":"Floor"},
    {"date":"2026-10-27","time":"8:30 AM","title":"Safety walk with Greg","loc":"Plant"},
    {"date":"2026-10-28","time":"7:00 AM","title":"Toolbox Talk — Day shift","loc":"Floor"},
]

# SETTINGS
# ICS Calendar Feed (Outlook auto-sync)
# The dashboard pulls this URL on every rebuild to get live meetings
ICS_URL = "https://outlook.office365.com/owa/calendar/816390b4b0e44f5080019c66609de8d9@superiorcompositesco.com/9c00023c0c804ce085d37a48ff4fbb3a10100425901936832656/calendar.ics"

# SETTINGS
REFRESH_MINUTES = 5
