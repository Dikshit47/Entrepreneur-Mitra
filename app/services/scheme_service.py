"""Scheme service."""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.scheme import Scheme, SchemeRule, SchemeBenefit, DocumentRequirement, SchemeSource
from app.schemas.scheme import SchemeOut, SchemeDetailOut
from app.utils.exceptions import NotFoundException


class SchemeService:
    @staticmethod
    def get_schemes(
        db: Session,
        status: Optional[str] = "ACTIVE",
        scheme_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[SchemeOut]:
        query = db.query(Scheme)
        if status:
            query = query.filter(Scheme.status == status)
        if scheme_type:
            query = query.filter(Scheme.scheme_type == scheme_type)
        if search:
            s_term = f"%{search.lower()}%"
            query = query.filter(
                (Scheme.name.ilike(s_term)) |
                (Scheme.description.ilike(s_term)) |
                (Scheme.target_group.ilike(s_term))
            )
        schemes = query.all()
        return [SchemeOut.model_validate(s) for s in schemes]

    @staticmethod
    def get_scheme_by_id(db: Session, scheme_id: str) -> SchemeDetailOut:
        scheme = db.query(Scheme).options(
            joinedload(Scheme.rules),
            joinedload(Scheme.benefits),
            joinedload(Scheme.required_documents),
            joinedload(Scheme.sources)
        ).filter(Scheme.scheme_id == scheme_id).first()

        if not scheme:
            raise NotFoundException(resource="Scheme", identifier=scheme_id)

        return SchemeDetailOut.model_validate(scheme)
