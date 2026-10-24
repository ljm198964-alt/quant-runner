"""Use early GitHub cron events to begin M3 scans at user-approved Beijing slots.

GH schedule may start late. Never silently claim delayed execution was on-time.
"""
import argparse
import datetime
import json
import time

UTC=datetime.timezone.utc

def target(schedule,now):
    # Early schedule at UTC 17:00 -> UTC 22:00 = 06:00 Beijing next day.
    # Early schedule at UTC 23:00 -> UTC 04:00 = 12:00 Beijing next day.
    hour={'0 17 * * *':22,'0 23 * * *':4}[schedule]
    day=now.date() if hour==22 else now.date()+datetime.timedelta(days=1)
    if hour==22 and now.hour>=22:day+=datetime.timedelta(days=1)
    # For schedule=23 and action starts after midnight, day is current UTC day.
    if hour==4 and now.hour<12:day=now.date()
    return datetime.datetime.combine(day,datetime.time(hour,tzinfo=UTC))

def wait(schedule,now=None,sleep=time.sleep):
    now=now or datetime.datetime.now(UTC)
    destination=target(schedule,now)
    seconds=(destination-now).total_seconds()
    if seconds < -600 or seconds>5*3600:
        raise RuntimeError('MISSED_OR_INVALID_SCAN_SLOT '+json.dumps({'schedule':schedule,'target':destination.isoformat(),'now':now.isoformat()}))
    if seconds>0:sleep(seconds)
    print(json.dumps({'status':'SCAN_SLOT_REACHED','target_utc':destination.isoformat(),'actual_utc':datetime.datetime.now(UTC).isoformat()}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cron',required=True);a=p.parse_args();wait(a.cron)
