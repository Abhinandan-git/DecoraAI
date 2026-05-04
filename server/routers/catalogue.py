"""
routers/catalogue.py
---------------------
Floor plan element catalogue.

GET /api/catalogue  →  list[CatalogueItem]
"""

from fastapi import APIRouter

from models.catalogue import CatalogueItem
from services.catalogue_service import get_all_items

router = APIRouter(prefix="/api", tags=["catalogue"])


@router.get(
    "/catalogue",
    response_model=list[CatalogueItem],
    summary="Return all SVG floor plan elements",
)
def catalogue() -> list[CatalogueItem]:
    return get_all_items()
