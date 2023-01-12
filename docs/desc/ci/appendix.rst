Quick-example ``pyproject.toml``
================================

An example ``pyprojet.toml`` configuration file, used for the demo code in the
``desc-continuous-integraion`` repository.

.. literalinclude:: ../../../pyproject.toml
   :language: toml
   :linenos:

Quick-example ``ci_workflow.yml``
=================================

An example Continuous Integration YAML workflow
(``.github/workflows/ci_example_2.yml`` in the ``desc-continuous-integraion``
repository). More details in :ref:`ci_using_github_actions`.

.. literalinclude:: ../../../.github/workflows/ci_example_2.yml
   :language: yaml
   :linenos:

.. _nersc-ci-appendix:

NERSC CI files
==============

Below are some details of the workings of the ``mirror`` and ``target``
repositories' CI workflows.

Mirror repository files
-----------------------

The purpose of the ``mirror`` repository is to clone the contents of the
``source`` repository at GitHub to the ``target`` repository at the NERSC
GitLab instance. This is done through a simple CI workflow (``.gitlab-ci.yml``)
which runs a simple Bash script (``mirror.bash``), and is automatically
triggered from the CI workflow at the GitHub ``source`` repository.

The two files that make up the CI workflow for the ``mirror`` repository are
detailed below.

.. literalinclude:: ../../../examples/nersc_gitlab/mirror_repo_files/mirror.bash
   :language: bash
   :linenos:
   :caption: ./gitlab/mirror_repo_files/mirror.bash

The ``git push target --prune`` means we are only pushing the
``$GITHUB_SOURCE_BRANCH`` branch (and tags) of the ``source`` repository (which
will likely be your ``main`` or ``master`` branch).  It is possible to target
multiple branches through this mechanism, however it not recommended to mirror
all branches by default.

Additionally, we also use the environment variable ``GIT_ASKPASS`` to provide
authentication tokens to git.  This ensures that the tokens are not visible in
the CLI which is an important requirement in multi-tenant hosts e.g. *Cori*
nodes.

.. literalinclude:: ../../../examples/nersc_gitlab/mirror_repo_files/.gitlab-ci.yml
   :language: yaml
   :linenos:
   :caption: ./gitlab/mirror_repo_files/.gitlab-ci.yml

Similar to the workflows for GitHub Actions, GitLab workflows are defined in a
file named ``.gitlab-ci.yml``, which must reside in the root directory of your
repository.

This workflow...

* can only be triggered via a trigger token (which comes from the GitHub CI
  job).

* runs the ``mirror.bash`` script, which clones the ``source`` repository into
  the ``target`` repository.

* automatically triggers the CI workflow of the ``target`` repository, which
  continues the pipeline.

When submitting a CI workflow to *Cori* you must include the queue submission
parameters, passed as the environment variable ``SCHEDULER_PARAMETERS``. The
format is the same as if you were submitting a standard job at NERSC. Our job
(cloning a repository) is very quick, so we are submitting to the ``debug``
queue. However if you need a longer job runtime, or want to charge the time to
a particular project, you will need to modify these parameters accordingly.

.. note:: The repo URLs (``GITLAB_TARGET_REPO`` etc) and project numbers
   (``GITLAB_TARGET_PROJECT_NUMBER`` etc) have been passed through along with
   the trigger token, originally defined in the ``source`` CI workflow.

Status repository files
-----------------------

The ``status-github.py`` file, shown below, is a Python script that
automatically appends the CI workflow result from the ``target`` repository on
GitLab to the ``source`` repository on GitHub.

.. literalinclude:: ../../../examples/nersc_gitlab/status_repo_files/status-github.py
   :language: python
   :linenos:
   :caption: ./gitlab/status_repo_files/status-github.py

The second file is the GitLab CI workflow.

.. literalinclude:: ../../../examples/nersc_gitlab/status_repo_files/.gitlab-ci.yml
   :language: yaml
   :linenos:
   :caption: ./gitlab/status_repo_files/.gitlab-ci.yml

This is very similar to the ``mirror`` repository workflow, see above for details.
