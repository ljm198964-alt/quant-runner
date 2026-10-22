"""User-approved M3 minimum 90-minute lead, requiring independently qualified UTC kickoff."""
from __future__ import annotations
import datetime

MIN_LEAD_MINUTES = 90
UTC = datetime.timezone.utc

def verified_kickoff(row):
    """Accept only explicitly UTC/offset-aware provider time, never naive wall clocks."""
    value=row.get('kickoff_utc_verified')
    if not isinstance(value,str) or not value:return None
    try:
        ts=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:return None
    if ts.tzinfo is None or ts.utcoffset() is None:return None
    return ts.astimezone(UTC)

def gate(row,observed_utc):
    kickoff=verified_kickoff(row)
    if kickoff is None:return False,None,'KICKOFF_UTC_UNVERIFIED'
    if observed_utc.tzinfo is None:raise ValueError('observation must be offset-aware')
    lead=(kickoff-observed_utc.astimezone(UTC)).total_seconds()/60
    if lead<MIN_LEAD_MINUTES:return False,round(lead,3),'UNDER_90_MINUTES'
    return True,round(lead,3),'PASS'
