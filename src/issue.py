import json
from utils import Utils


class Issues:
    '''This class is responsible for creating the issues'''
    def __init__(self, file_path, token, repo):
        self.file_path = file_path
        self.issues = []
        self.token = token
        self.github_api_url = "https://api.github.com"
        self.repo = repo

    def __create_issue_body_architecture(self, smells):
        '''Create the body of the issue'''
        body = ""
        for smell in smells:
            smell_info = smell.split(",")
            body += f"\n - [ ] **Package Name**: {smell_info[1]} **Smell**: {smell_info[2]}<br><br>"
        return body

    def __create_issue_body_design(self, smells):
        '''Create the body of the issue'''
        body = ""
        for smell in smells:
            smell_info = smell.split(",")
            body += f"\n - [ ] **Package Name**: {smell_info[1]} **Type/Module**: {smell_info[2]} **Smell**: {smell_info[3]}<br><br>"
        return body

    def __create_issue_body_implementation(self, smells):
        '''Create the body of the issue'''
        body = ""
        for smell in smells:
            smell_info = smell.split(",")
            body += f"\n - [ ] **Package Name**: {smell_info[1]} **Type/Module**: {smell_info[2]} **Method**: {smell_info[3]} **Smell**: {smell_info[4]}<br><br>"
        return body

    def __parse_issues(self):
        with open(self.file_path, "r") as f: #pylint: disable=unspecified-encoding
            smells = json.load(f)

        architecture_smells = smells.get("architecture_smells", [])
        design_smells = smells.get("design_smells", [])
        implementation_smells = smells.get("implementation_smells", [])

        if architecture_smells:
            self.issues.append({"title": "Architecture Smells", "body": self.__create_issue_body_architecture(architecture_smells)})

        if design_smells:
            self.issues.append({"title": "Design Smells", "body": self.__create_issue_body_design(design_smells)})

        if implementation_smells:
            self.issues.append({"title": "Implementation Smells", "body": self.__create_issue_body_implementation(implementation_smells)})

    def get_issues(self):
        '''Get the issues'''
        self.__parse_issues()
        return self

    def create_issues(self):
        '''Create the issues'''
        for issue in self.issues:
            print(issue["body"])
            data = {
                "title": issue["title"],
                "body": issue["body"],
                "labels": ["smell"]
            }
            print(data)
            resp = Utils.api_request(f"{self.github_api_url}/repos/{self.repo}/issues", self.token, method="POST", json=data)
            if resp.status_code != 201:
                print(f"Failed to create issue - {issue['title']}.")
                print(resp.json())
                return False
            print(f"Issue - {issue['title']} created successfully.")
        return True






