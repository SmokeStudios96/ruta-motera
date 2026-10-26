from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

_NUM = "(-?[0-9]+(?:[.][0-9]+)?)"
_WKT = re.compile("POINT[ ]*[(][ ]*" + _NUM + "[ ]+" + _NUM + "[ ]*[)]", re.IGNORECASE)


class POICategory(str, Enum):
    SCENIC_CURVE = "scenic_curve"
    BIKER_RESTAURANT = "biker_restaurant"
    MECHANIC = "mechanic"
    GAS_STATION = "gas_station"
    BIKER_HOTEL = "biker_hotel"
    CAMPING = "camping"


def _lng_lat(loc: Any) -> Optional[tuple[float, float]]:
    if isinstance(loc, dict):
        c = loc.get("coordinates")
        if isinstance(c, (list, tuple)) and len(c) >= 2:
            try:
                return float(c[0]), float(c[1])
            except (TypeError, ValueError):
                return None
    elif isinstance(loc, str):
        m = _WKT.search(loc)
        if m:
            return float(m.group(1)), float(m.group(2))
    return None


class POIBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    category: POICategory
    address: Optional[str] = Field(default=None, max_length=300)
    phone: Optional[str] = Field(default=None, max_length=50)
    website: Optional[str] = Field(default=None, max_length=500)

    model_config = ConfigDict(str_strip_whitespace=True)


class POICreate(POIBase):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)


class POIResponse(POIBase):
    id: UUID
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    created_by: Optional[UUID] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    @model_validator(mode="before")
    @classmethod
    def _compute_lat_lng(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if data.get("lat") is not None and data.get("lng") is not None:
            return data
        point = _lng_lat(data.get("location"))
        if point is None:
            raise ValueError("Faltan lat/lng y 'location' no es un Point valido")
        merged = dict(data)
        merged["lng"], merged["lat"] = point
        return merged


class POINearbyResponse(POIResponse):
    distance_meters: float = Field(ge=0)

