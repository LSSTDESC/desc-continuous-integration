# ----------------------------------------------------------------------------#
# Script to clone a DESC repository from GitHub to the NERSC GitLab instance. #
#                                                                             #
# This script goes in your "mirror" repository on GitLab.                     #
#                                                                             #
# Script adapted from the CI Resources "mirroring" example                    #
# (https://software.nersc.gov/ci-resources/mirroring)                         #
#                                                                             #
# You need to set these in Settings->CI/CD->Variables:                        #
#   - MIRROR_SOURCE_PAT : PAT of the source repository from GitHub.           #
#   - MIRROR_TARGET_PAT : PAT of the target repository on GitLab.             #
#                                                                             #
# These are defined in the CI workflow file (.gitlab-ci.yml):                 #
#   - MIRROR_SOURCE_REPO : URL of the source repository from GitHub.          #
#   - MIRROR_TARGET_REPO : URL of the target repository on GitLab.            #
#   - TARGET_PROJECT_NUMBER: Project number for the target repository         #
#   - MIRROR_SOURCE_BRANCH: branch from source repo to mirror                 #
#                                                                             #
# Authors:                                                                    #
#   Stuart McAlpine (@stuartmcalpine)                                         #
#   Heather Kelly (@heather999)                                               #
# ----------------------------------------------------------------------------#

#!/bin/bash

set -e

# Working directory.
wd=$(pwd)

# Always want to remove authentication file on exit (file even if workflow fails).
function cleanup()
{
    echo "Cleanup: Removing ${wd}/askpass"
    rm -rf ${wd}/askpass
}
trap cleanup EXIT

# Set GIT_ASKPASS for git authentication.
function set_askpass()
{
    echo "#!/bin/bash" > ${wd}/askpass
    echo "echo $1" >> ${wd}/askpass

    chmod +x ${wd}/askpass
    export GIT_ASKPASS=${wd}/askpass
}

# Step 1) Fetch information from source repository.
set_askpass ${MIRROR_SOURCE_PAT}
echo "Cloning from ${MIRROR_SOURCE_REPO}"

rm -rf source
git init --bare source

cd source
git remote add origin ${MIRROR_SOURCE_REPO}
git config remote.origin.mirror true

git fetch origin --prune

# Step 2) Clone source repository contents to target repository.
set_askpass ${MIRROR_TARGET_PAT}
git remote add target ${MIRROR_TARGET_REPO}

# Only pushes the MIRROR_SOURCE_BRANCH repository (and its tags).
# Protected branches do not translate across gitlab, github, bitbucket etc.
git push target --prune +refs/remotes/origin/$MIRROR_SOURCE_BRANCH:refs/heads/$MIRROR_SOURCE_BRANCH +refs/tags/*:refs/tags/*
