CI at NERSC using GitLab
========================

For the majority of cases the GitHub-hosted runners available with GitHub
Actions are more than sufficient to test and maintain code stability for DESC
repositories.

However, some repositories at DESC do require a direct deployment of the CI
workflow to the *Cori* and *Perlmutter* machines at `NERSC
<https://www.nersc.gov/>`__, to have access to specific development tools, or
to test the code using the large datasets hosted at the facility, for example.

As there is no way to link CI workflows using GitHub Actions to the NERSC
facilities directly, we require a bit of a workaround:

#. Mirror the repository to the `NERSC GitLab instance <https://software.nersc.gov/>`__
   where we have direct access to the *Cori* and *Perlmutter* machines.

#. Implement a CI workflow using GitLab's builtin CI tools (similar to GitHub
   Actions).

#. Report the results back to GitHub.

Below is a schematic of the process.

.. image:: ../images/repo-flow.png

Here we go over the steps required to implement a CI workflow at NERSC, for the
example of our test repository. The goal is the same as before, to trigger the
repositories' test suite when changes to the repositories' codebase are made.
The difference now being that these tests will be performed directly on *Cori*,
and not on a GitHub Actions-hosted runner.

.. note:: You will need a NERSC account and access to the `NERSC GitLab
   instance <https://software.nersc.gov/>`__ before moving forward. See `here
   <https://confluence.slac.stanford.edu/display/LSSTDESC/Getting+a+NERSC+Computing+Account>`__
   for details on how DESC members get an account at NERSC.

Creating a mirror repository at GitLab
--------------------------------------

The instance `software.nersc.gov` currently does not have a premium GitLab
license, therefore it does not have features like in-built mirroring.

Therefore we must start by creating a ``mirror`` repository on the NERSC GitLab
instance ourselves. The sole purpose of the ``mirror`` repository is to
automatically clone our original code hosted by GitHub into a new duplicate
repository on the NERSC GitLab instance.  In the nomenclature of this tutorial,
the original GitHub repository is our ``source``, and the GitLab repository
automatically created and updated by the ``mirror`` repository is the ``target``.

The ``mirror`` repository only needs to contain two files: (1) a bash script
(``mirror.bash``) and a (2) GitLab CI workflow (``.gitlab-ci.yml``), which we
discuss in more detail later.

.. tip:: Call your ``mirror`` repository ``mirror-<GitHub-Repository-Name>``,
   e.g., for this example repository we would call our ``mirror`` repository
   ``mirror-desc-continous-integration``.

.. tip:: Instead of creating a ``mirror`` repository from scratch, you can copy
   the ``mirror-desc-continous-integration`` example repository and modify the
   ``.gitlab-ci.yml`` to your ``target`` and ``source`` repositories. 

Personal Access tokens
^^^^^^^^^^^^^^^^^^^^^^

To start, in the ``mirror`` repository you will need to declare personal access
tokens with sufficient scope to read and write to the ``source`` and ``target``
repositories.

The mirroring process is eventually done through a Bash script, where we expect
the Personal Access token of the ``source`` repository to be stored as
``MIRROR_SOURCE_PAT``, and the Personal Access token of the ``target``
repository as ``MIRROR_TARGET_PAT``.

Steps to create tokens from various sources are below:

#. `GitHub <https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token>`__

#. `GitLab <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`__. Instructions specifically for the NERSC GitLab instance are `here <https://software.nersc.gov/NERSC/nersc-ci-docs/-/wikis/Home#interacting-with-a-repository-through-api>`__.

#. `Bitbucket <https://confluence.atlassian.com/bitbucketserver/personal-access-tokens-939515499.html>`__

The ``MIRROR_TARGET_PAT`` will of course be made in the NERSC GitLab instance,
so follow the instructions for Gitlab.  The tokens are added in the ``mirror``
repository under Settings -> CI/CD -> Variables (make sure the chosen ``Role``
is "Maintainer").  It is important to mask these variables, so that they are
not visible in the logs.

.. image:: ../images/ci-variables.png

However, this does not protect the variables completely.  Additionally, ensure
that you do not add other users to this repository with high enough permissions
to read your variables/tokens or run jobs (or modify the ``mirror.bash`` where
they can be exposed through the script).

.. note:: Since the ``mirror`` repo contains personal access tokens (PAT) this
   repo should always be created by the users under their own usernamespace.
   There is no requirement to add others to this repo.  Creating the ``mirror``
   repo under a group may inadvertently grant visibility of the tokens to
   others, as ownership in GitLab flows from top to bottom.

Mirror repository files
^^^^^^^^^^^^^^^^^^^^^^^

Two files are required for the ``mirror`` repository, a Bash script which
performs the workings of the repository cloning, and a GitLab CI workflow to
trigger the Bash script to automatically run.

The ``mirror.bash`` file, shown below, is located in the
``gitlab_mirror_example`` directory of this repository, and provides a good
example of how to mirror.

.. literalinclude:: ../../gitlab_mirror_example/mirror.bash
   :language: bash
   :linenos:
   :caption: gitlab_mirror_example/mirror.bash

The ``git push target --prune`` command shows how to only push the ``main``
branch (and tags) of the ``source`` repository.  It is possible to target
multiple branches through this mechanism, however it not recommended to mirror
all branches by default.

Additionally, we also use the environment variable ``GIT_ASKPASS`` to provide
authentication tokens to git.  This ensures that the tokens are not visible in
the CLI which is an important requirement in multi-tenant hosts e.g. Cori
nodes.

.. note:: Most examples online for interacting with git repositories through
   tokens use something along the lines of
   ``https://username:access_token@github.com/username/repo_name.git``. Do not
   do this! always use the environment variable ``GIT_ASKPASS``. Additionally
   populate the variable as shown in ``mirror.bash``.

Similar to the workflows for GitHub Actions, GitLab workflows are defined in a
file named ``.gitlab-ci-yml``, which must reside in the root directory of your
repository. 

.. literalinclude:: ../../gitlab_mirror_example/.gitlab-ci.yml
   :language: yaml
   :linenos:
   :caption: gitlab_mirror_example/.gitlab-ci.yml

We will go into some more details of the GitLab CI format in the next section,
but briefly, the ``.gitlab-ci-yml`` workflow for the ``mirror`` repository,
shown above, is designed to execute the ``mirror.bash`` script when triggered
by a schedule, or when manually triggered through the GitLab API. It is here
where we define the paths to the ``source`` (``MIRROR_SOURCE_REPO``) and
``target`` (``MIRROR_TARGET_REPO``) repositories, which you will have to modify
for your needs. The ``SCHEDULER_PARAMETERS`` is where we define our compute
node allocation options for submitting to *Cori*, which we detail more later.

Step-by-step
^^^^^^^^^^^^

To recap, the steps are:

#. Create a blank ``mirror`` repository called
   ``mirror-<GitHub-Repository-Name>`` within your personal namespace on the
   NERSC GitLab instance.

#. Create a blank repository called ``<GitHub-Repository-Name>`` within your
   personal namespace on the NERSC GitLab instance. This will host the
   duplicate code from GitHub.

#. Create a Personal Access Token in the ``source`` GitHub repository (with read
   rights) and in the ``target`` GitLab duplicate repository you just created
   (with write rights, "Maintainer" role).

#. In the ``mirror`` repository, add the ``source`` (``MIRROR_SOURCE_PAT``) and
   ``target`` (``MIRROR_TARGET_PAT``) repositories Personal Access Tokens as
   masked CI/CD variables.

#. Copy the ``mirror.bash`` and ``.gitlab-ci.yml`` files from this repository
   to your ``mirror`` repository and update the ``MIRROR_SOURCE_REPO`` and
   ``MIRROR_TARGET_REPO`` parameters within ``.gitlab-ci.yml`` to the correct
   urls.

#. Trigger the pipeline manually through the GitLab API (CI/CD -> Pipelines ->
   Run pipeline) to ensure it works.

#. Add a schedule to automatically trigger the workflow daily from now on
   (CI/CD -> Schedules -> New Schedule). 

Building a GitLab CI workflow for your repository
-------------------------------------------------
