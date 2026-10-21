"""Read-only identity and UTC audit for M3 to Crown fixture pairing."""
from datetime import datetime, timezone

def strict_utc(value):
    timestamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if timestamp.tzinfo is None or timestamp.utcoffset().total_seconds() != 0:
        raise ValueError('explicit UTC required')
    return timestamp.astimezone(timezone.utc)

def check_pair(forecast, fixture):
    if fixture.get('join_method') not in ('shared_provider_id', 'official_fixture_crosscheck'):
        return False
    if not fixture.get('identity_evidence_uri') or not fixture.get('totalcorner_match_id'):
        return False
    if forecast.get('fixture_identity_id') != fixture.get('fixture_identity_id'):
        return False
    for name in ('league', 'season', 'home_team', 'away_team'):
        if forecast.get(name) != fixture.get(name) or not forecast.get(name):
            return False
    try:
        predicted = strict_utc(forecast['forecasted_at_utc'])
        kickoff = strict_utc(fixture['kickoff_at_utc'])
        evidence_at = strict_utc(fixture['kickoff_evidence_captured_at_utc'])
    except (KeyError, ValueError, TypeError, AttributeError):
        return False
    return predicted <= evidence_at < kickoff
