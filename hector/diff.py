"""
For generating diff coverage reports from coverage reports
Delegates this tasks largely to `diff-cover` with some convenient defaults.

"""
import os
import subprocess

from typing import Optional, Union


def generate_report(fail_under: Optional[Union[int, str]] = None):

    cmd = [
                "diff-cover",
                "coverage.xml",
                "--compare-branch",
                "master",
                "--json-report",
                "diff-coverage.json"
            ]

    if fail_under:
        if isinstance(fail_under, str):
            fail_under = int(fail_under)

        if not isinstance(fail_under, int):
            raise Exception("Invalid value for Fail under!")

        if not (0 <= fail_under <= 100):
            raise Exception("Invalid value for Fail under! Out of Range!!")

        cmd.extend(["--fail-under", str(fail_under)])


    if not os.path.isfile("coverage.xml"):
        raise Exception("Please provide coverage.xml")

    try:
        p = subprocess.Popen(
            cmd,
            stdout = subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stout, stderr = p.communicate()

        return p.returncode, stout, stderr
    except subprocess.CalledProcessError as err:
        raise err # TODO: handle this gracefully
