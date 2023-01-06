Developing a Python package at DESC
===================================

The *"standard"* way of building packages in Python has gone through many
changes in recent years, and if you have not been keeping track, it can be
difficult to know the best method for putting a Python package together such
that it is easy to install, easy to maintain and easy to publish. 

Here we go over the (relatively) new standard for Python packaging, the
``pyproject.toml`` file. We would recommend developers at DESC strongly
consider migrating to this new packaging standard, particularly when starting a
new package from scratch. The intuitive, clean and maintainable format of
``pyproject.toml`` packages make them both easy to work with and publish with a
minimal amount of effort. 

This guide assumes some basic knowledge of Python and creating your own Python
modules/software. If you are unfamiliar with creating your own Python modules
have a look at `this guide
<https://docs.python.org/3/tutorial/modules.html#packages>`_. Also note this is
by no means an exhaustive tutorial on the subject of Python packaging. A great
additional resource is from the `Python Packaging Guide
<https://packaging.python.org/en/latest/tutorials/packaging-projects/#>`_
itself.

We also assume the Python package will being hosted by the `DESC github
repository <https://github.com/lsstDESC>`_, however most of the guide will also
apply if this is not the case. If you are not familiar with `github`, checkout
the DESC guide on the `Confluence page
<https://confluence.slac.stanford.edu/display/LSSTDESC/Getting+Started+with+Git+and+GitHub>`_
or this `getting started
<https://github.com/drphilmarshall/GettingStarted#top>`_ guide.  

.. note::

   `TOML <https://toml.io/en/>`_ is a file format for configuration files,
   similar to YAML.

The directory structure
-----------------------

To start, the structure of your project should look something like this:

::

    /path/to/my/project/
    ├── README.md           
    ├── pyproject.toml      
    ├── LICENCE
    ├── .gitignore
    ├── src/                
    │   └── mypackage/      
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


Not all of these files and directories are required, however as a minimum you
should have ``README.md``, ``pyproject.toml`` and ``src/mypackage/``.

* ``README.md``: Usually a markdown file, typically outlines the project, its
  requirements, installation instructions, authors, etc... 

* ``pyproject.toml``: Where the build information, project dependencies,
  metadata, etc is stored. More in the next section.

* ``LICENCE``: This file shows the license of the package, outlining any
  restrictions of its use. It is good practice to use a well-known license
  rather than a self-created license, such as; `GNU
  <https://www.gnu.org/licenses/gpl-3.0.en.html>`_, `Apache licence
  <https://www.apache.org/licenses/LICENSE-2.0>`_, `MIT license
  <https://opensource.org/licenses/MIT>`_ or `creative commons license
  <https://creativecommons.org/choose/>`_.

* ``.gitignore``: This file specifies intentionally untracked files that Git
  should ignore (see `here <https://git-scm.com/docs/gitignore>`_).

* ``src/mypackage/``: Many people prefer placing their python packages in a
  ``src/`` folder in their project directory. This is a preference, and not a
  requirement, however it does break the habit of getting used to running the
  source code directly from the project directory, as using the ``src/``
  directory layout forces the user to install the package to run (don't worry,
  you still only have to install the package once with an editable install, see
  later).

* ``tests/``: Your tests go in here, see also our guide on Continuous
  Integration.

* ``.github/workflows/``: Your ``github`` Actions workflows go in here, see
  also our guide on Continuous Integration.

* ``docs/``: For extensive documentation, readthedocs files for example.

Once the directory structure is setup, we can move onto telling ``pip`` how to
build and install our package.

The ``pyproject.toml`` file
---------------------------

The ``pyproject.toml`` configuration file was introduced in `PEP518
<https://peps.python.org/pep-0518/>`_ as a way of specifying the minimum build
system requirements for Python projects. This allows the system to know what
packages are required during the building process itself, e.g., ``setuptools``,
``wheel``, so that one does not have to pre-install any package dependencies
before hand in order to install your package. The build dependencies are built
in an isolated environment, used to build the package, and later discarded,
keeping your base environment clean and tidy.

To specify which build system to use, and any requirements needed during the
build process, include this at the top of your ``pyproject.toml`` file.

.. code-block:: toml

   [build-system]
   requires = ["setuptools"]
   build-backend = "setuptools.build_meta"

Here we are saying we require ``setuptools`` and we are using ``setuptools`` to
build the package as our ``build-backend``.

.. note:: You can put your own custom build-backend here if you have very
   specific requirements for building your package.

In theory this is the minimum needed, if you were to ``pip install`` your
package at this stage it would use the specified information from
``pyproject.toml`` for the build system, and install your package by looking
for a traditional ``setup.py`` file.

However now all the information from ``setup.py`` (and ``setup.cfg``) can be
transferred over to ``pyproject.toml``, making it the only configuration file
you need, yet you can still keep the traditional ``setup.*`` files for legacy
purposes. For this guide, we want to keep everything in ``pyproject.toml``.

``setuptools`` now conforms to the `PEP621
<https://peps.python.org/pep-0621/>`_ standard for Storing project metadata in
``pyproject.toml`` (see ``setuptools``'s own tutorial `here
<https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html>`_. For
example:

.. code-block:: toml

   [project]
   name = "mypackage"
   description = "My package description"
   readme = "README.md"
   requires-python = ">=3.8"
   keywords = ["one", "two"]
   license = {text = "BSD 3-Clause License"}
   classifiers = [
       "Programming Language :: Python :: 3",
   ]
   authors = [
   { name = "Stuart McAlpine", email = "stuart.mcalpine@fysik.su.se" }
   ]
   dependencies = [
       "numpy",
   ]

All metadata goes under the ``[project]`` section, including the name of your
package, the minimum required Python version, and the package dependencies.
Here we are saying our package will be installed as ``mypackage``, it requires
Python versions ``>=3.8`` to run, and depends on ``numpy``. A lot of the
metadata is optional, but it is useful to be as thorough as possible detailing
the package, especially if you publish the package to PyPi for example (for a
list of all metadata options see `here
<https://packaging.python.org/en/latest/specifications/declaring-project-metadata/>`_). 

Another extremely useful thing to be aware of with Python packages is script
entrypoints. Here you can declare commands to directly execute functions within
your package. For   

.. code-block:: toml

   [project.scripts]
   my-script = "my_package.module:function"

Automatic versioning
--------------------

It is very important to properly version your code, so that people are aware of
changes, and your pacakge as a dependency can be properly managed. It is a good
practice to use the `Semantic Versioning <https://semver.org/>`_ format. 

It can however be tricky to keep track of all the declarations of your package
version within the code. A useful trick is to declare the version once within
``pyproject.toml`` and use the ``importlib.metadata`` method (build in to
Python ``>3.8``) to access it. 

You can then go to your ``__init__.py`` file in your ``mypackage`` directory and insert:

.. code-block:: python

   import importlib.metadata

   __version__ = importlib.metadata.version("mypackage")

then any calls to ``mypackage.__version__`` will be up to date and correct.

Installing your package
-----------------------

Once the ``pyproject.toml`` file is built, we can install the package with
``pip`` just like before. Within the project directory type:

.. code-block:: bash

   pip install -e .

Note the ``-e`` means an editable install, which is extremely useful,
particularly when developing your packages. An “editable installation” works
very similarly to a regular install with ``pip install .``, except that it only
installs your package dependencies, metadata and wrappers for console and GUI
scripts, but it points to the code directly in your project folder using a
special link. This means that changes in the Python source code can immediately
take place without requiring a new installation.
