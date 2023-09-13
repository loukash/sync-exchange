#!/usr/bin/env python3

import pytz
import caldav
import getpass
import datetime

from exchangelib import Credentials, Configuration, Account, DELEGATE


caldav_url = "https://cld.z.lukash.in/remote.php/dav"
caldav_user = "andrey"
headers = {}

try:
    password = getpass.getpass("Пароль рабочего календаря: ")
    caldav_password = getpass.getpass("Пароль домашнего календаря: ")
except Exception as e:
    print('ERROR', e)

credentials = Credentials(username="aglukashin@avito.ru", password=password)
config = Configuration(server="exchange.avito.ru", credentials=credentials)

account = Account(
    primary_smtp_address="aglukashin@avito.ru",
    config=config,
    autodiscover=False,
    access_type=DELEGATE,
)

start = datetime.datetime.now(tz=pytz.timezone(str(account.default_timezone)))

items = account.calendar.view(
    start=start,
    end=start + datetime.timedelta(days=14),
)

for item in items:
    print(item.subject, item.uid, item.is_all_day, item.start, item.end)

    with caldav.DAVClient(url=caldav_url, username=caldav_user, password=caldav_password, headers=headers) as client:
        my_principal = client.principal()
        my_calendars = my_principal.calendars()

        # for c in calendars:
        #     print(c.name, c.id, c.url)

        my_calendar = my_principal.calendar(cal_id="1-3")  # 1-3 - А. Работа; cal_id, cal_name, cal_url

        if item.is_all_day:
            continue

        my_event = my_calendar.save_event(
                dtstart=datetime.datetime.strptime(str(item.start), '%Y-%m-%d %H:%M:%S%z'),
                dtend=datetime.datetime.strptime(str(item.end), '%Y-%m-%d %H:%M:%S%z'),
                uid=item.uid,
                summary=item.subject,
                )

        print(my_event)

