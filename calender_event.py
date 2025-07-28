
from icalendar import Calendar, Event
from datetime import datetime
from pathlib import Path

import uuid

from zoneinfo import ZoneInfo

calendar=Calendar()
calendar.add('prodid', '-//My Calendar//EN')
calendar.add('version', '2.0')

event=Event()
event.add('uid', str(uuid.uuid4()))
event.add('summary', 'Sample Event')
event.add('dtstart', datetime(2025, 7, 29, 1, 0, 0, tzinfo=ZoneInfo('Europe/Madrid')))
event.add('dtend', datetime(2023, 7, 29, 2, 0, 0, tzinfo=ZoneInfo('Europe/Madrid')))
event.add('description', 'This is a sample event description.')
calendar.add_component(event)

calendar.add_missing_timezones()
Path("C:/Users/hian/Desktop/AutoCalendar/calendar.ics").write_bytes(calendar.to_ical())
