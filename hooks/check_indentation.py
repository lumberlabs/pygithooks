#!/usr/bin/env python
"""
Checks code for PEP8 indentation compliance.

Distinct from check_pep8 because this can actually propose fixes, instead of just complaining.
"""

import difflib
import os
try:
    import CStringIO as StringIO
except ImportError:
    import StringIO
import sys
import textwrap

import reindent


def clean_diff_line_for_python_bug_2142(diff_line):
    if diff_line.endswith("\n"):
        return diff_line
    else:
        return diff_line + "\n\\ No newline at end of file\n"


def get_correct_indentation_diff(code, filename):
    """
    Generate a diff to make code correctly indented.

    Code: a string containing a file's worth of Python code
    Filename: a filename for the code (used in diff generation)

    Returns a unified diff to make code correctly indented or None if code is already correctedly indented.
    """
    code_buffer = StringIO.StringIO(code)
    output_buffer = StringIO.StringIO()
    reindenter = reindent.Reindenter(code_buffer)
    reindenter.run()
    reindenter.write(output_buffer)
    reindent_output = output_buffer.getvalue()
    output_buffer.close()
    if code != reindent_output:
        diff_generator = difflib.unified_diff(code.splitlines(True),
                                              reindent_output.splitlines(True),
                                              fromfile=filename,
                                              tofile=filename + " (reindented)")
        # work around http://bugs.python.org/issue2142
        diff = "".join(clean_diff_line_for_python_bug_2142(diff_line) for diff_line in diff_generator)
        return diff
    else:
        return None


class CheckIndentation(object):

    def should_process_file(self, filename):
        return True

    def file_passes(self, temp_filename, original_filename=None):
        if original_filename is None:
            original_filename = temp_filename

        code = open(temp_filename, "r").read()

        diff = get_correct_indentation_diff(code, original_filename)
        if diff:
            error_message = textwrap.dedent("""
                                            # %(f)s has indentation problems. To fix them automatically,
                                            # pipe your `git commit` command's stderr through `patch -p0`, e.g.:
                                            # git commit 2>&1 | patch -p0
                                            # Don't forget to `git add` your changes after patching!
                                            #
                                            """ % dict(f=original_filename))
            return False, error_message + diff
        else:
            return True, None
