Documenting a Python package
============================

    "*Software documentation is a part of any software. Good documentation
    practices are important for the success of the software. Documentation must
    comprise an interactive User Experience, Information Architecture, and good
    understanding of your audience.*

    *It needs to serve the purpose of resolving the issues, when encountered by
    the developer, and the end user.*"

    -- `Taken from Document360.com
    <https://document360.com/blog/software-documentation/>`__

Documenting software is a crucial, but all too often overlooked, practice.  At
DESC, we strongly recommend a rigorous ritual of continually writing your
documentation **alongside** the development of your packages, and not, which is
often the case, left as an afterthought to the last minute. Software with a
good documentation greatly increases usability, readability and maintainability
of our software, and drastically reduces the need for continued support from
the developers post release.

Types of documentation come in many forms, some of the most common are:

* **README**: Usually a simple markdown file, called ``README.md``, placed in
  the root directory of the Python package. It should contain a high-level
  overview of the software, and often also includes dependency requirements,
  and installation instructions.

* **How-to guides / tutorials**: These guide the user to complete a task or a
  predetermined goal, demonstrating how one would use the software in typical
  scenarios. `Jupyter Notebooks <https://jupyter.org/>`__ are a great
  interactive solution for this type of documentation.

* **Reference docs**: Describes the technical detail of the software. For
  example, describing the inner workings of particular functions, physical or
  mathematical derivations used within the code, etc. This kind of
  documentation should be more extensive, and housed in the ``docs/``
  directory.

* **Release notes**: Describes the latest version of the software, feature
  releases, and what bugs have been fixed from previous versions.

As for the implementation, there are many documentation language formats and
helper tools to choose from.

Writing documentation
---------------------

The simplest approach is to put all the documentation in the ``README.md`` file
in the package's root directory, which is written in the markdown language
(here's a `getting started <https://www.markdownguide.org/getting-started/>`__
guide for the markdown syntax).

For smaller packages this approach is a fine one, however for larger packages
we recommend reserving the content of ``README.md`` for a high-level overview
of the software and author contact information (and potentially dependency
requirements and installation instructions), and that you create a dedicated,
more extensive, standalone documentation for the package to be housed in the
``docs/`` directory. 

This extensive documentation can again be in simple markdown, over one or many
files. However there are many more powerful options, such as the `Sphinx
<https://www.sphinx-doc.org/en/master/>`__ Python documentation generator,
which uses the `reStructuredText <https://docutils.sourceforge.io/rst.html>`__
markup language, and has access to the popular `Read the Docs theme
<https://sphinx-rtd-theme.readthedocs.io/en/stable/>`__ (Sphinx is also what
this guide is written in, see the Sphinx quickstart guide `here
<https://www.sphinx-doc.org/en/master/usage/quickstart.html>`__).

If you also want to use Sphinx to document your software, feel free to use this
guide's code as a template, the `.rst` files are located under ``docs/desc/``
in the `demo repository
<https://github.com/LSSTDESC/desc-continuous-integration>`__. For a full guide
on writing documentation check out this beginners guide at `writethedocs.org
<https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/>`__.

Badges in ``README.md``
^^^^^^^^^^^^^^^^^^^^^^^

As a quick aside, you may have noticed visual badges located at the top of some
*GitHub* repositories ``README.md`` files.

These can visually be quite useful, as they can immediately inform the reader
about compatibility, what software the code was written in, if it has passed
its latest Continuous Integration build, code coverage statistics, keywords,
versions, etc. They can also be dynamically linked to information about your
package (such as the supported Python versions, release number, etc), if it is
published on a site like `PyPi <https://pypi.org/>`__. 

For example, as our Package is in Python, we could include a Python badge:

|made-with-python|

.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/

or display our LICENCE type

|GitHub license|

.. |GitHub license| image:: https://img.shields.io/github/license/Naereen/StrapDown.js.svg
   :target: https://github.com/LSSTDESC/desc-continuous-integration/main/LICENSE

Here are some sites that have a list of popular badges:

* https://github.com/Naereen/badges

* https://shields.io/

* https://github.com/alexandresanlim/Badges4-README.md-Profile

Publishing documentation
------------------------

Once we have written our documentation, where do we put it?  

If everything is in ``README.md``, then we don't have to worry, it will be
displayed automatically on the *GitHub* repositories' landing page. If you have
more extensive documentation, in ``docs/``, you'll need to chose where and how
this documentation will get displayed. One popular option is `Read the Docs
<https://readthedocs.org/>`__, a vast repository for technical documentation.
Read the Docs is free, it automatically builds your documentation, and
automatically versions your documentation. It is also compatible with the
Sphinx documentation format. Once your link *Read the Docs* to your repository,
you can place the link to the extensive documentation in ``README.md`` so users
know its location. 

*GitHub* pages
^^^^^^^^^^^^^^

Another option, similar to *Read the Docs*, and one we would recommend, is
`GitHub Pages <https://pages.github.com/>`__. 

How to set up *GitHub Pages* depends on the format of your documentation. If
your documentation is written in simple markdown, make sure your ``index.md``
file is in the base ``docs/`` directory and follow these steps:

1. Navigate to the settings page for your repository on *GitHub*.

2. Select `Pages` from the left sidebar.

3. Select `Source` to be "Deploy from a branch".

4. Under branch, switch the selection from `None` to “main”, make sure to
   select the `/docs` folder, then press `Save`.

This will then provide you with a link to your documentation (in the format
`http://lsstdesc.org/desc-continuous-integration/
<http://lsstdesc.org/desc-continuous-integration/>`__). Now you can reference
this link in your ``README.md`` file and your documentation is online and
available for everyone to see.

.. note:: You may notice an additional workflow in your *GitHub Actions* tab
   after this step. This is an automatically generated workflow to build and
   publish your documentation. It will automatically get called whenever there
   is a change to your ``main`` branch (or whatever branch you selected in the
   *GitHub Pages* settings).

*GitHub* pages with Sphinx
^^^^^^^^^^^^^^^^^^^^^^^^^^

If, like this guide, you are using Sphinx for your documentation, there are a
few extra steps to get published on *GitHub Pages*. This is because
reStructuredText languages must be compiled in order to produce the `html`
output. One option would be to build the documentation ourselves locally, place
the output in the ``docs/`` folder, and upload these into our repository. As long
as there is an ``index.html`` in the ``docs/`` folder of the repository,
*GitHub Pages* will find it and display the documentation (make sure to have
*GitHub Pages* setup like we have shown in the previous section). 

However it is not very clean to store built files directly within our
repository. It would be much better if our repository hosted the raw
documentation, in the form of the `.rst` files, and automatically built the
documentation for us.

Luckily, we can do this with a Continuous Integration workflow (we have a whole
section on CI later in this guide, :ref:`desc_ci_intro`).

Here is the CI workflow that you need to put in your ``.github/workflows/``
directory.

.. literalinclude:: ../../../.github/workflows/documentation.yml
   :language: yaml
   :linenos:

The steps of the workflow is as follows:

#. Checkout the repository.

#. Install the `Sphinx` package and the *Read the Docs* theme.

#. Use `Sphinx` to build our documentation.

#. Push the contents of the ``_build`` folder to a new branch called ``gh-pages``.

Now, instead of pointing *GitHub Pages* to your ``main`` branch as we showed
previously, point it to the ``gh-pages`` branch and the ``/root`` directory

This workflow will automatically build your documentation whenever there is a
push or pull request to the repositories main branch, or it can be triggered
manually.  See our :ref:`desc_ci_intro` guide for more information about the
structure of CI workflows. 
