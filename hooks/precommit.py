#!/usr/bin/env python
"""
precommit.py

Runner of python-based precommit hooks.
"""

import os
import shutil
import sys
import tempfile

from check_pep8 import CheckPep8
from check_indentation import CheckIndentation
from check_tabs import CheckTabs
from util import get_config, run_command


def is_python_file(filename):
    """
    Returns True iff the file contains python code.

    For now, just use the file extension. Could peek inside the file as well, but that's slower, and it's not
    obvious what we should look for.
    """
    return os.path.splitext(filename)[1] == ".py"


def changed_files():
    """
    Return a generator of filenames changed in this commit. Excluded files that were just deleted.
    """
    git_diff_command = "git diff-index --cached --name-only --diff-filter=ACMRTUXB HEAD"
    git_out, git_err, git_rc = run_command(git_diff_command)

    if git_err or git_rc:
        print "# Internal hook error:\n%s\n%s\n" % (git_out, git_err)
        sys.exit(1)

    cleaned_filenames = [filename.strip() for filename in git_out.splitlines()]
    for filename in cleaned_filenames:
        if len(filename) > 0:
            yield filename


def make_temp_copy(temp_dir_with_slash, filename):
    # TODO: Once all the hooks can take straight text rather than files, use git show instead:
    # git_cat_command = "git show :{f}".format(f=filename)
    # git_out, git_err, git_rc = run_command(git_cat_command)
    # if git_err or git_rc:
    #     return None
    # return git_out # contents of <filename> in the index

    git_checkout_command = "git checkout-index --prefix=%s -- %s" % (temp_dir_with_slash, filename)
    git_out, git_err, git_rc = run_command(git_checkout_command)

    if git_out or git_err or git_rc:
        print("# Internal hook error:\n{out}\n{err}\n".format(out=git_out, err=git_err))
        sys.exit(1)

    temp_filename = os.path.join(temp_dir_with_slash, filename)
    return temp_filename


def main():
    hooks = [CheckTabs(), CheckIndentation()]

    should_check_pep8 = get_config("check-pep8", as_bool=True, default=True)
    if should_check_pep8:
        hooks += [CheckPep8()]

    # create temp directory for getting copies of files from staging.
    # TODO: Make all the hooks operate on strings instead of files, and get rid of this.
    temp_dir = tempfile.mkdtemp()
    temp_dir_with_slash = temp_dir + os.sep

    failure_encountered = False

    try:
        for filename in changed_files():
            if not is_python_file(filename):
                continue

            relevant_hooks = [hook for hook in hooks if hook.should_process_file(filename)]

            if relevant_hooks:
                temp_filename = make_temp_copy(temp_dir_with_slash, filename)
                for relevant_hook in relevant_hooks:
                    passes, error_message = relevant_hook.file_passes(temp_filename, original_filename=filename)
                    if not passes:
                        failure_encountered = True
                        print(error_message)
                        break
    finally:
        shutil.rmtree(temp_dir, True)

    return int(failure_encountered)

if __name__ == '__main__':
    sys.exit(main())
