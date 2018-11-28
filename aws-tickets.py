from framework.aws import AWS
from framework.utils import Utils
import argparse


if __name__ == '__main__':
    # Setup Arg parsing
    parser = argparse.ArgumentParser(description='AWS Event API scrapper')
    requiredNamed = parser.add_argument_group('Required Names Arguments')
    requiredNamed.add_argument('-s', '--service', help='Service to pull AWS events from', required=True)
    requiredNamed.add_argument('-e', '--environment', help='Environment to pull AWS events from. If health '
                                                           'services \'us-east-1\' is the only option', required=True)
    requiredNamed.add_argument('-i', '--instances', help='Instance or list of instances to pull events on',
                               required=False)
    args = parser.parse_args()

    # Set env globally for all future AWS commands
    aws = AWS(args.service, env=args.environment)

    # Grab instance tags
    if args.instances:
        instance_tags = args.instances.split(",")

    # Grab any and all events
    event = aws.get_aws_event_status(filters={'eventStatusCodes': ['upcoming']})

    # Print what we find
    print(event)
    Utils.print_table(event)
