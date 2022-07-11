.. DESC CI test documentation master file, created by
   sphinx-quickstart on Mon Jun 20 11:41:18 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DESC CI test's documentation!
========================================

This repository contains a set of Continuous Integration (CI) example
workflows, designed to get you started with CI for your DESC software.  

The repository contains some dummy code to go with the CI examples, written in
Python, yet the CI principles described in the documentation remain the same
regardless of the coding language adopted. Because we are demonstrating CI with
Python, we use ``pytest`` to build our test framework, however again this is up
to you, and what works best for your software. 

This documentation briefly introduces CI as a concept, how we can use GitHub
Actions to manage our CI workflows, and some working example CI workflows, yet
note it is not designed as an exhaustive tutorial for each.

Those already familiar with GitHub Actions and CI can skip to the *DESC CI
Checklist* to see our recommended strategy for CI workflows at DESC.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ./desc/what_is_ci
   ./desc/github_actions
   ./desc/desc_working_examples
   ./desc/desc_checklist
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
