import argparse
import os

from designiteutil.designite_diff import process
from artifact_processor import ArtifactProcessor
from issue import Issues

def get_new_smells(designite_output_old, designite_output_new):
    '''Get the new smells from the current run'''
    process(designite_output_old, designite_output_new, "new_smells.json")
    with open("new_smells.json", "r") as f: #pylint: disable=unspecified-encoding
        print(f.read())

def _download_artifact(designite_output, repo, token):
    download_artifact_output = ArtifactProcessor(designite_output, repo, token).download_artifact()
    if not download_artifact_output:
        print(f"Failed to download artifact for repository - {repo}.")
        return False
    print(f"Artifact '{designite_output}' downloaded successfully - {os.path.abspath(designite_output)}")
    return True


def ls(folder):
    print(f'ls {folder}: ')
    for file in [f for f in os.listdir(folder)]:
        print(file)


def main(token, designite_output_old, designite_output_new, repo):
    '''Download an artifact from a given run ID.'''
    ls('.')
    ls('/github/workspace')
    if not _download_artifact(designite_output_old, repo, token):
        return
    if not _download_artifact(designite_output_new, repo, token):
        return
    if not designite_output_new:
        print("Failed to find the artifact from the current run.")
        return

    get_new_smells(designite_output_old, designite_output_new)
    issues = Issues("new_smells.json", token=token, repo=repo).get_issues().create_issues()
    if not issues:
        print("Failed to create issues.")
        return

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--token", dest="token", help="API token")
    parser.add_argument("--repo-name", dest="repo", help="Repo name")
    parser.add_argument("--designite-output-old", dest="designite_output_old", help="Designite Output Old")
    parser.add_argument("--designite-output-new", dest="designite_output_new", help="Designite Output New")
    args = parser.parse_args()

    # download_artifact(args.token, args.run_id, args.repo)
    main(args.token, args.designite_output_old, args.designite_output_new, args.repo)