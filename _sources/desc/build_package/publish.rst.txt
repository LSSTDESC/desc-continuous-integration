Publishing a Python package
===========================

Publishing your package to a public repository makes the installation process
for the end user even simpler, and increases the visibility of your work.

Where to publish your package, as always, depends on your needs. Two popular
choices are the *Python Package Index* (PyPI) and Anaconda. Here's a brief
overview of each platform and when you might choose one over the other:

**Python Package Index**

- If your package is a general-purpose Python library or application, and you
  want it to be easily installable using pip.
- PyPI is the default package repository for Python, and most Python developers
  are familiar with using pip to install packages from PyPI.
- Many Python tools and frameworks rely on PyPI for package distribution. By
  publishing on PyPI, your package becomes part of this ecosystem.
- PyPI provides a straightforward versioning system, allowing users to easily
  manage package versions.

**Anaconda**

- If your package is specifically designed for data science, scientific
  computing, or machine learning, Anaconda might be best.
- Anaconda is popular in the data science community, and many data scientists
  prefer using conda for package management due to its ability to manage
  complex environments and handle non-Python dependencies.
- If your package has complex dependencies, or requires specific versions of
  libraries or Python.
- Anaconda allows the distribution of pre-compiled binary packages, making it
  easier for users to install packages without dealing with compilation issues.

Nothing stops you from publishing to both platforms of course. However this
approach requires some care and consideration of versioning and potential
differences in dependency handling between the two platforms.

Publishing to PyPI
------------------

The Python Package Index (PyPI) is a repository of software for the Python
programming language. It helps you find software developed and shared by the
Python community.

First, you will need to `register a PyPI account
<https://pypi.org/account/register/>`__. Whilst you’re at it, you should also
register an account on `TestPyPI <https://test.pypi.org/manage/projects/>`__.
TestPyPI is very useful. It allows you to try out all the steps of publishing a
package to PyPI without any consequences, which is particularly useful during
development, or if you have no previous experience.

Build your package
^^^^^^^^^^^^^^^^^^

Before uploading your package to PyPI, first you have to build it. You'll do
this using two tools, ``build`` and ``twine``, which you can install via pip in
the usual way.

.. code-block:: bash

   pip install build twine


We need to build our package because the software on PyPI isn’t distributed as
plain source code. Instead, they’re wrapped into distribution packages,
commonly as source archives and Python wheels. These are essentially compressed
archives of your source code. Wheels are usually faster and more convenient for
your end users, while source archives provide a flexible backup alternative.
You should provide both.

To create a source archive and a wheel for your package, you use ``build`` in
your the root of your Python package directory:

.. code-block:: bash

   python3 -m build

which will create a source archive and a wheel in the ``./dist/`` directory.
These are the files you'll upload to PyPI.

As a quick check, run

.. code-block:: bash

   twine check dist/*

to make sure there were no problems during the build.

Uploading your package
^^^^^^^^^^^^^^^^^^^^^^

Initially, we want to upload our package to TestPyPI to make sure everything
looks as it should.

To do this, run:

.. code-block:: bash

   twine upload -r testpypi dist/*

Twine will ask you for your username and password.

Head over to your TestPyPI page and make sure all the information looks
correct. Then, try installing your package from TestPyPI, e.g.,

.. code-block:: bash

   pip install -i https://test.pypi.org/simple/ mydescpackage


If everything works, then you can go ahead and upload your package to PyPI using:

.. code-block:: bash

   twine upload dist/*

Then users can install your package through ``pip``, e.g.,

.. code-block:: bash

   pip install mydescpackage

.. note:: All of the information PyPI receives about your package comes from the
   ``pyproject.toml`` file. At a minimum, you will need ``name`` and
   ``version`` included under the project metadata.

.. note:: The ``name`` value in the ``pyproject.toml`` file will be the
   distributed name on PyPI, and has to be unique. Ideally, the installed
   package name (i.e., the name of the folder in ``./src/``) should be the same
   as the PyPI distribution name, however they can be different if the package
   name has already been taken on PyPI.

   If you are installing your pacakge under a different name as the PyPI
   distributed name, be careful not to name your package with too generic a
   name.

Publishing to Anaconda
----------------------

The primary difference for getting your package ready to distribute to PyPI
versus Anaconda is the need for a "recipe". A Conda recipe consists of a base
YAML file listing a set of instructions, along with optional supplementary
configuration files and build scripts, that define how the package will be
built.

For completeness, here we outline the key components of a Conda recipe.
However if we are working with a simple pure Python package, such as
``mydescpackage`` from this tutorial, we do not have to worry about creating
almost any of these components ourselves.

- **meta.yaml (required)** : The central component of a Conda recipe is the
  ``meta.yaml`` file. This YAML file contains metadata about the package,
  including its name, version, description, and dependencies. It also specifies
  the source code location, build script, and other information necessary for
  building the package.

- **External build script (optional)** : The build section in the ``meta.yaml``
  file includes the commands that defines how the package should be built. If
  this is an involved procedure, it can be included as a standalone script,
  containing the commands to compile the source code, install dependencies,
  and create the final package.

- **External test script (optional)** : The test section in the ``meta.yaml``
  file specifies how the package should be tested after it is built. This helps
  ensure that the package functions correctly. Again if this procedure is more
  involved, it can be included as additional standalone scripts.

- **Other Files (optional)** : A Conda recipe may include other files, such as
  ``bld.bat`` for Windows build instructions or ``build.sh`` for Unix-like
  systems. These files can contain platform-specific build instructions.

As stated above, constructing the ``meta.yaml`` file and build scripts manually
is only necessary in the case of complex dependencies or platform-specific
build instructions. For simple pure Python packages, we can automate the recipe
using a package called `grayskull <https://pypi.org/project/grayskull/>`__.

**Steps for publishing to Anaconda**

Here are the steps to publish a simple Python package hosted by GitHub to
Anaconda:

1. Create a release on the GitHub repository
2. Generate the Anaconda recipe automatically using ``grayskull``
3. Build the package using ``conda build``
4. Upload the package to Anaconda

which we will go through one by one below (see also a similar tutorial `here
<https://conda.org/blog/2023-05-18-how-to-use-conda-build/>`__).

Create a GitHub release
^^^^^^^^^^^^^^^^^^^^^^^

In the context of GitHub, a release is a distribution of a software project at
a specific point in time. It's a snapshot of a project's source code, along
with additional assets such as binary executables, documentation, and other
resources that users might need. GitHub provides a specific feature called
"releases" to facilitate the organization and distribution of these snapshots.

It is a release of our code the we are going to publish to Anaconda, so we have
to start by making one.

To create a release on GitHub, go to the "Releases" tab of your repository and
click on the "Draft a new release" button. Give your release a semantic version
tag, e.g., "v0.0.1", a title, and a description. Then, click "Publish release".

.. note:: You can also create the Conda recipe direcly from PyPi if you have a
   release of your package published there.

Create the Anaconda recipe
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. epigraph::

   *Grayskull is an automatic conda recipe generator.  The main goal of this
   project is to generate concise recipes for conda-forge. The Grayskull
   project was created with the intention to eventually replace conda
   skeleton.*

   *Presently Grayskull can generate recipes for Python
   packages available on PyPI and also those not published on PyPI but
   available as GitHub repositories. Grayskull can also generate recipes for R
   packages published on CRAN. Future versions of Grayskull will support recipe
   generation for packages of other repositories such as Conan and CPAN etc..*

   -- Grayskull documentation

We are going to automatically generate an Anaconda recipe for our Python
package using ``grayskull``, which we will do from within a Conda environment
(we are assuming you have Conda installed at this point).

If you want to work within a fresh environment with `grayskull` and
`conda-build` installed, create one via

.. code-block:: bash

   conda create -n packaging -y -c conda-forge grayskull conda-build
   conda activate packaging

The advantage of ``grayskull`` is that it can generate our Conda recipe
automatically using the information from our GitHub release (through the
``pyproject.toml`` and similar files). 

Make a fresh folder (not inside your base repository folder of your package)

.. code-block:: bash

   mkdir grayskull
   cd grayskull

Then run ``grayskull``

.. code-block:: bash

   grayskull pypi https://github.com/<your-gh-username>/<your-repo>

or, if you are generating a recipe from a package already published on PyPi

.. code-block:: bash

   grayskull pypi <pypi-package-name>

When its completed, you should see a ``meta.yml`` file in a folder named
``<your-repo>``.

Check the recipe
~~~~~~~~~~~~~~~~

The recipe created will be a good template, but it may not be perfect. For
example, here is what is generated for `mydescpackage`: 

.. literalinclude:: ../../../examples/grayskull/meta.yaml
   :language: yaml
   :linenos:

Here we see the name of the package will be installed as has defaulted to the
repository name, so we want to change ``{% set name =
"desc-continuous-integration" %}`` to ``{% set name = "mydescpackage" %}``. The
licence file hasn't automatically been picked up, so we have to insert that. It
has set up a test for our ``display-pi`` command, however we can remove the
``--help`` as that is not implemented for our entry point. We could also add
our ``pytest`` tests to the test section to make sure all our unit tests pass
at build time.

Build your package
^^^^^^^^^^^^^^^^^^

Now that we have the recipe, we need to build our package in preparation for
publication to Anaconda.

We do this using ``conda-build`` (which we installed above). Run it from the same
folder you ran ``grayskull`` in

.. code-block:: bash

   conda build <your-repo>

If all goes well, an archive of your package should be created in
``$CONDA_PREFIX/conda-bld/noarch/<your-repo>.tar.bz2``. 

.. note:: You can see where the package will be installed by running ``conda
   build <your-repo> --output``. Or, if you want to install your packages to a
   custom location, set the ``CONDA_BLD_PATH`` environment variable to your
   desired location.

.. note:: You can specify what Python versions your package will be pre-built
   for (check the docs `here
   <https://docs.conda.io/projects/conda-build/en/stable/resources/variants.html>`__).
   Also be aware of what architecture you are building your package on. It's a
   good idea to make a ``conda_build_config.yaml`` with the multiple Python
   versions your package supports, so there is a prebuilt binary for each
   Python version.

.. tip :: You can check everything has worked by installing the package from
   your local builds folder, i.e., ``conda install -c local
   <your-package-name>``

Upload your package
^^^^^^^^^^^^^^^^^^^

Now, final step, uploading your package to Anaconda, either to your private
channel, or a community channel you have access to.

1. Make an account on `anaconda.org <www.anaconda.org>`__.
2. Install the Anaconda client if you haven't already. You can do this via
   ``conda install anaconda-client``.
3. Use the ``anaconda login`` command to log in to your Anaconda Cloud account.
4. Upload your package using ``anaconda upload <path_to_your_package>``,
   Replace ``<path_to_your_package>`` with the path to your built package file
   (``.tar.bz2`` or ``.tar.gz`` file).
