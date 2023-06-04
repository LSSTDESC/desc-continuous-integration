Publishing a Python package
===========================

Publishing your package to a public repository makes the installation process
for the end user even simpler, and increases the visibility of your work.

Publishing to PyPi
------------------

The Python Package Index (PyPI) is a repository of software for the Python
programming language. It helps you find software developed and shared by the
Python community.

First, you will need to `register a PyPi account
<https://pypi.org/account/register/>`__. Whilst you’re at it, you should also
register an account on `TestPyPI <https://test.pypi.org/manage/projects/>`__.
TestPyPI is very useful. It allows you to try out all the steps of publishing a
package to PyPi without any consequences, which is particularly useful during
development, or if you have no previous experience.

Build your package
^^^^^^^^^^^^^^^^^^

Before uploading your package to PyPi, first you have to build it. You'll do
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
These are the files you'll upload to PyPi.

As a quick check, run

.. code-block:: bash

   twine check dist/*

to make sure there were no problems during the build.

Uploading your package
^^^^^^^^^^^^^^^^^^^^^^

Initially, we want to upload our package to TestPyPi to make sure everything
looks as it should.

To do this, run:

.. code-block:: bash

   twine upload -r testpypi dist/*

Twine will ask you for your username and password.

Head over to your TestPyPi page and make sure all the information looks
correct. Then, try installing your package from TestPyPi, e.g.,

.. code-block:: bash

   pip install -i https://test.pypi.org/simple/ mydescpackage


If everything works, then you can go ahead and upload your package to PyPi using:

.. code-block:: bash

   twine upload dist/*

Then users can install your package through ``pip``, e.g.,

.. code-block:: bash

   pip install mydescpackage

.. note:: All of the information PyPi receives about your package comes from the
   ``pyproject.toml`` file. At a minimum, you will need ``name`` and
   ``version`` included under the project metadata.

.. note:: The ``name`` value in the ``pyproject.toml`` file will be the
   distributed name on PyPi, and has to be unique. Ideally, the installed
   package name (i.e., the name of the folder in ``./src/``) should be the same
   as the PyPi distribution name, however they can be different if the package
   name has already been taken on PyPi.

   If you are installing your pacakge under a different name as the PyPi
   distributed name, be careful not to name your package with too generic a
   name.

Publishing to Conda
-------------------

Coming soon...

