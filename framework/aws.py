import boto3
from botocore.exceptions import ClientError
from .utils import Utils


class AWS:
    def __init__(self, env):
        self.env = env

    def get_aws_events(self, instance_tags):
        instance_event_dict = {}
        region_list = ['us-west-1', 'us-west-2', 'us-east-1']

        # Build session
        session = boto3.Session(profile_name=self.env)

        for instance_tag in instance_tags:
            for region in region_list:
                print(region)
                ec2 = session.client('ec2', region_name=region)
                try:

                    # Pull instance name
                    instance_name = ec2.describe_instances(
                        Filters=[
                            {
                                'Name': 'tag-key',
                                'Values': ['Name']
                            }
                        ],
                        InstanceIds=[instance_tag])

                    # Pull instance status
                    instance_status = ec2.describe_instance_status(
                        InstanceIds=[instance_tag])

                    for reservation in instance_name['Reservations']:
                        # print "Reservation %s " % reservation
                        for instance in reservation['Instances']:
                            for item in instance['Tags']:
                                if item['Key'] == 'Name':
                                    instance_details = {'Instance_Id': instance['InstanceId'], 'Name': item['Value']}
                                    instance_event_dict.update({instance['InstanceId']: instance_details})

                    for item in instance_status['InstanceStatuses']:
                        try:
                            for event in item['Events']:
                                start_time = Utils.utc_to_local(event['NotBefore'])
                                end_time = Utils.utc_to_local(event['NotAfter'])
                                instance_event_dict[instance['InstanceId']].update(
                                    {'Event_type': event['Code'], 'Start': start_time, 'End': end_time})
                        except ValueError as ve:
                            print('Whoops need to work on this ', ve)
                            continue

                except ClientError as ce:
                    print('Whoops need to work on this', ce)
                    continue

        return instance_event_dict
