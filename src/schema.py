from typing import Optional,List

from langchain_core.pydantic_v1 import BaseModel, Field


class Person(BaseModel):
    """Information about a person."""

    # ^ Doc-string for the entity Person.
    # This doc-string is sent to the LLM as the description of the schema Person,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    Name: Optional[str] = Field(default=None, description="The name of the person")
    Position: Optional[str] = Field(
        default=None, description="The current position of a person"
    )
    Research_interest: Optional[str] = Field(
        default=None, description="Research interest of a person"
    )
class Data(BaseModel):
    """Extracted data about people."""

    # Creates a model so that we can extract multiple entities.
    people: List[Person]