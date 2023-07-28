#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class AoaliasKey:
    id: str
    ID: str
    head: str
    init: str
    KEYS = None

    def __init__(self, id, head, init):
        self.id, self.head, self.init = id, head, init
        self.ID = self.id.capitalize()


AoaliasKey.KEYS = {
    "d": AoaliasKey("dev", "Dev_", "d"),
}
