.. DESC CI test documentation master file, created by
   sphinx-quickstart on Mon Jun 20 11:41:18 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _desc_ci_intro:

What is Continuous Integration (CI)?
====================================

    "*Continuous integration (CI) is a software practice that requires
    frequently committing code to a shared repository. Committing code more
    often detects errors sooner and reduces the amount of code a developer
    needs to debug when finding the source of an error. Frequent code updates
    also make it easier to merge changes from different members of a software
    development team. This is great for developers, who can spend more time
    writing code and less time debugging errors or resolving merge conflicts.*

    *When you commit code to your repository, you can continuously build and
    test the code to make sure that the commit doesn't introduce errors. Your
    tests can include code linters (which check style formatting), security
    checks, code coverage, functional tests, and other custom checks.*

    *Building and testing your code requires a server. You can build and test
    updates locally before pushing code to a repository, or you can use a CI
    server that checks for new code commits in a repository.*"

    -- `Taken from the GitHub website
    <https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration>`__

Essentially, CI is a philosophy to keep a repositories' code live and
up-to-date, by encouraging the developers to push their code changes as
frequently as possible, whilst ensuring the codebase remains stable and bug
free through the use of a test suite and a CI workflow. 

CI is a keenly encouraged practice when developing DESC software. Continuous
testing is a key means of maintaining software quality. Running tests regularly
can significantly reduce development time, as they can catch bugs as soon as
they are introduced. In addition, comprehensive tests allow for aggressive
refactoring, which is an important part of agile development for producing high
quality code.

Starting with a test suite
--------------------------

A good test suite is the cornerstone of a CI workflow. Testing can occur at
several levels: system testing, integration testing, and unit testing, with
unit tests being the most granular and operating at the function and class
level.

Here are some recommendations to think about when creating a test suite for
your DESC software, taken directly from the `LSST DESC Coding Guidelines
<https://lsstdesc.org/assets/pdf/docs/DESC_Coding_Guidelines_latest.pdf>`__.
It is also worth looking at the `DM team's unit test policy
<https://developer.lsst.io/coding/unit-test-policy.html>`__.

* **Unit tests** are good for testing small bits of code to check that each
  function does what it is supposed to do. Unit tests should ideally be
  comprehensive, but if not, they should at least cover the parts of the code
  where the cost of failure is highest.

* **Regression tests** may be helpful to make sure existing functionality is
  preserved in the future through possible code refactoring.

* **User interface tests** check that the code behaves sensibly if the user does
  something they shouldn’t do (e.g., gives bad inputs, forgets a parameter,
  etc).

* **Functional tests** check that the code produces correct outputs for a variety of inputs.

* If you can test some fancy, efficient algorithm against a more obviously
  correct (but slower) algorithm, that’s a great test to include.

* If there are specific special cases where the answer can be known
  analytically or via some other means, these are good functional tests as
  well.

* Think about edge cases. What might cause your code to fail? You should add
  tests that these edge cases work correctly.

* Integration tests check that your class/function/etc. works correctly with
  other parts of the overall code base.

pytest
^^^^^^

There are many fantastic Python packages that can help you build a test suite
framework for your software. One popular example is ``pytest``. 

    "*The pytest framework makes it easy to write small, readable tests, and
    can scale to support complex functional testing for applications and
    libraries.*" -- `pytest website <https://docs.pytest.org/en/7.1.x/>`__

We utilize ``pytest`` to build a simple test framework for the dummy code in
this example repository, designed to scrutinize the mathematical functions in
``./python/my_arithmetic.py``, making sure they work as expected. The unit
tests are located in the ``./python/test_*.py`` files, which can be run by
simply entering ``pytest ./python`` into the command line. For those not
familiar with ``pytest``, their `tutorial website
<https://docs.pytest.org/en/7.1.x/getting-started.html>`__ is a great place to
get started. 

The goal of CI, then, is to automate our test suite using a workflow, which we
will demonstrate using GitHub Actions.
