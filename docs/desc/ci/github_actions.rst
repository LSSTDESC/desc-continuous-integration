.. DESC CI test documentation master file, created by
   sphinx-quickstart on Mon Jun 20 11:41:18 2022.

.. _ci_using_github_actions:

GitHub Actions
==============

For DESC repositories we strongly encourage the use of *GitHub*'s automated
CI/CD workflow tool, `GitHub Actions <https://github.com/features/actions>`__.
With *GitHub Actions* you can automate, customize, and execute your software
development workflows right in your repository. In addition, you have access to
thousands of community created pre-built "Actions" to make the process of CI as
simple and efficient as possible.

CI with *GitHub Actions* is configured via "workflows", YAML configuration
files checked into the ``.github/workflows`` directory of your repository,
which will automatically run when triggered by an event in your repository,
when triggered manually, or at a defined schedule. A repository can have
multiple workflows, triggered independently, each of which can perform a
different set of tasks.

This guide is not designed to be a definitive tutorial on *GitHub Actions* (for
that see `here <https://docs.github.com/en/actions/quickstart>`__),  but to be
an entry point for getting you started with CI for your DESC software.

Our `demo repository
<https://github.com/LSSTDESC/desc-continuous-integration>`__ has four
workflows, of differing complexities, which we describe in detail in this
section. The goal of each example workflow is always the same, however, keeping
our software stable through any changes to the codebase by initiating the test
suite and ensuring they pass.  

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * -
     - YAML
     - What is does
   * - Example 1
     - ``ci_example_1.yml``
     - Install ``mydescpackage`` and run the test suite
   * - Example 2
     - ``ci_example_2.yml``
     - Future proof, lint and perform code-coverage to ``mydescpackage`` 
   * - Example 3
     - ``ci_example_3.yml``
     - Test ``mydescpackage`` within the *DESC* *Conda* environment using the *DESC* Docker image
   * - Example 4
     - ``ci_example_4.yml``
     - Test ``mydescpackage`` within the *DESC* *Conda* enviromnent (manual install)

For reference, the full workflows can be expanded below:

.. collapse:: Click to see Example 1 in full

    .. literalinclude:: ../../../.github/workflows/ci_example_1.yml
      :language: yaml
      :linenos:

.. collapse:: Click to see Example 2 in full

    .. literalinclude:: ../../../.github/workflows/ci_example_2.yml
      :language: yaml
      :linenos:

.. collapse:: Click to see Example 3 in full

    .. literalinclude:: ../../../.github/workflows/ci_example_3.yml
      :language: yaml
      :linenos:

.. collapse:: Click to see Example 4 in full

    .. literalinclude:: ../../../.github/workflows/ci_example_4.yml
      :language: yaml
      :linenos:

|

Example 1: A simple CI workflow
-------------------------------

Let's start simple, with an example CI workflow that automatically initiates
the repositories test suite when there is a push or pull request opened on the
``main`` branch. 

Triggering the workflow
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../.github/workflows/ci_example_1.yml
   :language: yaml
   :linenos:
   :lineno-start: 3
   :lines: 3-13

First, ``name:`` provides a reference tag to this workflow, handy for keeping
track of your workflows within the *GitHub Actions* API. 

Then, how and when we want our workflow to be triggered is listed under the
``on:`` parameter.  For this example, our workflow will be triggered whenever
there is a push or pull request onto the ``main`` branch. Connecting a CI
workflow to at least the main branch is an excellent practice, ensuring that
any proposed changes to the codebase of the primary branch cannot proceed until
they go through the required battery of unit tests, increasing our codes
stability.

There are naturally many more options that can be selected for ``on:``.  We can
trigger a CI workflow for pull requests, push requests, forks etc, to one or
many selected branches of the repository. One useful trigger is ``on:
workflow_dispatch``, which allows you to trigger the CI workflow manually
through the *GitHub Actions* API, great for initially testing and debugging your
workflows.  You can also schedule your CI workflow to automatically run at
periodic intervals. For a complete list of conditions from which you can
trigger your CI workflow see the documentation `here
<https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows>`__.

Testing our code in different environments 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../.github/workflows/ci_example_1.yml
   :language: yaml
   :linenos:
   :lineno-start: 15
   :lines: 15-32

Now we reach the main body of our workflow, marked ``jobs:``.  Workflows are
built from one or more jobs, with each job of a workflow defining its own
working environment and a set of practical instructions to perform, e.g.,
running the unit tests, constructing and deploying containers, statistics
reporting, etc. Note that by default each job in the workflow will operate
independently, allowing them to be run in parallel on different host machines.
However you can link your jobs to be sequentially dependent to one another if
desired. For our example there is only one job within the workflow, called
``ci-with-pytest``.

A ``job:`` starts with some global preferences (at the scope of only that job).
At a minimum, we must at least declare the desired host machine architecture
our job will run on, defined using the ``runs-on:`` parameter.  Luckily,
*GitHub* hosts "runners" (virtual machines) with various versions of Ubuntu,
MacOS and Windows that we can use to test on.  There is the capability to set
up your own self-hosted runner (if your code operates only on a particularly
unique architecture), but we do not cover that here.

Rather than restricting ourselves to testing our code on a single operating
system, or Python version, commonly we are going to want to test over a
reasonable range of operating systems and Python versions to accommodate the
eventualities of the widest possible userbase. In our example we want to test
our code using four versions of Python3 on the two most recent releases of
Ubuntu (denoted ``ubuntu-20.04``, and ``ubuntu-latest``) and the latest MacOS
release (``macos-latest``) [1]_. Whilst we could do this by declaring multiple
(almost identical) ``jobs:``, differing only in a few values (like
``runs-on:``), it is much cleaner and simpler to use a ``strategy:`` matrix.

A strategy matrix lets you use variables in a single job definition to
automatically create multiple job runs based on the combinations of the
variables. For example, our ``matrix:``, which can be thought of like a Python
dictionary, has two entries; ``python-version`` and ``os``, which both contain
a list of values.  This is telling *GitHub Actions* that we want to spawn an
independent job for each *cross-referenced* value(s) within these lists, i.e.,
twelve jobs, with each of those jobs having a unique combination of
``python-version`` and ``os`` stored within the globally accessible matrix.

   .. note:: The names in your matrix can be anything, ``python-version``
    and ``os`` are not explicitly built-in variable names. The entries in the
    matrix can be accessed at any point in the workflow via syntax like ``${{
    matrix.os }}``, the value of which will vary depending on the
    runner/spawned job. 

The ``fail-fast: false`` option tells *GitHub Actions* not to fail all the
spawned jobs of a workflow immediately if one job within the matrix fails
(which is the default behaviour).

Then, ``runs-on: ${{ matrix.os }}`` selects the *GitHub* hosted runner for this
job: four on ``ubuntu-20.04``, four on ``ubuntu-latest`` and four on
``macos-latest`` (for the four versions of Python we are testing).

The steps of a job
^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../.github/workflows/ci_example_1.yml
   :language: yaml
   :linenos:
   :lineno-start: 34
   :lines: 34-54

Last but not least is the of step-by-step instructions for our
``ci-with-pytest`` job, listed as a series of individual ``steps:``. A
``uses:`` step denotes an "*GitHub Action*", a community constructed code
snippet that performs a predefined task [2]_, whereas a ``run:`` step directly
executes a command on the host machine. Steps are run in sequence.

Our example job has four steps:

1. Checkout this repository to the host machine using the
   ``actions/checkout@v3`` pre-built action. This will almost always be one of
   the first steps in your workflow. Note the ``@v3`` tag directly requests the
   release version of the action we want to use.
2. Use the ``actions/setup-python@v4`` action to install the desired version of
   Python on the host machine. Note some actions accept arguments (``with:``),
   this action accepts the Python version you wish to install, for example,
   which we take from our strategy matrix.
3. Install ``mydescpackage`` using ``pip``.
4. Finally, run our test suite using ``pytest``.

We can monitor the output from each of these steps individually through the
*GitHub Actions* API. If a step in our job fails, the job will be aborted, and
we must fix it before the codebase receives any changes

.. note:: You can run multiple command line inputs within a single ``run:`` by
  preceding the commands with the pipe symbol (``|``).

.. [1] See `here <https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners>`__ for a complete list of GitHub hosted runners.
.. [2] Check out the `GitHub marketplace <https://github.com/marketplace?type=actions>`__ for a list of community actions.

Example 2: Going beyond just testing
------------------------------------

Here we show a second example, very similar to the first, but it demonstrates
some additional features you may wish to take advantage of within your CI
workflow.

Future proofing
^^^^^^^^^^^^^^^

.. literalinclude:: ../../../.github/workflows/ci_example_2.yml
   :language: yaml
   :linenos:
   :lineno-start: 16
   :lines: 16-39

Say we want to consider a version of the operating system, or Python, that we
are not yet willing to fully support, but we may migrate to it in the future.
It could be useful to already test our codes within these more modern
environments, with the caveat that we are not that worried if they fail the CI.
Indeed, this is a useful way to preemptively capture any versioning or
compatibility bugs that may arise in the future before we fully migrate.  The
key is, however, that for the operating system or Python versions that we are
not yet willing to fully support, we do not want those experimental CI jobs to
fail our entire workflow.

To do this, first we manually add a job of a particular setup to our strategy
matrix using the ``include:`` parameter. Here we are experimenting on
``ubuntu-latest`` and only on ``python==3.11``. To tell *GitHub Actions* not to
worry if this particular job fails, but to remain worried if the other jobs in
our matrix fail, we add an ``experimental`` value to our matrix, which, if
true, means that the CI workflow will complete even if this job fails (which we
tell *GitHub Actions* via ``continue-on-error: ${{ matrix.experimental }}``).    

Code formatting/linting
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../../.github/workflows/ci_example_2.yml
   :language: yaml
   :linenos:
   :lineno-start: 62
   :lines: 62-64

Tidy and readable code is a healthy practice. When multiple developers are
working on a single project, or when a codebase is being handed over to another
team, clashes in programming styles can cause difficulties for maintaining and
debugging. This is the reason why many programmers try to adhere to a coding
style convention during development, most commonly the "PEP 8" style
convention.   

We can keep on top of coding style practices within our CI through code
"linting". There are many fantastic tools that can lint our Python code and
report any violations of the selected coding style. For our example we are
using the ``flake8`` Python linting tool. You can enforce up to an arbitrary
level of strictness depending on your needs, here we only demonstrate checking
for indentation and syntax errors in the code files.  However you could be
stricter, ensuring no trailing/leading whitespaces, line length limits, etc
(see the Flake8 documentation for a full list of error and warning codes). In
addition, ``--count`` prints the total number of errors found,
``--show_source`` will print the source code generating the error/warning in
question, ``--statistics`` counts the number of occurrences of each
error/warning code and prints a report, and ``--select=`` specifies the list of
error codes we wish Flake8 to check.

.. note:: If you want to report how well your code meets the PEP 8 standards,
   but do not want it to fail your CI, include the ``--exit-zero`` parameter.
   You could run Flake8 an additional time, more strictly than before, but only
   report the findings rather than failing the workflow, for example. 


Code coverage
^^^^^^^^^^^^^

.. literalinclude:: ../../../.github/workflows/ci_example_2.yml
   :language: yaml
   :linenos:
   :lineno-start: 66
   :lines: 66-72

The goal of a test suite is to cover many plausible scenarios that our code may
encounter during general use. However it can be challenging, particularly if
the code is complex, to know how much of our codebase our unit tests touch, a
metric referred to as "code coverage". Ideally we want our test suite to cover
as large a proportion of the codebase as possible, with the idea that a larger
coverage aids towards increased stability. There are many tools in Python to
automatically establish the coverage of the test suite, and whilst there are
caveats to exactly what metric of coverage is the most useful to report, a
basic code coverage statistic can be a very useful first step for
establishing the scope of your test suite.

Note that we need ``pytest-cov`` as a dependency (listed in our
``pyproject.toml``), and have requested ``pytest`` to output a coverage report.
In theory this is enough, we could check the coverage report for our test suite
in the *GitHub Actions* API. However it can also be useful to upload the
coverage report to a site like *codecov.io* to disseminate the report more
thoroughly.  This also allows us to create a visible code coverage badge on the
front page of the repository (see the ``README.md`` file for the syntax on how
to add the badge).

CI and the DESC Python environment
----------------------------------

If your software is a dependency for other DESC packages, or it builds into a
larger DESC pipeline, this can also be considered within the CI workflow. As
part of the DESC release management strategy, there exist independent CI
workflows designed to perform on complete DESC pipelines to ensure they remain
stable through any changes to the individual dependent repositories (see
:ref:`ci_desc_pipelines`). However we can already assist for this at the
individual repository level, by ensuring that our software operates as expected
within the ``desc-python`` *Conda* environment. This will mitigate, as much as
possible, versioning and dependency conflicts between the DESC packages when
they come together to form the pipeline.   

Setting up a CI workflow to operate within the ``desc-python`` *Conda*
environment only requires a few steps, and can be done in two ways: (1) working
within a DESC *Docker* container which has the ``desc-python`` *Conda*
environment pre-installed (recommended), or (2) manually installing the
``desc-python`` *Conda* environment on the host machine by utilizing the YAML
setup files within the `desc-python
<https://github.com/LSSTDESC/desc-python>`__ repository.

Example 3: Testing within the DESC *Conda* environment (docker image)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    "*A container is a standard unit of software that packages up code and all
    its dependencies so the application runs quickly and reliably from one
    computing environment to another. A Docker container image is a
    lightweight, standalone, executable package of software that includes
    everything needed to run an application: code, runtime, system tools,
    system libraries and settings.*"

    -- `DockerHub <https://www.docker.com/resources/what-container/>`__

Working within a DESC *Docker* container is the quickest and simplest way to
test code within the ``desc-python`` *Conda* environment. LSST-DESC has a large
array of container images hosted by DockerHub (`full list here
<https://hub.docker.com/u/lsstdesc>`__) exactly for this purpose, and linking
*GitHub Actions* to these container images is also seamless and
straightforward. 

Example 3 performs very similarly to example 2, however we no longer need to
install Python or any dependencies onto the host machine, but instead include
the line

.. literalinclude:: ../../../.github/workflows/ci_example_3.yml
   :language: yaml
   :linenos:
   :lineno-start: 32
   :lines: 32-33

to tell *GitHub Actions* that we wish to download and operate the entirety of
the ``ci-with-pytest`` job within this container.

The naming convention for CI-based LSST-DESC container images includes both the
operating system version and Python version, and has a ``:ci-dev`` tag which
is necessary to include.

Our matrix in the case of this example

.. literalinclude:: ../../../.github/workflows/ci_example_3.yml
   :language: yaml
   :linenos:
   :lineno-start: 25
   :lines: 25-27

is used to specify which container image to work within, and not the of *GitHub
actions* host runner, as was the case for the previous examples. We always
select ``ubuntu-latest`` host machines to operate on (however this choice is
largely arbitrary as we are operating within a container on the machine
anyway).   

.. note:: Only Ubuntu host machines support container images. To operate within
   the ``desc-python`` *Conda* environment using a MacOS architecture you will
   need to install the environment manually (see next example).

The downside of operating within containers is the setup overhead (containers
can be many gigabytes that have to be downloaded and extracted). To that end,
we recommend two workflows for your Python packages, one that only installs the
dependencies needed to get your code working (like the examples 1 & 2), and a
second workflow that operates within the DESC container, but on a schedule. For
example, here we trigger our workflow every Friday at midnight, 

.. literalinclude:: ../../../.github/workflows/ci_example_3.yml
   :language: yaml
   :linenos:
   :lineno-start: 7
   :lines: 7-9

(see `here
<https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule>`__
for more details on scheduling your workflows).

.. note:: If you have Python dependencies that are not part of the
   ``desc-python`` environment, you will have to install them yourself manually
   after. For example ``pytest-cov`` will be installed when we install
   ``mydescpackage``. As this is a package needed only for the CI workflow
   there is no real need to add it to the ``desc-python`` environment. However,
   if your software requires an additional package to operate you can request
   its inclusion by raising an issue at the ``desc-python`` repository.

Example 4: Testing within the DESC *Conda* environment (manual install)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If for some reason you cannot use the DESC containers, or you need to test your
code on MacOS architecture, you can install the ``python-desc`` *Conda*
environment on the host machine manually. 

The most up-to-date version of the ``python-desc`` *Conda* environment can be
found in `this <https://github.com/LSSTDESC/desc-python>`__ DESC repository,
which we can call upon during our CI workflow.

.. literalinclude:: ../../../.github/workflows/ci_example_4.yml
   :language: yaml
   :linenos:
   :lineno-start: 40
   :lines: 40-45

First we checkout the ``desc-python`` repository. Note we do this using the
same *GitHub Action* as we have been using to checkout our own repository
(which is the default behaviour), but now we are telling the Action to checkout
a specified *GitHub* repository (``repository:``) into a specified directory on
the host machine (``path:``).

.. literalinclude:: ../../../.github/workflows/ci_example_4.yml
   :language: yaml
   :linenos:
   :lineno-start: 47
   :lines: 47-62

Next we use another *GitHub Action* to install *MiniConda* onto the host
machine, specifying the Python version and that we wish to setup and to
activate the *Conda* ``base`` environment. Then we install the ``desc-python``
environment packages from the YAML files to the base environment. We use
*Mamba* to resolve the environment, which is generally much quicker for
resolving complex environments.

.. literalinclude:: ../../../.github/workflows/ci_example_4.yml
   :language: yaml
   :linenos:
   :lineno-start: 15
   :lines: 15-19

One extra step is on line 18, where we have specified the
``default:`` ``shell: bash -l {0}``, which is required for *MiniConda* to
activate environments.
