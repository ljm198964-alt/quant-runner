from __future__ import annotations

import json
import math
import re
from pathlib import Path

POLICY_VERSION = "M1_SELECTION_20261006_TOP_TIER_NATIONAL_REVERSE_V3"
SCAN_MIN_LEAD_HOURS = 4.0
SCAN_MAX_LEAD_HOURS = 36.0
PREFERRED_MIN_LEAD_HOURS = 18.0
PREFERRED_MAX_LEAD_HOURS = 30.0

BASE_EV = {"HIGH": 0.020, "MEDIUM": 0.040}
BASE_EDGE = {"HIGH": 0.015, "MEDIUM": 0.030}

EXPLICIT_ALLOWED = (
    re.compile(r"^UEFA Nations League", re.I),
    re.compile(r"^International Match$", re.I),
    re.compile(r"^Gulf Cup$", re.I),
)

# Formal M1 V2 domestic scope: men's senior TOP TIER only.
# Second tiers are intentionally excluded even where the research/student scope still knows them.
TOP_TIER_IN = (
    re.compile(r"^England Premier League$", re.I),
    re.compile(r"^Germany Bundesliga I$", re.I),
    re.compile(r"^France Ligue 1$", re.I),
    re.compile(r"^Italy Serie A$", re.I),
    re.compile(r"^Spain (?:La Liga|Primera Division)$", re.I),
    re.compile(r"^Netherlands Eredivisie$", re.I),
    re.compile(r"^Belgium First Division A$", re.I),
    re.compile(r"^Portugal (?:Primeira Liga|Liga Portugal)$", re.I),
    re.compile(r"^Austria Bundesliga$", re.I),
    re.compile(r"^Switzerland Super League$", re.I),
    re.compile(r"^Scotland Premiership$", re.I),
    re.compile(r"^Greece Super League(?: 1)?$", re.I),
    re.compile(r"^(?:Turkey|Türkiye) Super Lig$", re.I),
    re.compile(r"^Denmark Superliga(?:en)?$", re.I),
    re.compile(r"^Sweden Allsvenskan$", re.I),
    re.compile(r"^Norway Eliteserien$", re.I),
    re.compile(r"^Finland Veikkausliiga$", re.I),
    re.compile(r"^(?:Republic of )?Ireland Premier Division$", re.I),
    re.compile(r"^Northern Ireland (?:Premiership|Premier)$", re.I),
    re.compile(r"^Iceland (?:Besta deild|Premier League)$", re.I),
    re.compile(r"^Czechia (?:First League|1\. Liga)$", re.I),
    re.compile(r"^Slovakia (?:Super Liga|1\. Liga)$", re.I),
    re.compile(r"^Poland Ekstraklasa$", re.I),
    re.compile(r"^Croatia HNL$", re.I),
    re.compile(r"^Serbia Super Liga$", re.I),
    re.compile(r"^Romania (?:Liga I|Liga 1|SuperLiga)$", re.I),
    re.compile(r"^Hungary NB I$", re.I),
    re.compile(r"^Slovenia (?:PrvaLiga|Prva Liga)$", re.I),
    re.compile(r"^Bulgaria First League$", re.I),
    re.compile(r"^Cyprus (?:First Division|Division 1)$", re.I),
    re.compile(r"^Israel Premier League$", re.I),
    re.compile(r"^Ukraine (?:Premier League|Vyscha Liga)$", re.I),
    re.compile(r"^Belarus Premier League$", re.I),
    re.compile(r"^Kazakhstan Premier League$", re.I),
    re.compile(r"^Georgia Erovnuli Liga$", re.I),
    re.compile(r"^Armenia Premier League$", re.I),
    re.compile(r"^Azerbaijan Premier League$", re.I),
    re.compile(r"^Estonia Meistriliiga$", re.I),
    re.compile(r"^Latvia Virsliga$", re.I),
    re.compile(r"^Lithuania A Lyga$", re.I),
    re.compile(r"^Japan J(?:1[ -]League|-League| League)$", re.I),
    re.compile(r"^South Korea K[- ]?League 1$", re.I),
    re.compile(r"^China Super League$", re.I),
    re.compile(r"^Saudi Arabia Pro League$", re.I),
    re.compile(r"^Egypt Premier League$", re.I),
    re.compile(r"^Wales (?:Premier League|Cymru Premier)$", re.I),
    re.compile(r"^Albania Superliga$", re.I),
    re.compile(r"^Andorra Premier Division$", re.I),
    re.compile(r"^Faroe Islands Premier League$", re.I),
    re.compile(r"^Kosovo Superliga$", re.I),
    re.compile(r"^Malta Premier League$", re.I),
    re.compile(r"^Montenegro Prva Liga$", re.I),
    re.compile(r"^North Macedonia First League$", re.I),
    re.compile(r"^Bosnia & Herzegovina Premier League$", re.I),
    re.compile(r"^Colombia Primera A$", re.I),
    re.compile(r"^Argentina Liga Profesional$", re.I),
    re.compile(r"^Brazil Serie A$", re.I),
    re.compile(r"^USA MLS$", re.I),
    re.compile(r"^Mexico Liga MX$", re.I),
)

# Explicit second-tier guard. This is intentionally redundant with the top-tier
# whitelist so future scope edits cannot silently re-admit second divisions.
SECOND_TIER = re.compile(
    r"^(?:"
    r"England Championship|"
    r"Germany (?:Bundesliga II|2\. Bundesliga)|"
    r"France Ligue 2|Italy Serie B|Spain Segunda(?: Division)?|"
    r"Netherlands Eerste Divisie|Belgium (?:First Division B|Challenger Pro League)|"
    r"Portugal (?:Liga Portugal 2|Segunda Liga)|Austria 2\. Liga|"
    r"Switzerland Challenge League|Scotland Championship|Greece Super League 2|"
    r"(?:Turkey|Türkiye) 1\.? Lig|Denmark (?:Division 1|1st Division)|"
    r"Sweden Superettan|Norway Division 1|Finland Ykkosliiga|"
    r"(?:Republic of )?Ireland First Division|Northern Ireland Championship|"
    r"Iceland 1\. deild|Czechia 2\. Liga|Slovakia 2\. Liga|Poland I Liga|"
    r"Croatia 1\. ?NL|Serbia Prva Liga|Romania (?:Liga II|Liga 2)|Hungary NB II|"
    r"Slovenia 2\. SNL|Bosnia & Herzegovina 1st League|Bulgaria Second League|"
    r"Cyprus (?:Second Division|Division 2)|Israel Leumit Liga|"
    r"Ukraine (?:First League|Persha Liga)|Belarus First League|Kazakhstan First Division|"
    r"Georgia Erovnuli Liga 2|Armenia First League|Azerbaijan First Division|"
    r"Estonia Esiliiga|Latvia 1\. Liga|Lithuania (?:I Lyga|1 Lyga)|"
    r"Japan J2(?:-| )League|South Korea K[- ]?League 2|China League One|"
    r"Saudi Arabia Division 1|Egypt Division 2|Wales (?:Cymru North|Cymru South|Championship North|Championship South)|"
    r"Albania First Division|Andorra Second Division|Faroe Islands (?:1\. deild|1st Division)|"
    r"Kosovo (?:Division 1|First League)|Malta Challenge League|"
    r"Montenegro (?:Druga Liga|Second League)|North Macedonia Second League"
    r")$",
    re.I,
)

HARD_EXCLUDE = re.compile(
    r"women|\bw\b|u\s*1[789]|u\s*2[013]|youth|reserve|academy|"
    r"esoccer|amateur|regional|university|college|"
    r"club friendl|friendly club|"
    r"3\.?\s*liga|liga\s*3|third division|third league|3rd division|"
    r"serie\s*[cd]\b|league\s*(one|two)\b|regionalliga|oberliga|"
    r"primera federaci[oó]n|segunda\s*b\b|tercera|championnat national\b",
    re.I,
)

CUP_OR_INTL = re.compile(
    r"\bcup\b|champions league|europa league|conference league|"
    r"qualif|world cup|asian games|afc |caf |concacaf|conmebol|"
    r"international|nations league|friendl",
    re.I,
)

def load_scope(path: str = "M1赛事范围_当前.json") -> dict:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def scope_status(league: str, league_id: str = "", home: str = "", away: str = "") -> dict:
    league = str(league or "").strip()
    text = f"{league} {home} {away}"
    for pat in EXPLICIT_ALLOWED:
        if pat.search(league):
            return {"status": "IN", "reason": "user_explicit_international"}
    if str(league_id) == "670":
        return {"status": "IN", "reason": "user_explicit_gulf_cup"}
    if HARD_EXCLUDE.search(text):
        return {"status": "OUT", "reason": "hard_exclusion"}
    if CUP_OR_INTL.search(league):
        return {"status": "OUT", "reason": "unapproved_cup_or_international"}
    if SECOND_TIER.search(league):
        return {"status": "OUT", "reason": "all_second_tiers_disabled_by_user"}
    for pat in TOP_TIER_IN:
        if pat.search(league):
            return {"status": "IN", "reason": "approved_top_tier"}
    return {"status": "OUT", "reason": "not_in_approved_top_tier_scope"}

def adverse_line_move(market: str, side: str, opening_line: float | None, current_line: float | None) -> float:
    if opening_line is None or current_line is None:
        return 0.0
    o, c = float(opening_line), float(current_line)
    if market == "全场让球":
        v = (o - c) if side == "HOME" else (c - o)
    elif market == "全场大小球":
        v = (c - o) if side == "OVER" else (o - c)
    else:
        return 0.0
    return max(0.0, v)

def decision_thresholds(quality: str, state_signal: str, lead_hours: float, adverse_move: float) -> dict:
    quality = str(quality or "").upper()
    if quality not in BASE_EV:
        return {"eligible_quality": False, "required_ev": None, "required_edge": None}
    ev = BASE_EV[quality]
    edge = BASE_EDGE[quality]
    if state_signal == "NEUTRAL":
        ev += 0.010
        edge += 0.005
    if lead_hours < 8:
        ev += 0.040
        edge += 0.020
    elif lead_hours < PREFERRED_MIN_LEAD_HOURS:
        ev += 0.010
        edge += 0.005
    elif lead_hours > PREFERRED_MAX_LEAD_HOURS:
        ev += 0.010
        edge += 0.005
    if adverse_move >= 0.25:
        steps = min(3, int(math.floor(adverse_move / 0.25 + 1e-9)))
        ev += 0.020 * steps
        edge += 0.010 * steps
    return {"eligible_quality": True, "required_ev": ev, "required_edge": edge}

def gate_candidate(*, quality: str, state_signal: str, lead_hours: float, ev: float,
                   edge: float, adverse_move: float) -> dict:
    if lead_hours < SCAN_MIN_LEAD_HOURS or lead_hours > SCAN_MAX_LEAD_HOURS:
        return {"status": "OUTSIDE_DECISION_WINDOW", "formal": False}
    if state_signal == "CONFLICT":
        return {"status": "REJECT_STATE_CONFLICT", "formal": False}
    th = decision_thresholds(quality, state_signal, lead_hours, adverse_move)
    if not th["eligible_quality"]:
        return {"status": "REJECT_DATA_QUALITY", "formal": False, **th}
    if ev <= 0:
        return {"status": "NO_VALUE", "formal": False, **th}
    if ev < th["required_ev"] or edge < th["required_edge"]:
        return {"status": "WATCHLIST_EDGE_TOO_THIN", "formal": False, **th}
    return {"status": "CANDIDATE", "formal": True, **th}

def _selftest() -> None:
    assert abs(adverse_line_move("全场让球", "HOME", -0.5, -0.75) - 0.25) < 1e-12
    assert abs(adverse_line_move("全场让球", "AWAY", -0.5, -0.25) - 0.25) < 1e-12
    assert abs(adverse_line_move("全场大小球", "OVER", 2.5, 2.75) - 0.25) < 1e-12
    assert abs(adverse_line_move("全场大小球", "UNDER", 2.75, 2.5) - 0.25) < 1e-12
    assert gate_candidate(quality="HIGH", state_signal="SUPPORT", lead_hours=24,
                          ev=.04, edge=.03, adverse_move=0)["formal"]
    assert not gate_candidate(quality="HIGH", state_signal="SUPPORT", lead_hours=24,
                              ev=.001, edge=.001, adverse_move=0)["formal"]
    assert not gate_candidate(quality="LOW", state_signal="SUPPORT", lead_hours=24,
                              ev=.20, edge=.10, adverse_move=0)["formal"]
    assert not gate_candidate(quality="HIGH", state_signal="SUPPORT", lead_hours=2,
                              ev=.20, edge=.10, adverse_move=0)["formal"]
    assert scope_status("Poland III Liga")["status"]=="OUT"
    assert scope_status("Croatia 2.NL")["status"]=="OUT"
    assert scope_status("Germany Bundesliga II")["status"]=="OUT"
    assert scope_status("Netherlands Eerste Divisie")["status"]=="OUT"
    assert scope_status("Spain Segunda")["status"]=="OUT"
    assert scope_status("Japan J2-League")["status"]=="OUT"
    assert scope_status("Scotland Championship")["status"]=="OUT"
    assert scope_status("England Premier League")["status"]=="IN"
    assert scope_status("Netherlands Eredivisie")["status"]=="IN"
    assert scope_status("Japan J1-League")["status"]=="IN"
    assert scope_status("Colombia Primera A")["status"]=="IN"
    assert scope_status("Argentina Liga Profesional")["status"]=="IN"
    assert scope_status("Brazil Serie A")["status"]=="IN"
    assert scope_status("USA MLS")["status"]=="IN"
    assert scope_status("Mexico Liga MX")["status"]=="IN"
    assert scope_status("UEFA Nations League A")["status"]=="IN"
    assert scope_status("International Match")["status"]=="IN"
    print("M1 runtime policy selftest PASS")

if __name__ == "__main__":
    _selftest()