import boto3
from botocore.exceptions import ClientError


class AWS:
    def __init__(self, service, env=None):
        self.env = env
        self.service = service

    def __session_client(self, *args):
        arg = None
        # Grab argument
        for a in args:
            arg = a

        # Build Session
        if self.env:
            session = boto3.client(service_name=self.service,
                                   region_name=self.env)
        elif args:
            session = boto3.client(service_name=self.service,
                                   region_name=arg)
        else:
            session = boto3.client(service_name=self.service)

        return session

    def __get_paginated_events_arns(self, filters):

        arns = []

        # Build client
        client = self.__session_client()

        # Build paginator
        paginator = client.get_paginator('describe_events')

        # Create paginated results
        if filters:
            response = paginator.paginate(filter=filters).build_full_result()
        else:
            response = paginator.paginate().build_full_result()

        # Get Arns
        for r in response['events']:
            arns.append(r)

        # Send it all back
        return arns

    def _get_paginated_instances(self, instance_id, availability_zone, vpc_id):

        # Build client
        client = self.__session_client()

        # Build paginator
        paginator = client.get_paginator('describe_instances')

        for vid in vpc_id:
            try:
                # Create paginated results
                response = paginator.paginate(Filters=[
                    {
                        'Name': 'availability-zone',
                        'Values': [availability_zone]
                    },
                    {
                        'Name': 'tag-key',
                        'Values': ['Name']
                    },
                    {
                        'Name': 'vpc-id',
                        'Values': [vid]
                    }
                ],
                    InstanceIds=[instance_id]).build_full_result()

                print(response)
            except ClientError as ce:
                print('Woops Error: ', ce)

    def _get_vpc_ids(self, region_name=None):

        vpc_ids = list()

        client = self.__session_client(region_name)

        vpcs = client.describe_vpcs()

        for vpc in vpcs['Vpcs']:
            vpc_ids.append(vpc['VpcId'])

        return vpc_ids

    def get_aws_event_status(self, filters=None):
        instance_event_dict = dict()

        # Build the client
        client = self.__session_client()

        try:
            # Get all ARNS that can be found
            event_arn = self.__get_paginated_events_arns(filters)

            for arn in event_arn:
                response = client.describe_affected_entities(filter={
                    'eventArns': [arn['arn']]
                })

                for r in response['entities']:
                    instance_event_dict.update({r['entityValue']: {'Instance_Id': r['entityValue'],
                                                                   'Region': arn['region'],
                                                                   'Event_type': arn['eventTypeCode'],
                                                                   'Service': arn['service'],
                                                                   'Start': arn['startTime'],
                                                                   'End': arn['endTime']}})

            return instance_event_dict

        except ClientError as ce:
            print(ce)
