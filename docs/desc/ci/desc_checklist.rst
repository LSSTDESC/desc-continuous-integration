.. _DESC checklist:

The DESC CI checklist
=====================

Below is our recommended CI checklist for DESC repositories written in Python.
Note that ``ci_example_2.yml`` includes the first four points of the checklist
and ``ci_example_3.yml`` and ``ci_example_4.yml`` cover all five points.

This checklist was last updated January 2023.

1. Test your code using ``ubuntu-20.04``, ``ubuntu-22.04`` and
   ``macos-latest``.

2. Test your code using ``Python 3.8`` and above.

3. Use ``Flake8`` (or similar tool) to automatically lint and check your code
   for basic formatting errors.

.. tip:: If you are starting a codebase from scratch, try and adhere as best
   you can to the `PEP 8 <https://peps.python.org/pep-0008/>`__ coding standard
   right from the get-go to avoid any programming style clashes down the line.

4. Check the code coverage of your test suite using an automated tool like
   `pytest <https://docs.pytest.org/en/7.2.x/>`__.

.. tip:: Think about uploading your code coverage results to a site like
   codecov.io and putting a code coverage badge on your repositories front
   page. 

5. If your software package is a dependency for other DESC software, or it
   builds into a larger DESC pipeline, test your code within the
   ``desc-python`` environment docker container.

.. note:: We understand that setting up the ``desc-python`` environment can be
   considerably slower than only working with the minimum packages required to
   operate your code. If this overhead proves to costly, we recommend creating
   two workflows: (1) a regularly used workflow operating from push and pull
   requests that only meets the minimum requirements needed to run the code,
   and (2) a periodically triggered workflow, say once a week, that operates
   within the ``desc-python`` environment docker container. 
