#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from aoalias import Aoalias


def test_resolve_dev():
    test_root = Path(__file__).with_name("root1")
    assert test_root.exists()
    ao = Aoalias(test_root)

    assert ao.resolve("d1").samefile(test_root.joinpath("d1_2023_xxx"))


def test_resolve_dev():
    test_root = Path(__file__).with_name("root2")
    assert test_root.exists()
    ao = Aoalias(test_root)

    assert ao.resolve("d1").samefile(test_root.joinpath("Dev_001_2023_xxx"))


def test_resolve_dev():
    test_root = Path(__file__).with_name("root3")
    assert test_root.exists()
    ao = Aoalias(test_root)

    assert ao.resolve("d1").samefile(test_root.joinpath("Dev/001_2023_xxx"))
