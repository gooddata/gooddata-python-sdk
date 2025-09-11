# (C) 2025 GoodData Corporation
"""This module defines the AnalyticalObjects Pydantic model.

The model is used to represent features of analytical objects important for
checking the validity of references.
"""

from pydantic import BaseModel, Field


class Attributes(BaseModel):
    title: str
    are_relations_valid: bool = Field(alias="areRelationsValid")


class AnalyticalObject(BaseModel):
    id: str
    type: str
    attributes: Attributes


class AnalyticalObjects(BaseModel):
    """Simplified model representing response obtained from GoodData API when querying
    analytical objects.

    This model is used to represent analytical objects such as metrics, visualizations,
    and dashboard in a simplified manner, with the purpose of checkinf the validity
    of references of these objects.

    This is not a complete schema of the analytical objects!
    """

    data: list[AnalyticalObject]
