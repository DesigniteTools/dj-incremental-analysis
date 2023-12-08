import argparse
from designiteutil.designite_diff import process
from artifact_processor import ArtifactProcessor

def get_new_smells(designite_output_old, designite_output_new):
    '''Get the new smells from the current run'''
    process(designite_output_old, designite_output_new, "new_smells.json")
    with open("new_smells.json", "r") as f: #pylint: disable=unspecified-encoding
        print(f.read())


def main(token, designite_output_old, designite_output_new, repo):
    '''Download an artifact from a given run ID.'''

    download_artifact_output = ArtifactProcessor(designite_output_old, repo, token).download_artifact()

    if not download_artifact_output:
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
    main(args.token, args.designite_output_old, args.designite_output_new, args.repo)