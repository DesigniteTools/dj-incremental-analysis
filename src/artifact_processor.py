'''
File: artifact_processor.py 
Author: indranil Palit < 
Description: Module to download and extract the artifact from the repository.
'''

import os
import zipfile
from utils import Utils


class ArtifactProcessor:
    '''This class is responsible for downloading the artifact from the repository and extracting it.'''

    def __init__(self, designite_output_old, repo, token):
        self.github_api_url = "https://api.github.com"
        self.designite_output_old = designite_output_old
        self.repo = repo
        self.token = token

    def __fetch_repo_artifact(self):
        artifact_resp = Utils.api_request(f"{self.github_api_url}/repos/{self.repo}/actions/artifacts", self.token, params={"per_page": 100})

        if artifact_resp.status_code != 200:
            print(f"Failed to fetch artifacts for repository - {self.repo}.")
            return None

        artifacts = artifact_resp.json()["artifacts"]
        filtered_artifacts = list(filter(lambda artifact: artifact["name"] == self.designite_output_old, artifacts))

        if not filtered_artifacts or len(filtered_artifacts) >1:
            print(f"No artifacts found for this repository or multiple artifacts found - {self.designite_output_old}. Please check the artifact name.")
            return None

        artifact = filtered_artifacts[0]

        return artifact


    def download_artifact(self):
        '''Download an artifact from a given artifact name'''

        artifact = self.__fetch_repo_artifact()

        if not artifact:
            return False

        resp = Utils.api_request(artifact["archive_download_url"], self.token)
        if resp.status_code != 200:
            print(f"Failed to download artifact '{artifact['name']}'.")
            return False
        try:
            # Save the downloaded artifact to a local file - This saves in the current repository checkout directory (/github/workspace)
            with open(f'{artifact["name"]}.zip', 'wb') as f:
                f.write(resp.content)

            os.makedirs(artifact["name"], exist_ok=True)
            # Extract the downloaded artifact
            with zipfile.ZipFile(f'{artifact["name"]}.zip', 'r') as zip_ref:
                zip_ref.extractall(artifact["name"])
        except Exception as e: #pylint: disable=broad-except
            print(f"Failed to extract artifact '{artifact['name']}'.")
            print(e)
            return False

        return True
    