.. DESC CI test documentation master file, created by
   sphinx-quickstart on Mon Jun 20 11:41:18 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Example CI workflows from DESC repositories 
===========================================

Here we quickly overview a brief selection of CI workflows taken from activate
DESC repositories. These demonstrate CI at DESC in action.

We go through each example step-by-step, highlighting any additional
capabilities of GitHub Actions CI workflows that were not covered by the
examples in the previous section.

The DESC CI workflows were taken from the repositories on August 2022.

`The Core Cosmology Library <https://github.com/LSSTDESC/CCL>`__
----------------------------------------------------------------

.. literalinclude:: ../../desc_ci_workflows/ccl.yml
   :language: yaml
   :linenos:

* The workflow is trigged by push requests to the ``main``, ``master`` or any
  ``release`` branch. It is also triggered by a pull request to any branch.

* There is one job in the workflow, called ``build``, which uses a
  ``strategy:`` ``matrix:`` to spawn two jobs, testing the code on Ubuntu and
  MacOS, both using Python version 3.8.

* Now the steps of the ``build`` job.

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

   #. Install the Python dependencies using ``mamba`` (see note below about
      setting the environment variables in this step).

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

.. note:: You can download resources onto the host machine using terminal
   commands just like you would on your own machine (using ``wget``, ``curl``,
   etc). 

.. note:: You can evaluate expressions in workflows to give you more control on
  what part of your workflows run under certain conditions. For example the
  ``if:`` expression on line 43. See the documentation `here
  <https://docs.github.com/en/actions/learn-github-actions/expressions>`__ for
  more details.

.. note:: You can set environment variables on the host machine using ``env:``.
   The scope of these variables depends on where they are set. For example
   ``MATRIX_OS`` set on line 76 is only visible for the commands within the
   ``install deps`` job.

.. note:: You can also set environment variables within a step that are
   available to any subsequent steps in a workflow job by defining or updating
   the environment variable and writing this to the ``GITHUB_ENV`` environment
   file (see lines 68-75). The step that creates or updates the environment
   variable does not have access to the new value, but all subsequent steps in
   a job will have access.

`imSim <https://github.com/LSSTDESC/imSim>`__
---------------------------------------------

.. literalinclude:: ../../desc_ci_workflows/imsim.yml
   :language: yaml
   :linenos:

* The workflow is trigged by push and pull requests to the ``main`` and
  ``release`` branches.

* There is one job in the workflow, called ``build``, which uses a
  ``strategy:`` ``matrix:`` to spawn one job, testing the code on Ubuntu using
  Python version 3.8.

* Now the steps of the ``build`` job.

    #. The ``actions/checkout@v2`` Action is called to checkout the repository
       onto the host machine.
 
    #. The ``conda-incubator/setup-miniconda@v2`` Action is called to install
       MiniConda onto the host machine with a specified condarc file.
    
    #. Install ``mambda`` and use it to install dependencies from the
       ``conda_requirements.txt`` file.
    
    #. Install any dependencies not on Conda using ``pip``.
   
    #. Manually install ``rubin_sim`` and download skybrightness and throughputs catalogs.

    #. Install imSim onto the host machine using ``pip``.
    
    #. Install GalSim onto the host machine using ``pip``.

    #. Install dependencies needed for testing.
    
    #. Run unit tests.

`tables_io <https://github.com/LSSTDESC/tables_io>`__
-----------------------------------------------------

.. literalinclude:: ../../desc_ci_workflows/tables_io.yml
   :language: yaml
   :linenos:

* The workflow is trigged by push and pull requests to the ``main`` branch.

* There is one job in the workflow, called ``build``, which uses a
  ``strategy:`` ``matrix:`` to spawn three jobs, testing the code on Ubuntu using 
  Python versions 3.7, 3.8 and 3.9.

* Now the steps of the ``build`` job.

    #. The ``actions/checkout@v2`` Action is called to checkout the repository
       onto the host machine.
 
    #. The ``actions/setup-python@v2`` Action is called to install the
       specified version of Python onto the host machine.
    
    #. Install ``OpenMPI``, ``pip`` and Python dependencies, then reinstall
       ``h5py`` with parallel support.
    
    #. Lint the code using ``pylint``.
   
    #. Run unit tests.

    #. Upload code coverage results.

.. note:: Testing your code on many different Python versions is a great way to
   keep your code stable for a wide userbase. However, a mixture of many
   packages to be used on many version of Python can create conflicts when
   installing dependencies open endedly (i.e., when not specifying the package
   versions when installing). In some cases, like for the dependency list in
   this repository, you will have to manually guide towards the correct
   versions (or version ranges) for your package dependencies, depending on the
   version of Python you are using.  This can be done in the
   ``requirements.txt`` file used for installing dependencies. For example,
   ``numpy>=1.21.0;python_version>="3.8"`` says only install ``numpy`` versions
   1.21.0 or higher if the Python version is 3.8.   
