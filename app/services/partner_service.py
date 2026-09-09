"""Geo-spatial Partner Locator service with Haversine distance calculation."""
import math
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.partner import PartnerLocation
from app.schemas.partner import PartnerLocationOut, NearbyPartnerQuery


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two geographic points in kilometers."""
    R = 6371.0  # Earth radius in kilometers

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2) + \
        (math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return round(R * c, 2)


class PartnerService:
    @staticmethod
    def find_nearby_partners(
        db: Session,
        query_in: NearbyPartnerQuery
    ) -> List[PartnerLocationOut]:
        partners = db.query(PartnerLocation).filter(PartnerLocation.active == True).all()

        nearby_list = []
        for p in partners:
            dist = haversine_distance_km(query_in.latitude, query_in.longitude, p.latitude, p.longitude)
            if dist <= query_in.radius_km:
                cat_match = True
                if query_in.category:
                    cat_match = query_in.category.lower() in p.scheme_categories.lower()

                nearby_list.append(PartnerLocationOut(
                    partner_id=p.id,
                    name=p.partner_name,
                    partner_type=p.partner_type,
                    scheme_categories=p.scheme_categories,
                    distance_km=dist,
                    category_match=cat_match,
                    status="VERIFIED" if p.active else "UNVERIFIED",
                    fund_utilisation_status=p.fund_utilisation_status,
                    address=p.address,
                    district=p.district,
                    state=p.state,
                    pincode=p.pincode,
                    contact_number=p.contact_number,
                    latitude=p.latitude,
                    longitude=p.longitude
                ))

        # Sort by distance ascending
        nearby_list.sort(key=lambda x: x.distance_km)
        return nearby_list
