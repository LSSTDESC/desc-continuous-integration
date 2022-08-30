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

source_repo    = os.getenv('GITLAB_TARGET_REPO')
source_branch  = os.getenv('GITHUB_SOURCE_BRANCH')
target_repo    = os.getenv('GITHUB_SOURCE_REPO')
source_pat     = os.getenv('STATUS_SOURCE_PAT')
target_pat     = os.getenv('STATUS_TARGET_PAT')
target_repo_context = os.getenv('GITLAB_STATUS_CONTEXT')

source_api = "https://software.nersc.gov/api/v4"
target_api = "https://api.github.com"

target_project = target_repo.split("/")[-2:]
seperator = '/'
target_project = seperator.join(target_project)
target_project = target_project.split(".")[0]

source_project = source_repo.split("/")[-1].split(".")[0]
search_repos = requests.get("{}/projects?search={}".format(source_api,source_project),
        headers={'PRIVATE-TOKEN': source_pat})
source_project_number = search_repos.json()[0]['id']
source_branch = source_branch.split(",")

pipelines_all = requests.get("{}/projects/{}/pipelines".format(source_api,source_project_number),
        headers={'PRIVATE-TOKEN': source_pat}).json()
for pipeline in pipelines_all:
    if pipeline['ref'] in source_branch:
        ci_status = pipeline['status']
        acceptable_pipelines=["running","success","failed","canceled","skipped","manual"]
        if  ci_status in acceptable_pipelines:
            break

ci_status = pipeline['status']
print(f"Status from GitHub = {ci_status}")

if ci_status == "running":
    ci_status = "pending"
elif ci_status == "failed":
    ci_status = "failure"
elif ci_status == "canceled":
    ci_status = "error"
elif ci_status == "skipped":
    ci_status = "error"
elif ci_status == "manual":
    ci_status = "error"

ci_web_url = pipeline['web_url']
sha = pipeline['sha']

status = {
        'state' : ci_status,
        'target_url' : ci_web_url,
        'context' : target_repo_context
        }
post_status = requests.post("{}/repos/{}/statuses/{}".format(target_api,target_project,sha),
        headers={'Authorization' : 'token ' + target_pat},
        data=json.dumps(status))

if post_status.status_code != 201:
    print(post_status.text)
    exit()

