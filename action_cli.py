# import typer


# def main(api_token: str, vcs: str = "github"):
#     print(vcs)

# if __name__=="__main__":
#     typer.run(main)

import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--token", dest="token", help="API token")
parser.add_argument("--user", dest="user", help="User name")
parser.add_argument("--repo", dest="repo", help="Repo name")
parser.add_argument("--artifact", dest="artifact", help="Artifact ID")

def download_artifact(token, artifact_id, user, repo):
    headers = {"Authorization": f"Bearer {token}"}
    timeout = 10  # Set the timeout value in seconds
    r = requests.get(f"https://api.github.com/repos/{user}/{repo}/actions/artifacts/{artifact_id}", headers=headers, timeout=timeout)
    print(r.json())

if __name__ == "__main__":
    args = parser.parse_args()
    download_artifact(args.token, args.artifact, args.user, args.repo)
    