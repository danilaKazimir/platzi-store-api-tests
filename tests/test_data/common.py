from typing import Literal

import pytest

type LookupField = Literal["id", "slug"]

LOOKUP_FIELD_PARAMS = (
    pytest.param("id", id="id"),
    pytest.param("slug", id="slug"),
)
