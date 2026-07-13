#!/usr/bin/env python3

from __future__ import annotations

import os
from typing import Iterable, Mapping

ADMIN_IDS_ENV_VAR = "CAVE_BOT_ADMIN_IDS"


def parse_admin_ids(raw: str | None) -> frozenset[str]:
    """Parse a comma-separated list of GroupMe user IDs into a set of non-empty, stripped IDs."""
    if not raw:
        return frozenset()

    return frozenset(part.strip() for part in raw.split(",") if part.strip())


def get_admin_ids_from_env(env: Mapping[str, str] = os.environ) -> frozenset[str]:
    return parse_admin_ids(env.get(ADMIN_IDS_ENV_VAR))


def is_admin(sender_id: str | None, admin_ids: Iterable[str]) -> bool:
    """Return True if sender_id is a non-empty match against the admin_ids set."""
    if not sender_id:
        return False

    return sender_id in admin_ids
