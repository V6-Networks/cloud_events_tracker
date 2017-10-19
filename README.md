# Cloud Events racker

A bit of code that takes IAAS providers events and creates calendar events and issue tickets for tracking purposes

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* AWS credentials in .aws/credentials
```
[default]
aws_access_key_id={YOUR_ACCESS_KEY_ID}
aws_secret_access_key={YOUR_SECRET_ACCESS_KEY}

[prd]
aws_access_key_id={YOUR_ACCESS_KEY_ID}
aws_secret_access_key={YOUR_SECRET_ACCESS_KEY}

[dev]
aws_access_key_id={YOUR_ACCESS_KEY_ID}
aws_secret_access_key={YOUR_SECRET_ACCESS_KEY}
```

### Installing

* Requirements
  * Python 3
  * Install pipenv (https://github.com/kennethreitz/pipenv)

initialize the development

```
pipenv shell 
```

Demo
```
python aws-tickets.py -e prd -i i-4f3b21,i-1d23422b,i-0559d
+------------+-------------+-----------+---------------+---------------------+---------------------+
|    Name    | Instance ID |   Region  |   Event_type  |     Start Local     |      End Local      |
+------------+-------------+-----------+---------------+---------------------+---------------------+
|  web1-prd  |   i-4f3b21  | us-west-1 | system-reboot | 2017-11-01 04:30:00 | 2017-11-01 08:00:00 |
|  App2-stg  |  i-1d23422b | us-west-2 | system-reboot | 2017-11-06 03:30:00 | 2017-11-06 07:00:00 |
| code3-dev  |   i-0559d   | us-west-2 | system-reboot | 2017-11-06 05:15:00 | 2017-11-06 07:00:00 |
+------------+-------------+-----------+---------------+---------------------+---------------------+
```



## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

TBA

## Built With

TBA

## Contributing

TBA

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/V6-Networks/cloud_events_tracker/tags). 

## Authors

* **Daniel Rahamim** - *Initial work* - [Drahamim](https://github.com/drahamim)
* **Eric Olson** - *Initial work* - [Reservoirdog](https://github.com/reservoirdog)

See also the list of [contributors](https://github.com/V6-Networks/cloud_events_tracker/contributors) who participated in this project.

## License

TBA

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
