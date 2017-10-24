import calendar
from datetime import datetime, timedelta
from prettytable import PrettyTable


class Utils:
    @staticmethod
    def utc_to_local(utc_dt):
        # get integer timestamp to avoid precision lost
        timestamp = calendar.timegm(utc_dt.timetuple())
        local_dt = datetime.fromtimestamp(timestamp)
        assert utc_dt.resolution >= timedelta(microseconds=1)

        return local_dt.replace(microsecond=utc_dt.microsecond)

    @staticmethod
    def print_table(events):
        x = PrettyTable(['Name', 'Instance ID','Region', 'Event_type', 'Start Local', 'End Local'])
        for k, c in events.items():
            x.add_row([
                c['Name'],
                c['Instance_Id'],
                c['Region'],
                c['Event_type'],
                c['Start'],
                c['End']
            ])
        print(x)
