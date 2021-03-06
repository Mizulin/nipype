#!/usr/bin/env python
from __future__ import print_function, division, unicode_literals, absolute_import

from future import standard_library
standard_library.install_aliases()

import pytest
import sys
from contextlib import contextmanager

from io import StringIO
from ...utils import nipype_cmd

PY2 = sys.version_info[0] < 3

@contextmanager
def capture_sys_output():
    caputure_out, capture_err = StringIO(), StringIO()
    current_out, current_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = caputure_out, capture_err
        yield caputure_out, capture_err
    finally:
        sys.stdout, sys.stderr = current_out, current_err


class TestNipypeCMD():
    maxDiff = None

    def test_main_returns_2_on_empty(self):
        with pytest.raises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                nipype_cmd.main(['nipype_cmd'])

        exit_exception = cm.value
        assert exit_exception.code == 2

        msg = """usage: nipype_cmd [-h] module interface
nipype_cmd: error: the following arguments are required: module, interface
"""

        if PY2:
            msg = """usage: nipype_cmd [-h] module interface
nipype_cmd: error: too few arguments
"""
        assert stderr.getvalue() == msg
        assert stdout.getvalue() == ''

    def test_main_returns_0_on_help(self):
        with pytest.raises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                nipype_cmd.main(['nipype_cmd', '-h'])

        exit_exception = cm.value
        assert exit_exception.code == 0

        assert stderr.getvalue() == ''
        assert stdout.getvalue() == \
            """usage: nipype_cmd [-h] module interface

Nipype interface runner

positional arguments:
  module      Module name
  interface   Interface name

optional arguments:
  -h, --help  show this help message and exit
"""


    def test_list_nipy_interfacesp(self):
        with pytest.raises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                nipype_cmd.main(['nipype_cmd', 'nipype.interfaces.nipy'])

        # repeat twice in case nipy raises warnings
        with pytest.raises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                nipype_cmd.main(['nipype_cmd', 'nipype.interfaces.nipy'])
        exit_exception = cm.value
        assert exit_exception.code == 0

        assert stderr.getvalue() == ''
        assert stdout.getvalue() == \
            """Available Interfaces:
	ComputeMask
	EstimateContrast
	FitGLM
	FmriRealign4d
	Similarity
	SpaceTimeRealigner
"""

    def test_run_4d_realign_without_arguments(self):
        with pytest.raises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                nipype_cmd.main(['nipype_cmd', 'nipype.interfaces.nipy', 'FmriRealign4d'])

        exit_exception = cm.value
        assert exit_exception.code == 2

        error_message = """usage: nipype_cmd nipype.interfaces.nipy FmriRealign4d [-h]
                                                       [--between_loops [BETWEEN_LOOPS [BETWEEN_LOOPS ...]]]
                                                       [--ignore_exception]
                                                       [--loops [LOOPS [LOOPS ...]]]
                                                       [--slice_order SLICE_ORDER]
                                                       [--speedup [SPEEDUP [SPEEDUP ...]]]
                                                       [--start START]
                                                       [--time_interp TIME_INTERP]
                                                       [--tr_slices TR_SLICES]
                                                       in_file [in_file ...]
                                                       tr"""

        if not PY2:
            error_message += """
nipype_cmd nipype.interfaces.nipy FmriRealign4d: error: the following arguments are required: in_file, tr
"""
        else:
            error_message += """
nipype_cmd nipype.interfaces.nipy FmriRealign4d: error: too few arguments
"""

        assert stderr.getvalue() == error_message
        assert stdout.getvalue() == ''

    def test_run_4d_realign_help(self):
        with pytest.raises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                nipype_cmd.main(['nipype_cmd', 'nipype.interfaces.nipy', 'FmriRealign4d', '-h'])

        exit_exception = cm.value
        assert exit_exception.code == 0

        assert stderr.getvalue() == ''
        assert "Run FmriRealign4d" in stdout.getvalue()

