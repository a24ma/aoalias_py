#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from pathlib import Path
import re
from aoalias.keys import AoaliasKey

log = logging.getLogger(f"{__name__}")


class Aoalias:
    root: Path

    def __init__(self, root: Path = None):
        if root is not None:
            self.root = root
        else:
            self.root = Path.home().joinpath("Share")
        if not self.root.exists():
            raise FileNotFoundError(f"not found {self.root}")

    def resolve(self, addr) -> Path:
        res = self._resolve_r(addr, self.root)
        if res is None:
            raise FileNotFoundError(f"not found 'aol://{addr}'")
        return res

    def _resolve_r(self, addr, parent):
        key, seq_num, is_leaf = self._get_next_key_and_seq(addr)
        base_dir, pattern = self._get_base_and_pattern(key, seq_num, parent)
        paths = [p for p in base_dir.glob("*") if re.match(pattern, p.name)]
        n = len(paths)
        if n == 0:
            return None  # not found
        if n > 1:
            raise FileExistsError(
                f"address '{addr}' in '{parent}' is not unique: {paths}"
            )
        next_dir = paths[0]
        if is_leaf:
            return next_dir
        else:
            res = re.split("\d+", addr, maxsplit=1)
            if len(res) == 0:
                raise ValueError(f"invalid address: aol://{addr}")
            child = self._resolve_r(res[1], next_dir)
            if child is None:
                return None  # not found child
            return next_dir + child

    def _get_next_key_and_seq(self, addr):
        _res = re.split("[a-zA-z~]+", addr, maxsplit=2)
        _n = len(_res)
        if _n < 2:
            raise ValueError(f"invalid address: {addr}")
        key = AoaliasKey.KEYS[addr[0]]
        seq_num = int(_res[1])
        is_leaf = _n == 2
        return key, seq_num, is_leaf

    def _get_base_and_pattern(self, key, seq_num, parent):
        seq_ptn = f"{seq_num:03d}".replace("0", r"\d?")
        parent_sub = parent.joinpath(key.ID)
        if parent_sub.is_dir():
            base_dir = parent_sub
            head_ptn = r""
        else:
            base_dir = parent
            head_ptn = rf"({key.head}|{key.init})"
        pattern = rf"{head_ptn}{seq_ptn}_[ivxc\d-]+_"
        return base_dir, pattern
