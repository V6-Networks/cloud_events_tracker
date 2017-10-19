# import os
# import logging
import sys
# import shutil
# import json
from prettytable import PrettyTable
# import string
import boto3
import calendar
from datetime import datetime, timedelta
from jira.client import JIRA


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
        x = PrettyTable(['Name', 'Instance ID', 'Event_type', 'Start Local', 'End Local'])
        for k, c in events.items():
            x.add_row([
                c['Name'],
                c['Instance_Id'],
                c['Event_type'],
                c['Start'],
                c['End']
            ])
        print(x)


class AWS:
    def __init__(self, env):
        self.env = env

    def get_aws_events(self, instance_tags):
        instance_event_dict = {}
        for instance_tag in instance_tags:
            session = boto3.Session(profile_name=self.env)
            ec2 = session.client('ec2')
            instance_name = ec2.describe_instances(
                Filters=[
                    {
                        'Name': 'tag-key',
                        'Values': [
                            'Name']
                    }
                ],
                InstanceIds=[instance_tag]
            )
            instance_status = ec2.describe_instance_status(
                InstanceIds=[instance_tag]
            )
            for reservation in instance_name['Reservations']:
                # print "Reservation %s " % reservation
                for instance in reservation['Instances']:
                    for item in instance['Tags']:
                        if item['Key'] == 'Name':
                            instance_details = {'Instance_Id': instance['InstanceId'], 'Name': item['Value']}
                            instance_event_dict.update({instance['InstanceId']: instance_details})

            for item in instance_status['InstanceStatuses']:
                for event in item['Events']:
                    start_time = Utils.utc_to_local(event['NotBefore'])
                    end_time = Utils.utc_to_local(event['NotAfter'])
                    instance_event_dict[instance['InstanceId']].update(
                        {'Event_type': event['Code'], 'Start': start_time, 'End': end_time})

        return instance_event_dict


class JIRA_API:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def post_to_jira(self, environment, details):
        jira_options = {'server': self.host}
        jira = JIRA(options=jira_options, basic_auth=(self.user, self.password))
        if environment == "dev":
            project = "SDLC"
        else:
            project = "OPS"
        issue_dict = {
            'project': {'key': project},
            'summary': 'New issue from jira-python',
            'description': 'Look into this one',
            'issuetype': {'name': 'Bug'},
        }
        new_issue = jira.create_issue(fields=issue_dict)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("You forgot some arguments\n")
        print("Usage: python %s prd instance" % sys.argv[0])
        sys.exit(1)
    else:
        # Set env globally for all future AWS commands
        aws = AWS(sys.argv[1])
        instance_tags = sys.argv[2].split(",")

        # Grab any and all events
        event = aws.get_aws_events(instance_tags)

        # Print what we find
        print(event)
        Utils.print_table(event)
