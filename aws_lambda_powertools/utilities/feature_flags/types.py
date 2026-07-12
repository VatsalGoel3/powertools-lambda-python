from typing import Any, TypeVar, Union

from typing_extensions import ParamSpec

# JSON primitives only, mypy doesn't support recursive tho
JSONType = Union[str, int, float, bool, None, dict[str, Any], list[Any]]
T = TypeVar("T")
P = ParamSpec("P")
