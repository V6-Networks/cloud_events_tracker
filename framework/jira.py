from jira.client import JIRA


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

        return new_issue
