from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Union

from pydantic import BaseModel

from aws_lambda_powertools.utilities.parser import parse

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext

AnyInheritedModel = Union[type[BaseModel], BaseModel]
RawDictOrModel = Union[dict[str, Any], AnyInheritedModel]


class ModelWithUnionType(BaseModel):
    name: str
    profile: RawDictOrModel


def lambda_handler(event: ModelWithUnionType, context: LambdaContext):
    event = json.dumps(event)

    event_parsed = parse(event=event, model=ModelWithUnionType)

    return {"name": event_parsed.name}
