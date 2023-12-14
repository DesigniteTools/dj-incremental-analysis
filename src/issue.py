import json
from constants import ARCHITECTURE_SMELL_TEMPLATE, DESIGN_SMELL_TEMPLATE, IMPLEMENTATION_SMELL_TEMPLATE


class Issues:
    '''This class is responsible for creating the issues'''
    def __init__(self, file_path):
        self.file_path = file_path
        self.issues = []

    def __create_issue_body_architecture(self, smells):
        '''Create the body of the issue'''
        body = ""
        for smell in smells:
            smell_info = smell.split(",")
            body += ARCHITECTURE_SMELL_TEMPLATE.replace("_pkg_name_", smell_info[1]) \
                                .replace("_smell_", smell_info[2])
            body += "\n\n"
        return body
    
    def __create_issue_body_design(self, smells):
        '''Create the body of the issue'''
        body = ""
        for smell in smells:
            smell_info = smell.split(",")
            body += DESIGN_SMELL_TEMPLATE.replace("_pkg_name_", smell_info[1]) \
                                .replace("_type_", smell_info[2]) \
                                .replace("_smell_", smell_info[3])
            body += "\n\n"
        return body

    def __create_issue_body_implementation(self, smells):
        '''Create the body of the issue'''
        body = ""
        for smell in smells:
            smell_info = smell.split(",")
            body += IMPLEMENTATION_SMELL_TEMPLATE.replace("_pkg_name_", smell_info[1]) \
                                .replace("_type_", smell_info[2]) \
                                .replace("_method_", smell_info[3]) \
                                .replace("_smell_", smell_info[4])
            body += "\n\n"
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
        return self.issues



                    
                    
                