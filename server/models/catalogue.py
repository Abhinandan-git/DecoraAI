"""models/catalogue.py — Catalogue item schema."""

from typing import Literal

from pydantic import BaseModel

CategoryId = Literal["walls", "openings", "furniture", "fixtures"]


class CatalogueItem(BaseModel):
    id: str
    label: str
    category: CategoryId
    defaultWidth: int
    defaultHeight: int
    svg: str
