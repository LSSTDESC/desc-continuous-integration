Building a Python package
=========================

The "*standard*" way of building a Python package has gone through many changes
in recent years, and if you have not been keeping track it can be difficult to
know the best approach for creating a package that is easy to install, easy to
maintain, and easy to publish. 

Here we go over the (relatively) new standard for Python packaging, the
all-encompassing ``pyproject.toml`` file. We strongly recommend developers at
DESC consider migrating to this new packaging standard, if you haven't already,
particularly when starting a new software project from scratch. The intuitive,
clean and maintainable format of ``pyproject.toml`` packages makes them both
easy to develop and publish with a minimal amount of effort. 

This guide assumes some basic knowledge of putting together a piece of Python
software, such as creating your own modules, etc. For those new to Python
software, check out the `official Python guide
<https://docs.python.org/3/tutorial/modules.html#packages>`__ to get started.
Also note this is by no means an exhaustive tutorial on the subject of Python
packaging. A great additional resource for that is the `Python Packaging Guide
<https://packaging.python.org/en/latest/tutorials/packaging-projects/#>`__
itself, or the guide from `RealPython
<https://realpython.com/pypi-publish-python-package/>`__.

Much of this guide is written under the assumption that the Python package you
are creating will be hosted by the `DESC GitHub repository
<https://github.com/lsstDESC>`__, however the majority of the information will
still apply even if this is not the case. If you are not yet familiar with
`Git` or `GitHub`, or you need help getting setup on the `DESC GitHub
repository <https://github.com/lsstDESC>`__, checkout `this guide
<https://confluence.slac.stanford.edu/display/LSSTDESC/Getting+Started+with+Git+and+GitHub>`__
on the DESC Confluence page, or this more general `getting started
<https://github.com/drphilmarshall/GettingStarted#top>`__ guide for *Git*.  

The accompanying repository which hosts the demo Python package we will often
refer to in this guide can be found `here
<https://github.com/LSSTDESC/desc-continuous-integration>`__. The repositories
package, named ``mydescpackage``, is very simple, only consisting of a few
callable mathematical functions. You are welcome to download/fork it and use it
as a starting template for your Python project. 

.. note::

   For those wondering what a TOML file is, `TOML <https://toml.io/en/>`__ is a
   file format for configuration files, similar to YAML, it stands for "*Tom's
   Obvious Minimal Language*".

The directory structure
-----------------------

Let's get started, first we go over the general directory structure your Python
package should adhere to:

::

    /path/to/my/project/
    ├── README.md           
    ├── pyproject.toml      
    ├── LICENCE
    ├── .gitignore
    ├── src/                
    │   └── mydescpackage/      
    │       ├── __init__.py
    │       ├── _version.py
    │       ├── file1.py
    │       └── file2.py
    ├── tests/              
    │   ├── test1.py
    │   └── test2.py
    ├── .github/
    │   └── workflows/
    │       └── ci.yml
    └── docs/               


Note that not all of these files and directories are strictly required. As a
minimum you should have a ``README.md`` and ``pyproject.toml`` file in your
base project directory, and the code for your software should populate the
``src/mydescpackage/`` directory (replacing "mydescpackage" with the name of
your package).

What are these files and directories...

* ``README.md``: A simple markdown file, typically outlines the project, its
  requirements, installation instructions, authors, etc. The contents of this
  file will also be displayed on your *GitHub* projects' landing page. 

* ``pyproject.toml``: Where the build information, project dependencies,
  metadata, etc, of the Python package are stored (more in the next section).

* ``LICENCE``: Contains the license of the package, outlining any restrictions
  of its use. It is good practice to use a well-known license rather than a
  self-created license, such as; `GNU
  <https://www.gnu.org/licenses/gpl-3.0.en.html>`__, `Apache licence
  <https://www.apache.org/licenses/LICENSE-2.0>`__, `MIT license
  <https://opensource.org/licenses/MIT>`__ or `creative commons license
  <https://creativecommons.org/choose/>`__.

* ``.gitignore``: This file specifies intentionally untracked files that *Git*
  should ignore (see `here <https://git-scm.com/docs/gitignore>`__ for more
  details).

* ``src/mydescpackage/``: The code for your Python software goes here. 

* ``src/mydescpackage/_version.py``: Stores the version number of our Python
  package (see :ref:`automatic_versioning` for more details) 

* ``tests/``: Any unit tests of your Package go in here (see also our guide on
  :ref:`Continuous Integration <desc_ci_intro>`).

* ``.github/workflows/``: Your *GitHub Actions* Continuous Integration
  workflows go in here (see our guide on :ref:`Continuous Integration
  <desc_ci_intro>` for more details on CI workflows).

* ``docs/``: For any extensive documentation beyond the scope of ``README.md``,
  *Read the Docs* files for example.

Once the directory structure is setup, and it is populated with our software,
we can move onto telling ``pip`` how to build and install our package.

.. note:: Many people prefer placing the source code in a ``src/`` directory,
   and not in the project's root directory.  This is a preference, and not a
   requirement, you can have a "flat" directory structure where
   ``mydescpackage/`` resides in the root project folder.  However, having a
   ``src/`` directory requires the user to first install the software before it
   can run, breaking the habit of running the source code directly within the
   root project directory (don't worry, you still only have to install the
   package once with an editable install, see more about this later on).

The ``pyproject.toml`` file
---------------------------

The ``pyproject.toml`` configuration file was introduced in `PEP518
<https://peps.python.org/pep-0518/>`__ as a way of specifying the minimum build
requirements when installing a Python package. This tells the system what
packages are required during the building process itself (e.g., ``setuptools``,
``wheel``), removing the onus of pre-installing any dependencies required to
build your package away form the user. The build requirements specified in
``pyproject.toml`` are installed in an isolated environment, used to build the
package, and later discarded, keeping your base environment clean and tidy.

Below we go over the ``pyproject.toml`` file from our `demo package
<https://github.com/LSSTDESC/desc-continuous-integration>`__.

.. collapse:: Click to expand pyproject.toml

    .. literalinclude:: ../../../pyproject.toml
      :language: toml
      :linenos:

|

The build system
^^^^^^^^^^^^^^^^

To specify which build-backend to use for installing your package, and any
requirements needed during the build process, include something like this at
the top of your ``pyproject.toml`` file.

.. literalinclude:: ../../../pyproject.toml
   :language: toml
   :linenos:
   :lineno-start: 1
   :lines: 1-3

Here we are saying we require the ``setuptools`` package during the build, and
we are going to use ``setuptools`` to build the our Python package as our
``build-backend``. Other common requirements during the build process are
``wheel`` and ``cython``. Note we select a specific version of ``setuptools``
to install, ``setuptools>=61.0``, as that is when ``setuptools`` became PEP 621
compliant (see project metadata later).

.. note:: You do not have to use ``setuptools`` as your ``build-backend``, you
   can use alternate Python package managers such as `Poetry
   <https://python-poetry.org/>`__, or `Flit
   <https://flit.pypa.io/en/stable/>`__. You can even put your own custom
   ``build-backend`` here if you have very specific requirements for building
   your package. However if you are unsure, stick with ``setuptools``.

In theory this is the minimum we need. If you were to install your package via
*pip* at this stage (i.e., ``pip install .``) it would use the specified
information from ``pyproject.toml`` for the build system, then continue to
install your package with some generic default values (or by looking for more
information in the legacy ``setup.py`` and ``setup.cfg`` files).

But there is so much more information we can provide in ``pyproject.toml``
about our package, such as any dependencies, and general metadata. If you have
built Python packages in the past you may be more familiar with putting this
kind of information in the traditional ``setup.py`` and ``setup.cfg`` files.
However now everything can go in ``pyproject.toml``, making it the only
configuration file you need (note you can still keep the traditional
``setup.*`` files for legacy purposes, and backwards compatibility).

Project metadata
^^^^^^^^^^^^^^^^

As of `PEP621 <https://peps.python.org/pep-0621/>`__ there is a standard format
for storing project metadata in ``pyproject.toml``, which
``setuptools>=61.0.0`` conforms to (see their tutorial on metadata `here
<https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html>`__).
Below is the metadata for our `demo package
<https://github.com/LSSTDESC/desc-continuous-integration>`__:

.. literalinclude:: ../../../pyproject.toml
   :language: toml
   :linenos:
   :lineno-start: 5
   :lines: 5-20

All metadata goes under the ``[project]`` section, including for example the
name of your package, the minimum required Python version, and the package
dependencies.

For our configuration, the package will be installed as ``mypackage``,
it requires Python versions ``>=3.7`` to run, and depends on the ``numpy``
package. Many of the metadata fields are optional, but it is useful to be as
thorough as possible in detailing the package, especially if you publish the
package to PyPi for example (for a list of all metadata options see `here
<https://packaging.python.org/en/latest/specifications/declaring-project-metadata/>`__). 

.. literalinclude:: ../../../pyproject.toml
   :language: toml
   :linenos:
   :lineno-start: 24
   :lines: 24-25

Because we are using the ``src/`` directory layout for our package, we need to
tell ``setuptools`` this is where our Package's source code is (the default is
``.``). Any sub-directories of ``src/`` with an ``__init__.py`` file will
automatically be discovered by ``setuptools``. 

Optional dependencies
^^^^^^^^^^^^^^^^^^^^^

The packages you list under ``[project] dependencies`` should be the minimum
required for the Python software to operate under general use. Yet optional
dependencies, for alternate use scenarios, can also be included. 

For example, in our `demo package
<https://github.com/LSSTDESC/desc-continuous-integration>`__ we need the
``pytest``, ``pytest-cov`` and ``flake8`` package's when invoking the
Continuous Integration workflows. As these package's are only needed when
performing CI, and not for the general running of the package, we include them
as optional dependencies, which can be installed alongside the main
dependencies by running ``pip install .[ci]``.  

.. literalinclude:: ../../../pyproject.toml
   :language: toml
   :linenos:
   :lineno-start: 27
   :lines: 27-28


Optional dependencies are also useful if you want to separate out serial and
parallel (i.e., MPI) implementations of your package, packages required only
during development, or installations where you wish to also compile package's
documentation, for example.

Script entrypoints
^^^^^^^^^^^^^^^^^^

Another extremely useful thing to be aware of with Python packages is script
entrypoints. Here you can declare commands to be run from the terminal which
will directly execute functions within your package. For example, in our `demo
package <https://github.com/LSSTDESC/desc-continuous-integration>`__ we have a
function that computes the numerical value of *pi*. As we keep forgetting the
value of *pi*, and need to be reminded, we register the ``display-pi`` command
to help us, which directly calls the ``mydescpackage.pi.display_pi`` function
(which prints the computed value of *pi* to the terminal).

.. literalinclude:: ../../../pyproject.toml
   :language: toml
   :linenos:
   :lineno-start: 30
   :lines: 30-31

Script entrypoints are great for creating front-ends to your package. 

.. _Automatic_versioning:

Automatic versioning
--------------------

An extremely important attribute of your Python package is its version number,
for which it is good practice to use the `Semantic Versioning
<https://semver.org/>`__ format (i.e., MAJOR.MINOR.PATCH). The pseudo-standard
for Python packages is to store the version number as a string variable called
``__version__`` in the root of the package, e.g.,
``mydescpackage.__version__``.

We are going to have to manually declare our chosen version number somewhere
within our project, however we certainly want to avoid manual declarations in
multiple places, some of which we may forget to update (e.g., between the
``pyproject.toml`` file and within the source code). There are `many
options
<https://packaging.python.org/en/latest/guides/single-sourcing-package-version/>`__
that allow you to only declare the version number once, yet there is no current
standard for which practice is best.

We would recommend declaring the package version number in a ``_version.py``
file in the package source code directory (i.e., ``src/mydescpackage/``). This
option has the advantage that ``mydescpackage.__version__`` can be called both
in the scenario where the package has been installed via `pip`, or if the
source code is being called upon manually straight from the cloned repository.  

To do this, create a file called ``_version.py`` in the ``src/mydescpackage/``
directory with the following:

.. code-block:: python

   __version__ = "1.0.0"

.. note::

   We put the ``__version__`` variable in a file called ``_version.py`` instead
   of ``version.py`` so that ``pip`` does not install ``mydescpackage.version``
   as a callable method. 

Then, include this line in the ``__init__.py`` file in the ``src/mydescpackage/``
directory:

.. code-block:: python

   from ._version import __version__

Finally, we can tell `pip` to use this as the package version number by
updating our ``pyproject.toml`` file with the following:

.. code-block:: toml

   [project]
   ...
   dynamic = ["version"]

   [tool.setuptools.dynamic]
   version = {attr = "mydescpackage._version.__version__"}

Installing your package (from source)
-------------------------------------

Finally, once the ``pyproject.toml`` file is built, we can install the package
locally from source using ``pip`` just like we have always traditionally done.
Within the project directory type:

.. code-block:: bash

   pip install -e .

Note the ``-e`` flag means an "editable install", which is extremely useful,
particularly during the development stage of your software. An editable
installation works very similarly to a regular install with ``pip install .``,
except that it only installs your package dependencies, metadata and wrappers
for console and GUI scripts, but your system will point to the code directly in
your project folder using a special link. This means that any changes in the
Python source code can immediately take place without requiring a new
installation.

As it stands, users wishing to install our package first have to clone the
*GitHub* repository and install from source as shown above (which is fine). To
make the installation slightly for users, we can place our package on a public
software repository, such a ``PyPy`` or ``Conda``, which we cover next. 
