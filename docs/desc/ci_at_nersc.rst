CI at NERSC using GitLab
========================

For the majority of cases the GitHub-hosted runners available through GitHub
Actions are more than sufficient to test and maintain code stability for DESC
repositories.

However, some DESC software repositories would benefit greatly by having the
ability to deploy CI workflows directly on the *Cori* and *Perlmutter* machines
at `NERSC <https://www.nersc.gov/>`__. This would allow the software to be
tested more intensely within an HPC environment, give access to specific
development tools at NERSC, and give the ability to test the code against the
large datasets hosted at the facility, for example.

As there is no way to link CI workflows using GitHub Actions to the NERSC
facilities directly, we require a bit of a workaround:

#. Mirror the repository to the `NERSC GitLab instance <https://software.nersc.gov/>`__
   where we have direct access to the *Cori* and *Perlmutter* machines.

#. Implement a CI workflow using GitLab's builtin CI tools (similar to GitHub
   Actions).

#. Report the results back to GitHub.

Below is a schematic of the process.

.. image:: ../images/repo-flow.png

Here we go over the steps required to implement a CI workflow at NERSC starting
from a GitHub repository, for the example of our test repository. The goal is
the same as before, to trigger the repositories' test suite when changes to the
repositories' codebase are made.  The difference now being that these tests
will be performed directly on *Cori*, and not on a GitHub Actions-hosted
runner.

.. note:: You will need a NERSC account and access to the `NERSC GitLab
   instance <https://software.nersc.gov/>`__ before moving forward. See `here
   <https://confluence.slac.stanford.edu/display/LSSTDESC/Getting+a+NERSC+Computing+Account>`__
   for details on how DESC members get an account at NERSC.

Getting set up
--------------

The instance `software.nersc.gov` currently does not have a premium GitLab
license, therefore it does not have features like in-built mirroring.

This means there is a bit of manual setup required in order to get started with
CI at NERSC when starting from GitHub, however once setup, the process is fully
automated. 

Start by creating three **blank** repositories on the NERSC GitLab instance:

#. A ``target`` repository, with the same name as the GitHub ``source``
   repository (e.g, ``desc-continuous-integration``). This can be created in any
   namespace/group.  The CI eventual workflow is performed here, therefore those
   needing access to the CI logs should have this repository visible to them.

#. A ``mirror`` repository, whose job is to clone the GitHub ``source``
   repository to the GitLab ``target`` repository (e.g.,
   ``mirror-desc-continuous-integration``). This repository must be created in
   your private namespace.

#. A ``status`` repository, whose job is to report the status of the CI job
   performed at the GitLab repository back to the GitHub ``source`` repository
   (e.g., ``status-desc-continuous-integration``). This repository must be created
   in your private namespace.

.. figure:: ../images/create_blank_repo.png
	:class: with-border

	Figure 1: Example of creating a blank repository on GitLab.

.. figure:: ../images/three_repos.png
	:class: with-border

	Figure 2: At the end you should have three empty repositories on GitLab.

Personal Access tokens
^^^^^^^^^^^^^^^^^^^^^^

Personal access tokens (PATs) are an alternative to using passwords for
authentication to GitHub or GitLab when using the API or the command line. We
need to set up PATs between our repositories in order for them to communicate
through our CI pipeline.

#. In the GitHub ``source`` repository, in your user profile go to Settings ->
   Developer settings -> Personal Access Tokens -> Generate New Token. Give the
   token a "Note", say "NERSC CI", and tick "workflow". Then generate the token.
   Copy the generated PAT, go to the ``mirror`` repository, in Settings -> CI/CD
   -> Variables, add a variable ``MIRROR_SOURCE_PAT`` with the value of the
   generated PAT from the ``source`` repo (make sure to tick masked). Now go to
   the ``status`` repository and add a CI/CD variable ``STATUS_TARGET_PAT`` with
   again the same PAT as the value. 

#. In the GitLab ``target`` repository create a PAT by going to Settings ->
   Access Tokens. Give the token a name, say "mirror-repo", chose an expiration
   date, keep the role as "Maintainer", and tick "write_repository". Create the
   token, and add it to the ``mirror`` repository CI/CD variables as
   ``MIRROR_TARGET_PAT`` (make sure to tick masked). Now go to the ``status``
   repository and add the PAT as a CI/CD variable ``STATUS_SOURCE_PAT``. 

.. note:: The ``mirror`` and ``status`` repositories should be created in your
	private namespace, so only you have access. This is to protect the PATs stored
	within them. Do not share these tokens with anyone, this is the equivalent of
	password sharing.

.. note:: Always mask PATs stored as CI/CD variables. This prevents them from
	being displayed within the CI workflow output.

.. note:: PATs have an expiration date, you will have to periodically create
	new PATs.

Trigger tokens
^^^^^^^^^^^^^^

In order for our GitHub -> GitLab -> GitHub pipeline to work seamlessly behind
the scenes, we will have to trigger the CI workflows of each repository in
sequence one after the other. This is done through "Trigger tokens", which let
us remotely trigger CI workflows within our repositories. 

#. In the ``mirror`` repository, go to Settings -> CI/CD -> Pipeline triggers
   and create a trigger token with the description "trigger-from-github".  Copy
   the created trigger token, go to the ``source`` repository on GitHub, and add
   the generate trigger token as a *Secret* under Settings -> Secrets -> Actions
   with the name ``MIRROR_TRIGGER_TOKEN``.

#. Go to the ``target`` repository and create a trigger token called
   "trigger-from-mirror". Add this one to the ``mirror`` repository as a CI/CD
   variable called ``TARGET_TRIGGER_TOKEN``.

#. Go to the ``status`` repository and create a trigger token called 
   "trigger-from-target". Add this one to the ``target`` repository as a CI/CD
   variable called ``STATUS_TRIGGER_TOKEN``.

.. note:: Trigger tokens do not expire, but be sure to keep the variables masked.

Mirror repository files
^^^^^^^^^^^^^^^^^^^^^^^

Copy the two files from the ``./gitlab/mirror_repo_files/`` directory in to the
``mirror`` repository. 

The ``mirror.bash`` file, shown below, is a Bash script that automatically
clones the ``source`` GitHub repository files to the ``target`` GitLab repository. 

.. literalinclude:: ../../gitlab/mirror_repo_files/mirror.bash
   :language: bash
   :linenos:
   :caption: ./gitlab/mirro_repo_files/mirror.bash

The ``git push target --prune`` means we are only pushing the ``main`` branch
(and tags) of the ``source`` repository.  It is possible to target multiple
branches through this mechanism, however it not recommended to mirror all
branches by default.

Additionally, we also use the environment variable ``GIT_ASKPASS`` to provide
authentication tokens to git.  This ensures that the tokens are not visible in
the CLI which is an important requirement in multi-tenant hosts e.g. *Cori*
nodes.

The second file is the GitLab CI workflow. Similar to the workflows for GitHub
Actions we covered in the previous section, GitLab workflows are defined in a
file named ``.gitlab-ci.yml``, which must reside in the root directory of your
repository. 

.. literalinclude:: ../../gitlab/mirror_repo_files/.gitlab-ci.yml
   :language: yaml
   :linenos:
   :caption: ./gitlab/mirror_repo_files/.gitlab-ci.yml

We will go into detail of the GitLab CI format in the next section, but
briefly:

* The workflow is triggered automatically from GitHub using the trigger token.

* It runs the ``mirror.bash`` script, which mirrors the files from
  ``MIRROR_SOURCE_REPO`` in to ``MIRROR_TARGET_REPO``.

* It finishes by triggering the CI workflow in ``MIRROR_TARGET_REPO`` to
  continue the pipeline.

.. note:: You will have to modify the ``.gitlab-ci.yml`` file to point to your
	``MIRROR_SOURCE_REPO`` (on GitHub) and ``MIRROR_TARGET_REPO`` (on GitLab). You
	will also have modify the value of ``GITLAB_PROJECT_NUMBER``, the integer
	project number of your ``target`` repository on GitLab. The
	``SCHEDULER_PARAMETERS`` is where we define our compute node allocation options
	for submitting to *Cori*, which we detail more later.

Status repository files
^^^^^^^^^^^^^^^^^^^^^^^

Copy the two files from the ``./gitlab/status_repo_files/`` directory in to the
``status`` repository.

The ``status-github.py`` file, shown below, is a Python script that
automatically adds the CI status/result from the ``target`` repository on
GitLab to the ``source`` repository on GitHub.

.. literalinclude:: ../../gitlab/status_repo_files/status-github.py
   :language: python
   :linenos:
   :caption: ./gitlab/status_repo_files/status-github.py

The second file is the GitLab CI workflow.

.. literalinclude:: ../../gitlab/status_repo_files/.gitlab-ci.yml
   :language: yaml
   :linenos:
   :caption: ./gitlab/status_repo_files/.gitlab-ci.yml

.. note:: You will have to modify the ``.gitlab-ci.yml`` file to point to your
    ``STATUS_SOURCE_REPO`` (on GitLab) and ``STATUS_TARGET_REPO`` (on GitHub).

Triggering the CI workflow pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The final file to create is a GitHub Actions CI workflow to initiate the pipeline.

The ``ci_nersc.yml`` workflow in the ``.github/workflows/`` gives a good
example of how to do this. 

.. literalinclude:: ../../.github/workflows/ci_nersc.yml
   :language: yaml
   :linenos:
   :caption: ci_nersc.yml

Essentially, all we are doing is kick-starting the pipeline (in this example
manually) by initiating the ``mirror`` repositories CI workflow. You can
trigger the pipeline however you wish, however remember the examples in this
tutorial only work for the ``main`` branch, and each trigger will run a CI job
at NERSC.

.. note:: You will have to modify ``GITLAB_PROJECT_NUMBER`` to the GitLab
	project number of your mirror repository.

Building a GitLab CI workflow for your repository
-------------------------------------------------

Now that we are set up, we can think about how to perform CI at GitLab,
relating back to what we have learnt from using GitHub actions in the previous
examples.

Things to think about with CI at NERSC
--------------------------------------

.. note:: When deploying a CI workflow to *Cori* you are running code in the
   same environment, with the same permissions, as if you were working on a
   login node. Therefore things like ``$HOME`` refer to your real home
   directory, and you need to be careful about what scope your give to your CI
   workflows at NERSC.  As the developer, you are responsible for the code that
   is run, and you need to fully understand what is happening in the workflow
   that you are implementing.

.. note:: It is not recommended that you mirror code that you yourself do not
   own, unless they are from protected branches.

.. note:: Any code you mirror onto the NERSC GitLab instance must adhere to the
   broader NERSC user policy.
