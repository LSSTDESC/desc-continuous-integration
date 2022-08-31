# ----------------------------------------------------------------------------#
# Script to report the status of the CI workflow of the target repository on  #
# GitLab to the source repository on GitHub.                                  #
#                                                                             #
# This script goes in your "status" repository on GitLab.                     #
#                                                                             #
# Script adapted from the CI Resources "Report Status" example                #
# (https://software.nersc.gov/ci-resources/report-status)                     #
#                                                                             #
# You need to set these in Settings->CI/CD->Variables:                        #
#   - STATUS_SOURCE_PAT : PAT of the target repository from GitLab.           #
#   - STATUS_TARGET_PAT : PAT of the source repository on GitHub.             #
#                                                                             #
# Other variables are passed along with the trigger token from GitHub.        #
#                                                                             #
# Authors:                                                                    #
#   Stuart McAlpine (@stuartmcalpine)                                         #
#   Heather Kelly (@heather999)                                               #
# ----------------------------------------------------------------------------#

#!/usr/bin/env python3
import os
import requests
import json
import time

# Pull out environment variables.
source_repo = os.getenv("GITLAB_TARGET_REPO")
source_branch = os.getenv("GITHUB_SOURCE_BRANCH")
target_repo = os.getenv("GITHUB_SOURCE_REPO")
source_pat = os.getenv("STATUS_SOURCE_PAT")
target_pat = os.getenv("STATUS_TARGET_PAT")
target_repo_context = os.getenv("GITLAB_STATUS_CONTEXT")
sha = os.getenv("GITHUB_SHA")

# Get information from repos APIs.
source_api = "https://software.nersc.gov/api/v4"
target_api = "https://api.github.com"

target_project = target_repo.split("/")[-2:]
seperator = "/"
target_project = seperator.join(target_project)
target_project = target_project.split(".")[0]

source_project = source_repo.split("/")[-1].split(".")[0]
search_repos = requests.get(
    "{}/projects?search={}".format(source_api, source_project),
    headers={"PRIVATE-TOKEN": source_pat},
)
source_project_number = search_repos.json()[0]["id"]
source_branch = source_branch.split(",")


def check_status(source_api, source_project_number, source_pat, source_branch, sha):
    """ Get the workflow status of a CI job. """

    ci_status = None

    # Loop over each CI workflow at target repository and find the right commit.
    pipelines_all = requests.get(
        "{}/projects/{}/pipelines".format(source_api, source_project_number),
        headers={"PRIVATE-TOKEN": source_pat},
    ).json()

    for pipeline in pipelines_all:

        if pipeline["sha"] == sha:
            assert (
                pipeline["ref"] in source_branch
            ), f"Bad branch {pipeline['ref']} != {source_branch}"
            ci_status = pipeline["status"]
            ci_web_url = pipeline["web_url"]
            print(f"Found {sha} on branch {pipeline['ref']} with status '{ci_status}'.")
            break

    assert ci_status is not None, "Could not find workflow for this commit"

    return ci_status, ci_web_url


# Get the status of the work flow at the target repo for this commit.
ci_status, ci_web_url = check_status(
    source_api, source_project_number, source_pat, source_branch, sha
)

# Sometimes it takes a bit of time to update the status, this does a few checks.
count = 0
while ci_status == "running":
    if count >= 10:
        break

    time.sleep(10)
    ci_status, ci_web_url = check_status(
        source_api, source_project_number, source_pat, source_branch, sha
    )
    count += 1


# Convert to allowed GitHub Actions status tag.
if ci_status == "running":
    ci_status = "pending"
elif ci_status == "success":
    ci_status = "success"
else:
    ci_status = "error"

# Append workflow to GitHub.
status = {"state": ci_status, "target_url": ci_web_url, "context": target_repo_context}
post_status = requests.post(
    "{}/repos/{}/statuses/{}".format(target_api, target_project, sha),
    headers={"Authorization": "token " + target_pat},
    data=json.dumps(status),
)

if post_status.status_code != 201:
    print(post_status.text)
    exit()
