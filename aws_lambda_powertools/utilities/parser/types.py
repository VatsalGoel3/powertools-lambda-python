"""Generics and other shared types used across parser"""

from typing import Any, Literal, TypeVar, Union

from pydantic import BaseModel, Json

Model = TypeVar("Model", bound=BaseModel)
EnvelopeModel = TypeVar("EnvelopeModel")
EventParserReturnType = TypeVar("EventParserReturnType")
AnyInheritedModel = Union[type[BaseModel], BaseModel]
RawDictOrModel = Union[dict[str, Any], AnyInheritedModel]
T = TypeVar("T")

__all__ = ["Json", "Literal"]
