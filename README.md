Git pre-commit hooks for Python code formatting
===============================================

Installation
------------

* Requires Python 2.5+. Not tested with Py3k.
* Clone this repo:
  + `git clone git://github.com/lumberlabs/pygithooks.git`
* Install submodules:
  + `cd pygithooks`
  + `git submodule update --init`
* Configure as desired (see below).
* If this is the only git hook you are using:
  + `cd <your_repo>`
  + `cd .git`
  + `mv hooks hooks.pygithooks.bak`
  + `ln -s /path/to/pygithooks/hooks hooks`
* If you want to use these hooks along with other hooks, just add `/path/to/pygithooks/hooks/pre-commit.py || exit 1` to your existing `pre-commit`.

Configuration
-------------

Configuration works through [`git config`](http://www.kernel.org/pub/software/scm/git/docs/git-config.html), in the section `pygithooks`.

Sample configuration command:

    git config --global pygithooks.pep8-ignore E501,E261,E302

Supported keys:

* **check-pep8**
  + whether to run pep8.py at all; if set to false, only checks tabs and indentation.
  + sample value: `false`
  + default value: `true`
* **pep8-ignore**
  + pep8 checks to skip, passed directly to pep8's --ignore
  + sample value: `E501,E261,E302`
  + default value: none
* **pep8-exclude**
  + regular expression for filenames to exclude from pep8 checks
  + sample value: `.*/migrations/.*`
  + default value: none

Contributing
------------
* Yes, please. Fork and send a pull request!
* Code formatting note: We ignore E501 (line too long).

License
-------

* `pygithooks` is released under the BSD license.
* `reindent.py` is bundled for ease of installation; it is in the public domain. See the top of `hooks/reindent.py` for details.
* `pep8.py` is included as a submodule. It is under the expat license. See the top of `hooks/pep8/pep8.py` for details.
