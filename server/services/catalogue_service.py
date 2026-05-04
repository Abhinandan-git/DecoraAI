"""
services/catalogue_service.py
-------------------------------
Floor plan element catalogue.

All SVG strings use `currentColor` so the frontend can tint them
with CSS/inline color without modifying the markup.

To load from a database or JSON file instead, replace `_ITEMS` with
a DB query and keep `get_all_items()` as the public API.
"""

from models.catalogue import CatalogueItem

# ── Static catalogue ─────────────────────────────────────────────────────────

_ITEMS: list[CatalogueItem] = [
    # ── Walls ─────────────────────────────────────────────────────────────────
    CatalogueItem(
        id="wall-h", label="Wall H", category="walls",
        defaultWidth=120, defaultHeight=12,
        svg='<svg viewBox="0 0 120 12" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="120" height="12" fill="currentColor"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="wall-v", label="Wall V", category="walls",
        defaultWidth=12, defaultHeight=120,
        svg='<svg viewBox="0 0 12 120" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="12" height="120" fill="currentColor"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="wall-corner", label="Corner", category="walls",
        defaultWidth=72, defaultHeight=72,
        svg='<svg viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="12" height="72" fill="currentColor"/>'
            '<rect x="12" y="0" width="60" height="12" fill="currentColor"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="wall-t", label="T-Wall", category="walls",
        defaultWidth=72, defaultHeight=72,
        svg='<svg viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="72" height="12" fill="currentColor"/>'
            '<rect x="30" y="12" width="12" height="60" fill="currentColor"/>'
            '</svg>',
    ),

    # ── Openings ──────────────────────────────────────────────────────────────
    CatalogueItem(
        id="door-single", label="Door", category="openings",
        defaultWidth=80, defaultHeight=80,
        svg='<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="8" height="80" fill="currentColor"/>'
            '<rect x="8" y="72" width="72" height="8" fill="currentColor"/>'
            '<path d="M8 0 L80 0" stroke="currentColor" stroke-width="8" fill="none"/>'
            '<path d="M16 8 Q16 72 72 72" stroke="currentColor" stroke-width="1.5"'
            ' fill="none" stroke-dasharray="4 3" opacity="0.5"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="door-double", label="Double Door", category="openings",
        defaultWidth=120, defaultHeight=80,
        svg='<svg viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="8" height="80" fill="currentColor"/>'
            '<rect x="112" y="0" width="8" height="80" fill="currentColor"/>'
            '<rect x="8" y="72" width="104" height="8" fill="currentColor"/>'
            '<path d="M8 0 L112 0" stroke="currentColor" stroke-width="8" fill="none"/>'
            '<path d="M16 8 Q16 68 60 72" stroke="currentColor" stroke-width="1.5"'
            ' fill="none" stroke-dasharray="4 3" opacity="0.5"/>'
            '<path d="M104 8 Q104 68 60 72" stroke="currentColor" stroke-width="1.5"'
            ' fill="none" stroke-dasharray="4 3" opacity="0.5"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="window", label="Window", category="openings",
        defaultWidth=80, defaultHeight=16,
        svg='<svg viewBox="0 0 80 16" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="80" height="16" fill="currentColor" opacity="0.15"/>'
            '<rect x="0" y="0" width="80" height="4" fill="currentColor"/>'
            '<rect x="0" y="12" width="80" height="4" fill="currentColor"/>'
            '<line x1="40" y1="0" x2="40" y2="16" stroke="currentColor" stroke-width="1.5"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="sliding-door", label="Sliding", category="openings",
        defaultWidth=80, defaultHeight=16,
        svg='<svg viewBox="0 0 80 16" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="80" height="16" fill="currentColor" opacity="0.1"/>'
            '<rect x="0" y="0" width="80" height="4" fill="currentColor"/>'
            '<rect x="0" y="12" width="80" height="4" fill="currentColor"/>'
            '<rect x="4" y="4" width="36" height="8" fill="currentColor" opacity="0.4" rx="1"/>'
            '<rect x="40" y="4" width="36" height="8" fill="currentColor" opacity="0.25" rx="1"/>'
            '<line x1="22" y1="4" x2="22" y2="12" stroke="currentColor" stroke-width="1"/>'
            '<line x1="58" y1="4" x2="58" y2="12" stroke="currentColor" stroke-width="1" opacity="0.5"/>'
            '</svg>',
    ),

    # ── Furniture ─────────────────────────────────────────────────────────────
    CatalogueItem(
        id="sofa", label="Sofa", category="furniture",
        defaultWidth=120, defaultHeight=60,
        svg='<svg viewBox="0 0 120 60" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="10" width="120" height="50" rx="6" fill="currentColor"'
            ' opacity="0.15" stroke="currentColor" stroke-width="2"/>'
            '<rect x="0" y="10" width="120" height="18" rx="6" fill="currentColor"'
            ' opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="0" y="10" width="16" height="50" rx="4" fill="currentColor"'
            ' opacity="0.4" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="104" y="10" width="16" height="50" rx="4" fill="currentColor"'
            ' opacity="0.4" stroke="currentColor" stroke-width="1.5"/>'
            '<line x1="60" y1="28" x2="60" y2="60" stroke="currentColor"'
            ' stroke-width="1" opacity="0.3"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="bed-single", label="Single Bed", category="furniture",
        defaultWidth=80, defaultHeight=120,
        svg='<svg viewBox="0 0 80 120" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="2" y="2" width="76" height="116" rx="4" fill="currentColor"'
            ' opacity="0.12" stroke="currentColor" stroke-width="2"/>'
            '<rect x="6" y="6" width="68" height="30" rx="3" fill="currentColor"'
            ' opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="6" y="42" width="68" height="70" rx="2" fill="currentColor"'
            ' opacity="0.18" stroke="currentColor" stroke-width="1"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="bed-double", label="Double Bed", category="furniture",
        defaultWidth=120, defaultHeight=120,
        svg='<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="2" y="2" width="116" height="116" rx="4" fill="currentColor"'
            ' opacity="0.12" stroke="currentColor" stroke-width="2"/>'
            '<rect x="6" y="6" width="108" height="30" rx="3" fill="currentColor"'
            ' opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="6" y="6" width="50" height="30" rx="3" fill="currentColor" opacity="0.15"/>'
            '<rect x="6" y="42" width="108" height="72" rx="2" fill="currentColor"'
            ' opacity="0.18" stroke="currentColor" stroke-width="1"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="desk", label="Desk", category="furniture",
        defaultWidth=100, defaultHeight=55,
        svg='<svg viewBox="0 0 100 55" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="2" y="2" width="96" height="51" rx="2" fill="currentColor"'
            ' opacity="0.12" stroke="currentColor" stroke-width="2"/>'
            '<rect x="2" y="2" width="96" height="10" rx="2" fill="currentColor"'
            ' opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="4" y="16" width="40" height="35" rx="1" fill="currentColor"'
            ' opacity="0.08" stroke="currentColor" stroke-width="1"/>'
            '<rect x="6" y="18" width="36" height="5" rx="1" fill="currentColor" opacity="0.2"/>'
            '<rect x="6" y="25" width="36" height="5" rx="1" fill="currentColor" opacity="0.15"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="dining-table", label="Table", category="furniture",
        defaultWidth=100, defaultHeight=70,
        svg='<svg viewBox="0 0 100 70" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="10" y="10" width="80" height="50" rx="3" fill="currentColor"'
            ' opacity="0.15" stroke="currentColor" stroke-width="2"/>'
            '<rect x="14" y="4" width="18" height="12" rx="3" fill="currentColor"'
            ' opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="68" y="4" width="18" height="12" rx="3" fill="currentColor"'
            ' opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="14" y="54" width="18" height="12" rx="3" fill="currentColor"'
            ' opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '<rect x="68" y="54" width="18" height="12" rx="3" fill="currentColor"'
            ' opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
            '</svg>',
    ),

    # ── Fixtures ──────────────────────────────────────────────────────────────
    CatalogueItem(
        id="toilet", label="Toilet", category="fixtures",
        defaultWidth=48, defaultHeight=68,
        svg='<svg viewBox="0 0 48 68" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="6" y="0" width="36" height="20" rx="3" fill="currentColor"'
            ' opacity="0.2" stroke="currentColor" stroke-width="1.5"/>'
            '<ellipse cx="24" cy="48" rx="20" ry="18" fill="currentColor"'
            ' opacity="0.15" stroke="currentColor" stroke-width="2"/>'
            '<ellipse cx="24" cy="48" rx="14" ry="13" fill="currentColor"'
            ' opacity="0.08" stroke="currentColor" stroke-width="1"/>'
            '<rect x="10" y="18" width="28" height="6" rx="1" fill="currentColor"'
            ' opacity="0.3" stroke="currentColor" stroke-width="1"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="bathtub", label="Bathtub", category="fixtures",
        defaultWidth=70, defaultHeight=130,
        svg='<svg viewBox="0 0 70 130" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="2" y="2" width="66" height="126" rx="10" fill="currentColor"'
            ' opacity="0.15" stroke="currentColor" stroke-width="2"/>'
            '<rect x="8" y="8" width="54" height="114" rx="8" fill="currentColor"'
            ' opacity="0.08" stroke="currentColor" stroke-width="1"/>'
            '<circle cx="35" cy="100" r="8" fill="none" stroke="currentColor"'
            ' stroke-width="1.5" opacity="0.5"/>'
            '<circle cx="35" cy="100" r="2" fill="currentColor" opacity="0.4"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="sink", label="Sink", category="fixtures",
        defaultWidth=56, defaultHeight=50,
        svg='<svg viewBox="0 0 56 50" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="2" y="2" width="52" height="46" rx="4" fill="currentColor"'
            ' opacity="0.15" stroke="currentColor" stroke-width="2"/>'
            '<rect x="8" y="8" width="40" height="34" rx="8" fill="currentColor"'
            ' opacity="0.08" stroke="currentColor" stroke-width="1"/>'
            '<circle cx="28" cy="25" r="4" fill="none" stroke="currentColor"'
            ' stroke-width="1.5" opacity="0.5"/>'
            '<circle cx="28" cy="25" r="1.5" fill="currentColor" opacity="0.4"/>'
            '</svg>',
    ),
    CatalogueItem(
        id="staircase", label="Stairs", category="fixtures",
        defaultWidth=80, defaultHeight=120,
        svg='<svg viewBox="0 0 80 120" xmlns="http://www.w3.org/2000/svg">'
            '<rect x="0" y="0" width="80" height="120" fill="currentColor"'
            ' opacity="0.05" stroke="currentColor" stroke-width="2"/>'
            + "".join(
            f'<line x1="0" y1="{y}" x2="80" y2="{y}" stroke="currentColor"'
            f' stroke-width="1.5" opacity="0.6"/>'
            for y in range(10, 121, 12)
        )
            + '<path d="M10 110 L70 10" stroke="currentColor" stroke-width="1.5"'
              ' opacity="0.3" stroke-dasharray="3 3"/>'
              '</svg>',
    ),
]


# ── Public API ────────────────────────────────────────────────────────────────

def get_all_items() -> list[CatalogueItem]:
    """Return all catalogue items. Replace with a DB query when ready."""
    return _ITEMS


def get_item_by_id(item_id: str) -> CatalogueItem | None:
    return next((i for i in _ITEMS if i.id == item_id), None)
