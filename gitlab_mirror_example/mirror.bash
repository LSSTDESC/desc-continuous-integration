#!/bin/bash

# ---------------------------------------------------------------------------
# Script to clone a DESC repository from GitHub to the NERSC GitLab instance.
#
# This script goes in your "mirror" repository on GitLab.
#
# You need to set these in Settings->CI/CD->Variables:
#   - MIRROR_SOURCE_PAT : PAT of the source repository from GitHub.
#   - MIRROR_TARGET_PAT : PAT of the target repository on GitLab.
#
# These are defined in the CI workflow file (.gitlab-ci.yml):
#   - MIRROR_SOURCE_REPO : URL of the source repository from GitHub.
#   - MIRROR_TARGET_REPO : URL of the target repository on GitLab.
#
# Authors:
#   Heather Kelly (@heather999)
#   Stuart McAlpine (@stuartmcalpine)
# ---------------------------------------------------------------------------

# Working directory.
wd=$(pwd)

# Set environment variable GIT_ASKPASS to the value stored in MIRROR_SOURCE_PAT.
# This is used to authenticate the GitHub target repository.
builtin echo -e "#!/usr/bin/env bash
builtin echo ${MIRROR_SOURCE_PAT}" > ${wd}/askpass
chmod +x ${wd}/askpass
export GIT_ASKPASS=${wd}/askpass

set +e

bash << EOF
    echo "Cloning from ${MIRROR_SOURCE_REPO}"

    # Clone repo into a "source" directory.
    rm -rf source
    git init --bare source

    pushd source
        git remote add origin ${MIRROR_SOURCE_REPO}
        git config remote.origin.mirror true

        git fetch origin --prune

        # Switch authentication to the target repository.
        builtin echo -e "#!/usr/bin/env bash
        builtin echo ${MIRROR_TARGET_PAT}" > ${wd}/askpass

        # Push duplicate code to GitLab.
        git remote add target ${MIRROR_TARGET_REPO}

        # Make sure to carefully choose what branches to push.
        # Branches may trigger jobs in the target repo. 
        # Protected branches do not translate across gitlab, github, bitbucket etc.
        git push target --prune +refs/remotes/origin/main:refs/heads/main +refs/tags/*:refs/tags/*
    popd

EOF
status=$(echo $?)

rm -rf ${wd}/askpass

set -e

if [ ! ${status} == "0" ]; then
    exit ${status}
fi

