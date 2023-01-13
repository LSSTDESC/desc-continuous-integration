Welcome to DESC's Python packaging and Continuous Integration guide!
====================================================================

This documentation is designed as a quickstart guide for writing Python
packages and deploying Continuous Integration (CI) workflows at DESC. 

The accompanying demo Python package code and example CI workflows that are
referenced in this guide can be found in the `desc-continuous-integration
<https://github.com/LSSTDESC/desc-continuous-integration>`__ repository.

Those already familiar with *GitHub Actions* and CI and want to see our
recommended strategy for CI workflows at DESC can skip to the :ref:`DESC
Checklist`.

.. toctree::
   :maxdepth: 2
   :caption: Python packaging at DESC

   ./desc/build_package/building_a_package
   ./desc/build_package/publish
   ./desc/build_package/document

.. toctree::
   :maxdepth: 2
   :caption: Continuous Integration at DESC

   ./desc/ci/what_is_ci
   ./desc/ci/github_actions
   ./desc/ci/ci_at_nersc
   ./desc/ci/desc_working_examples
   ./desc/ci/desc_working_examples_pipelines
   ./desc/ci/desc_checklist

.. toctree::
   :maxdepth: 2
   :caption: Appendix

   ./desc/ci/appendix

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
