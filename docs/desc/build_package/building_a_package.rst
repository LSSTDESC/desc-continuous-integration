Developing a Python package at DESC
===================================

The *"standard"* way of building packages in Python has gone through many
changes in recent years, and if you have not been keeping track, it can be
difficult to know the best method for putting a Python package together such
that it is easy to install, easy to maintain and easy to publish. 

Here we go over the (relatively) new standard for Python packaging, the
``pyproject.toml`` file. We would recommend developers at DESC strongly
consider migrating to this new packaging standard, if you haven't already,
particularly when starting a new package from scratch. The intuitive, clean and
maintainable format of ``pyproject.toml`` packages make them both easy to work
with and publish with a minimal amount of effort. 

This guide assumes some basic knowledge of putting together a piece of Python
software, such as creating your own modules, etc. For those unfamiliar with
creating Python software, check out the `official Python guide
<https://docs.python.org/3/tutorial/modules.html#packages>`_. Also note this is
by no means an exhaustive tutorial on the subject of Python packaging. A great
additional resource for that is the `Python Packaging Guide
<https://packaging.python.org/en/latest/tutorials/packaging-projects/#>`_
itself.

Note we write this guide under the assumption that the Python package you are
creating will being hosted by the `DESC github repository
<https://github.com/lsstDESC>`_, however the majority of this guide will still
apply even if this is not the case. If you are not yet familiar with `git` or
`github`, or you need help getting setup on the `DESC github repository
<https://github.com/lsstDESC>`_, checkout `this guide
<https://confluence.slac.stanford.edu/display/LSSTDESC/Getting+Started+with+Git+and+GitHub>`_
on the DESC Confluence page, or this more general `getting started
<https://github.com/drphilmarshall/GettingStarted#top>`_ guide.  

The accompanying repository which hosts the demo package we often refer in this
guide can be found `here
<https://github.com/LSSTDESC/desc-continuous-integration>`_. The package,
``mydescpackage``, is very simple, consisting of a few callable mathematical
functions. You are welcome to download/fork it and use it as a starting
template for your project. 

.. note::

   For those wondering what a TOML file is, `TOML <https://toml.io/en/>`_ is a
   file format for configuration files, similar to YAML, it stands for "*Tom's
   Obvious Minimal Language*".

The directory structure
-----------------------

Let's get started, first we go over the directory structure of Python packages,
which should look something like this (replacing names where sensible):

::

    /path/to/my/project/
    ├── README.md           
    ├── pyproject.toml      
    ├── LICENCE
    ├── .gitignore
    ├── src/                
    │   └── mydescpackage/      
    │       ├── __init__.py
    │       ├── file1.py
    │       └── file2.py
    ├── tests/              
    │   ├── test1.py
    │   └── test2.py
    ├── .github/
    │   └── workflows/
    │       └── ci.yml
    └── docs/               


Note that not all of these files and directories are strictly required, however
as a minimum you should have the ``README.md`` and ``pyproject.toml`` files in
your base project directory and your software code should populate the
``src/mydescpackage/`` directory.

What are these files and directories...

* ``README.md``: Usually a markdown file, typically outlines the project, its
  requirements, installation instructions, authors, etc. The contents of this
  file will also be displayed on your *github* project landing page. 

* ``pyproject.toml``: Where the build information, project dependencies,
  metadata, etc, of the Python package is stored. More in the next section.

* ``LICENCE``: Contains the license of the package, outlining any restrictions
  of its use. It is good practice to use a well-known license rather than a
  self-created license, such as; `GNU
  <https://www.gnu.org/licenses/gpl-3.0.en.html>`_, `Apache licence
  <https://www.apache.org/licenses/LICENSE-2.0>`_, `MIT license
  <https://opensource.org/licenses/MIT>`_ or `creative commons license
  <https://creativecommons.org/choose/>`_.

* ``.gitignore``: This file specifies intentionally untracked files that Git
  should ignore (see `here <https://git-scm.com/docs/gitignore>`_).

* ``src/mydescpackage/``: Many people prefer placing their python packages in a
  ``src/`` folder in their project directory. This is a preference, and not a
  requirement, however it does break the habit of getting used to running the
  source code directly from the project directory, as using the ``src/``
  directory layout forces the user to install the package to run (don't worry,
  you still only have to install the package once with an editable install, see
  more about this later on).

* ``tests/``: Your tests go in here (see our guide on :ref:`Continuous
  Integration <desc_ci_intro>`).

* ``.github/workflows/``: Your *github* Actions Continuous Integration
  workflows go in here (see our guide on :ref:`Continuous Integration
  <desc_ci_intro>`).

* ``docs/``: For extensive documentation, *readthedocs* files for example.

Once the directory structure is setup, we can move onto telling ``pip`` how to
build and install our package.

The ``pyproject.toml`` file
---------------------------

The ``pyproject.toml`` configuration file was introduced in `PEP518
<https://peps.python.org/pep-0518/>`_ as a way of specifying the minimum build
system requirements for Python projects. This allows the system to know what
packages are required during the building process itself, e.g., ``setuptools``,
``wheel``, so that one does not have to pre-install any package dependencies
before hand in order to install your package. The build requirements specified
in ``pyproject.toml`` are installed in an isolated environment, used to build
the package, and later discarded, keeping your base environment clean and tidy.

The build system
^^^^^^^^^^^^^^^^

To specify which build-backend to use for installing your package, and any
requirements needed during the build process, include this at the top of your
``pyproject.toml`` file.

.. code-block:: toml

   [build-system]
   requires = ["setuptools >= 61.0"]
   build-backend = "setuptools.build_meta"

Here we are saying we require the ``setuptools`` package during the build, and
we are going to use ``setuptools`` to build the our Python package as our
``build-backend``. Other common requirements during he build process are
``wheel`` and ``cython``.

.. note:: You do not have to use ``setuptools`` as your ``build-backend``, you
   can use alternate Python package managers such as `Poetry
   <https://python-poetry.org/>`_, or `Flit
   <https://flit.pypa.io/en/stable/>`_. You even can put your own custom
   ``build-backend`` here if you have very specific requirements for building
   your package. However if you are unsure, stick with `setuptools`.

In theory this is the minimum needed, if you were to install your package via
*pip* at this stage, ``pip install .``, it would use the specified information
from ``pyproject.toml`` for the build system, and continue to install your
package with some generic default values, or by looking for more information in
the legacy ``setup.py`` and ``setup.cfg`` files.

However, we are now able to transfer the all information that has traditionally
been put in the ``setup.py`` and ``setup.cfg`` files directly into
``pyproject.toml``, making it the only configuration file you need (note you
can still keep the traditional ``setup.*`` files for legacy purposes and
backwards compatibility).

Project metadata
^^^^^^^^^^^^^^^^

As of `PEP621 <https://peps.python.org/pep-0621/>`_ there is a standard format
for storing project metadata in ``pyproject.toml``, which
``setuptools>=61.0.0`` conforms to (see their tutorial on metadata `here
<https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html>`_).
Below is the metadata for our demo package:

.. code-block:: toml

   [project]
   name = "mydescpackage"
   description = "Example DESC Python package, some simple mathmatical functions."
   license = {text = "BSD 3-Clause License"}
   classifiers = [
       "Programming Language :: Python :: 3",
   ]
   dependencies = [
       'numpy',
       'importlib-metadata;python_version<"3.8"'
   ]
   requires-python = ">=3"
   version = "0.0.1"

All metadata goes under the ``[project]`` section, including the name of your
package, the minimum required Python version, and the package dependencies.
Here we are saying our package will be installed as ``mypackage==0.0.1``, it
requires Python versions ``>=3`` to run, and depends on ``numpy``
(``importlib-metadata`` was not built-in to Python prior to ``<3.8``, so we
need to include that as a dependency in those cases). Many of the metadata
fields are optional, but it is useful to be as thorough as possible detailing
the package, especially if you publish the package to PyPi for example (for a
list of all metadata options see `here
<https://packaging.python.org/en/latest/specifications/declaring-project-metadata/>`_). 

.. code-block:: toml

   [tool.setuptools.packages.find]
   where = ["src"]

Because we are using the ``src/`` directory to host our package's code, we can
aid ``setuptools`` by pointing to this directory in its search for our
Package's source code (the default is ``.``). Any [sub/]directories of ``src/``
with an ``__init__.py`` file will automatically be discovered by
``setuptools``. 

Optional dependencies
^^^^^^^^^^^^^^^^^^^^^

The packages listed under ``[project] dependencies`` should be the minimum
required for your Python software to operate. Yet we can include optional
dependencies for alternate scenarios. 

For example, in our demo package we have a test suite which we invoke using the
``pytest`` package during the Continuous Integration process. As we only need
the ``pytest`` package during testing, we create an optional dependency list,
labelled `test`. 

.. code-block:: toml

   [project.optional-dependencies]
   test = ["pytest"]

which, when running ``pip install .[test]``, will install ``pytest`` along with
the default dependencies.

Optional dependencies are also useful if you want MPI-specific installs, or
installs to compile documentation, for example.

Package entrypoints/scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another extremely useful thing to be aware of with Python packages is script
entrypoints. Here you can declare commands to be run from the terminal which
will directly execute functions within your package. For example, in our demo
package we have a function that computes the numerical value of *pi*. As we
keep forgetting the value of *pi*, we can to register a command,
``display-pi``, to help us, which calls the ``mydescpackage.pi.display_pi``
function directly (outputting the value of *pi* to the terminal).

.. code-block:: toml

   [project.scripts]
   display-pi = "mydescpackage.pi:display_pi"

Entrypoints are great for creating front-ends to your packages. 

Automatic versioning
--------------------

An extremely important attribute of your Python package is its version, which
you should declare in the ``pyproject.toml`` metadata. It is a good practice to
use the `Semantic Versioning <https://semver.org/>`_ format for your code. 

In order to not have multiple manual declarations of the package version, both
in the ``pyproject.toml`` file and the source code, a useful trick is to use
the ``importlib.metadata`` method to access the version tag dynamically within
the code. 

To do this, go to your ``__init__.py`` file in your ``mydescpackage`` directory and insert:

.. code-block:: python

   try:
       # For Python >= 3.8
       from importlib import metadata
   except ImportError:
       # For Python < 3.8
       import importlib_metadata as metadata
   
   __version__ = metadata.version("mydescpackage")

then any calls to ``mydescpackage.__version__`` will be automatically up to
date and correct.

Installing your package (from source)
-------------------------------------

Finally, once the ``pyproject.toml`` file is built, we can install the package
using ``pip`` just like before. Within the project directory type:

.. code-block:: bash

   pip install -e .

Note the ``-e`` flag means an "editable install", which is extremely useful,
particularly when developing your packages. An editable installation works very
similarly to a regular install with ``pip install .``, except that it only
installs your package dependencies, metadata and wrappers for console and GUI
scripts, but your system will point to the code directly in your project folder
using a special link. This means that any changes in the Python source code can
immediately take place without requiring a new installation.

For this installation method, people will have to clone your *git* repository,
and install from source as shown above (which is fine). A slightly easier way
for people to install your packages is via public repositories, such a ``PyPy``
and ``Conda``, which we cover next. 
