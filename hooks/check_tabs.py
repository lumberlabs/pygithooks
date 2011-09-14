#!/usr/bin/env python
"""
Checks code for ambiguous tabs or other basic parsing issues.
"""

try:
    import CStringIO as StringIO
except ImportError:
    import StringIO
import tabnanny
import tokenize


class CheckTabs(object):

    def should_process_file(self, filename):
        return True

    def file_passes(self, temp_filename, original_filename=None):
        if original_filename is None:
            original_filename = temp_filename

        with open(temp_filename, "r") as temp_file:
            code = temp_file.read()

        # note that this uses non-public elements from stdlib's tabnanny, because tabnanny
        # is (very frustratingly) written only to be used as a script, but using it that way
        # in this context requires writing temporarily files, running subprocesses, blah blah blah
        code_buffer = StringIO.StringIO(code)
        try:
            tabnanny.process_tokens(tokenize.generate_tokens(code_buffer.readline))
        except tokenize.TokenError as e:
            return False, "# Could not parse code in {f}: {e}".format(e=e, f=original_filename)
        except IndentationError as e:
            return False, "# Indentation error in {f}: {e}".format(e=e, f=original_filename)
        except tabnanny.NannyNag as e:
            return False, "# Ambiguous tab in {f} at line {line}; line is '{contents}'.".format(line=e.get_lineno(),
                                                                                                contents=e.get_line().rstrip(),
                                                                                                f=original_filename)
        return True, None
