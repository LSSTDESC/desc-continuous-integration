.. DESC CI test documentation master file, created by
   sphinx-quickstart on Mon Jun 20 11:41:18 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Example CI workflows from DESC repositories 
===========================================

Here we show a brief selection of CI workflows taken from some activate DESC
repositories, break them down, and discuss their workings. These demonstrate CI
at DESC in action, whilst also demonstrating some additional capabilities of
GitHub Actions beyond the basic examples in the previous section, and what
extra steps we may need to perform to get our CI working.  

The DESC CI workflows were taken from the repositories on July 2022.

CCL (`The Core Cosmology Library <https://github.com/LSSTDESC/CCL>`__)
----------------------------------------------------------------------

.. literalinclude:: ../../desc_ci_workflows/ccl.yml
   :language: yaml
   :linenos:

#. The workflow is trigged by push requests to the ``main``, ``master`` or any
   ``release`` branch. It is also triggered by a pull request to any branch.
#. There is one job in the workflow, called ``build``, which uses a
   ``strategy:`` ``matrix:`` to spawn two jobs, testing the code on Ubuntu and
   MacOS, both using Python version 3.8.
#. Now the steps of the ``build`` job.

    #. The ``styfle/cancel-workflow-action@0.6.0`` Action is called to cancel
       any previous CI workflows that are still currently running.
    #. The ``actions/checkout@v2`` Action is called to checkout the repository
       onto the host machine.
    #. The ``conda-incubator/setup-miniconda@v2`` Action is called to install
       MiniConda onto the host machine with the specified version of
       Python from the strategy matrix.
    #. If this is the ``macos-10.15`` runner, uninstall the HomeBrew package
       manager.
    #. Lint the code in the ``pyccl`` and ``benchmarks`` folders using
       ``Flake8``.
    #. Install the Python dependencies using ``mamba``. 
    #. Install CLASS (Cosmic Linear Anisotropy Solving System) using the
       correct script (depending on the runner) within the ``ci_scripts``
       directory.
    #. Build CCL using ``setup.py``.
    #. Run the unit tests using ``pytest``.
    #. Upload code coverage results output by ``pytest``.

This example has quite a bit more setup to get the host machine ready for the
unit tests compared to the simple examples in the previous section,
particularly to accommodate for testing on the MacOS operating system. Below is
a few more details about the GitHub Actions syntax not covered by the examples
in the previous section.

.. note:: You can evaluate expressions in workflows to give you more control on
  what part of your workflows run under certain conditions. For example the
  ``if:`` expression on line 43. See the documentation `here
  <https://docs.github.com/en/actions/learn-github-actions/expressions>`__ for
  more details.

.. note:: You can set environment variables on the host machine using ``env:``.
   The scope of these variables depends on where they are set. For example
   ``MATRIX_OS`` set on line 76 is only visible for the commands within the
   ``install deps`` job.

imSim
-----

.. literalinclude:: ../../desc_ci_workflows/imsim.yml
   :language: yaml
   :linenos:

#. The workflow is trigged by push and pull requests to the ``main`` and
   ``release`` branches.
#. There is one job in the workflow, called ``build``, which uses a
   ``strategy:`` ``matrix:`` to spawn one job, testing the code on Ubuntu and
   using Python version 3.8.
#. Now the steps of the ``build`` job.

    #. The ``actions/checkout@v2`` Action is called to checkout the repository
       onto the host machine.
    #. The ``conda-incubator/setup-miniconda@v2`` Action is called to install
       MiniConda onto the host machine with a specified condarc file.
    #. Install ``mambda`` and use it to install dependencies from the
       ``conda_requirements.txt`` file.
    #. Install any dependencies not on Conda using pip.
    #. Install imSim and GalSim onto the host machine.
    #. Install dependencies needed for testing.
    #. Run unit tests.


