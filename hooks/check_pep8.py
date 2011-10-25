#!/usr/bin/env python
"""
Checks code for PEP8 compliance.
"""

import os
import re

from util import get_config, run_command


class CheckPep8(object):

    def __init__(self):
        self.exclude = get_config("pep8-exclude")
        self.exclude_re = re.compile(self.exclude) if self.exclude else None
        self.pep8_ignore = get_config("pep8-ignore")

    def should_process_file(self, filename):
        if self.exclude_re:
            return not self.exclude_re.match(filename)
        return True

    def __str__(self):
        return "<CheckPep8: ignore %r, exclude %r>" % (self.pep8_ignore, self.exclude)

    def file_passes(self, temp_filename, original_filename=None):
        if original_filename is None:
            original_filename = temp_filename

        pep8_path = os.path.join(os.path.dirname(__file__), "pep8", "pep8.py")
        pep8_command = "%(pep8_path)s --ignore=%(ignore)s -r %(filename)s" % dict(pep8_path=pep8_path,
                                                                                  ignore=self.pep8_ignore,
                                                                                  filename=temp_filename)
        pep8_out, pep8_err, pep8_rc = run_command(pep8_command)
        if len(pep8_err) > 0:
            return False, "# Internal error checking pep8:\n%(pep8_err)s\n" % dict(pep8_err=pep8_err)

        if len(pep8_out) > 0:
            assert temp_filename.endswith(original_filename)
            temp_dir = temp_filename[:-len(original_filename)]
            error_message = "# pep8 problems with %(f)s:" % dict(f=original_filename)
            pep8_formatted = "\n".join(["#   " + line.replace(temp_dir, "") for line in pep8_out.splitlines()])
            return False, error_message + "\n" + pep8_formatted

        return True, None
