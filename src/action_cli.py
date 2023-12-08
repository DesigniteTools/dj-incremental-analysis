import argparse
import requests
import os
import zipfile
from designiteutil.designite_diff import process

GITHUB_API_URL = "https://api.github.com"

def api_request(url, token, method="GET", data=None, params=None):
    '''Make an API request to GitHub.'''

    headers = {"Authorization": f"Bearer {token}"}
    timeout = 10
    response = requests.request(method, url, headers=headers, timeout=timeout, data=data, params=params)
    return response

def download_artifact(artifacts, designite_output_old, token):
    '''Download an artifact from a given artifact name'''
    
    for artifact in artifacts:
        if artifact["name"] == designite_output_old:
            resp = api_request(artifact["archive_download_url"], token)
            if resp.status_code != 200:
                print(f"Failed to download artifact '{artifact['name']}'.")
                return False

            # Save the downloaded artifact to a local file - This saves in the current repository checkout directory
            with open(f'{artifact["name"]}.zip', 'wb') as f:
                f.write(resp.content)

            os.makedirs(artifact["name"], exist_ok=True)
            # Extract the downloaded artifact
            with zipfile.ZipFile(f'{artifact["name"]}.zip', 'r') as zip_ref:
                zip_ref.extractall(artifact["name"])
        break
    return True

def get_new_smells(designite_output_old, designite_output_new):
    '''Get the new smells from the current run'''
    process(designite_output_old, designite_output_new, "new_smells.json")
    with open("new_smells.json", "r") as f:
        print(f.read())


def main(token, designite_output_old, designite_output_new, repo):
    '''Download an artifact from a given run ID.'''
    artifact_resp = api_request(f"{GITHUB_API_URL}/repos/{repo}/actions/artifacts", token, params={"per_page": 100})

    if artifact_resp.status_code != 200:
        print(f"Failed to fetch artifacts for repository - {repo}.")
        return
    
    artifact_resp = artifact_resp.json()
    
    if artifact_resp.get("total_count", 0) == 0:
        print(f"No artifacts found for this repository - {repo}.")
        return

    if not download_artifact(artifact_resp["artifacts"], designite_output_old, token):
        print(f"Failed to download artifact for repository - {repo}.")
        return
    
    print(f"Artifact '{designite_output_old}' downloaded successfully.")

    get_new_smells(designite_output_old, designite_output_new)




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--token", dest="token", help="API token")
    parser.add_argument("--repo-name", dest="repo", help="Repo name")
    parser.add_argument("--designite-output-old", dest="designite_output_old", help="Designite Output Old")
    parser.add_argument("--designite-output-new", dest="designite_output_new", help="Designite Output New")
    args = parser.parse_args()

    # download_artifact(args.token, args.run_id, args.repo)
    # main(args.token, args.designite_output_old, args.designite_output_new, args.repo)
    print(os.getcwd())