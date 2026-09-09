"""Profile service for managing entrepreneur profile and attributes."""
from typing import Dict, Any, Optional, List
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.profile import EntrepreneurProfile, ProfileAttribute
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileOut, AttributeSchema
from app.utils.exceptions import NotFoundException

CORE_PROFILE_FIELDS = [
    "business_type",
    "project_cost",
    "annual_family_income",
    "state",
    "district",
    "caste_category",
    "business_stage"
]


class ProfileService:
    @staticmethod
    def calculate_completeness(attributes: Dict[str, Any]) -> int:
        """Calculates profile completeness percentage based on core required fields."""
        if not attributes:
            return 0
        filled = sum(1 for f in CORE_PROFILE_FIELDS if f in attributes and attributes[f] is not None)
        return int((filled / len(CORE_PROFILE_FIELDS)) * 100)

    @classmethod
    def create_profile(cls, db: Session, prof_in: ProfileCreate, user_id: Optional[str] = None) -> ProfileOut:
        profile = EntrepreneurProfile(
            user_id=user_id,
            status="draft",
            preferred_language=prof_in.language
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

        # Upsert attributes
        cls.upsert_attributes(db, profile.id, prof_in.attributes, source="user_input")
        return cls.get_profile(db, profile.id)

    @classmethod
    def get_profile(cls, db: Session, profile_id: str) -> ProfileOut:
        profile = db.query(EntrepreneurProfile).filter(EntrepreneurProfile.id == profile_id).first()
        if not profile:
            raise NotFoundException(resource="Profile", identifier=profile_id)

        attrs = db.query(ProfileAttribute).filter(ProfileAttribute.profile_id == profile_id).all()
        attr_dict = {}
        attr_schemas = []
        for a in attrs:
            # Parse value
            val = a.attribute_value
            if a.data_type == "number":
                try:
                    val = float(val) if "." in val else int(val)
                except Exception:
                    pass
            elif a.data_type == "boolean":
                val = (val.lower() == "true")
            attr_dict[a.attribute_key] = val
            attr_schemas.append(AttributeSchema(
                key=a.attribute_key,
                value=val,
                data_type=a.data_type,
                source=a.source,
                confidence=a.confidence,
                user_confirmed=a.user_confirmed
            ))

        completeness = cls.calculate_completeness(attr_dict)
        return ProfileOut(
            profile_id=profile.id,
            user_id=profile.user_id,
            status=profile.status,
            language=profile.preferred_language,
            attributes=attr_dict,
            attribute_details=attr_schemas,
            completeness_pct=completeness,
            confirmed_at=profile.confirmed_at,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

    @classmethod
    def update_profile(cls, db: Session, profile_id: str, update_in: ProfileUpdate) -> ProfileOut:
        profile = db.query(EntrepreneurProfile).filter(EntrepreneurProfile.id == profile_id).first()
        if not profile:
            raise NotFoundException(resource="Profile", identifier=profile_id)

        if update_in.language:
            profile.preferred_language = update_in.language

        if update_in.attributes:
            cls.upsert_attributes(db, profile_id, update_in.attributes)

        db.commit()
        return cls.get_profile(db, profile_id)

    @staticmethod
    def upsert_attributes(db: Session, profile_id: str, attributes: Dict[str, Any], source: str = "user_input"):
        for k, v in attributes.items():
            if v is None:
                continue
            
            # Determine data type
            if isinstance(v, bool):
                dtype = "boolean"
                str_val = str(v).lower()
            elif isinstance(v, (int, float)):
                dtype = "number"
                str_val = str(v)
            else:
                dtype = "string"
                str_val = str(v).strip()

            existing = db.query(ProfileAttribute).filter(
                ProfileAttribute.profile_id == profile_id,
                ProfileAttribute.attribute_key == k
            ).first()

            if existing:
                existing.attribute_value = str_val
                existing.data_type = dtype
                existing.source = source
                existing.updated_at = datetime.now(timezone.utc)
            else:
                attr = ProfileAttribute(
                    profile_id=profile_id,
                    attribute_key=k,
                    attribute_value=str_val,
                    data_type=dtype,
                    source=source,
                    confidence=1.0,
                    user_confirmed=True
                )
                db.add(attr)
        db.commit()
