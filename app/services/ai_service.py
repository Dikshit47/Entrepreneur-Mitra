"""Explainable AI service strictly grounded in deterministic rule evaluations."""
from sqlalchemy.orm import Session, joinedload
from app.models.scheme import Scheme
from app.schemas.ai import AIExplainRequest, AIExplainResponse
from app.services.profile_service import ProfileService
from app.rules.engine import evaluate_scheme_rules
from app.utils.exceptions import NotFoundException


class AIService:
    @staticmethod
    def explain_eligibility(db: Session, req: AIExplainRequest) -> AIExplainResponse:
        profile = ProfileService.get_profile(db, req.profile_id)
        scheme = db.query(Scheme).options(
            joinedload(Scheme.rules),
            joinedload(Scheme.sources)
        ).filter(Scheme.scheme_id == req.scheme_id).first()

        if not scheme:
            raise NotFoundException(resource="Scheme", identifier=req.scheme_id)

        eval_res = evaluate_scheme_rules(scheme, profile.attributes)

        key_points = []
        for c in eval_res.criteria:
            if c.result == "PASS":
                key_points.append(f"✓ {c.field_name.replace('_', ' ').title()}: Shart poori hai ({c.reason})")
            elif c.result == "FAIL":
                key_points.append(f"✗ {c.field_name.replace('_', ' ').title()}: Shart anupayukt hai ({c.reason})")
            elif c.result == "UNKNOWN":
                key_points.append(f"? {c.field_name.replace('_', ' ').title()}: Jaankari pending hai")

        # Non-hallucinatory plain language synthesis
        if eval_res.status == "ELIGIBLE":
            plain_explanation = (
                f"Badhai ho! Aapki profile '{scheme.name}' ke sabhi niyamit nirdharit criteria ko poora karti hai. "
                "Aap is scheme ke antargat concessional loan ya subsidy ke liye aavedan kar sakte hain."
            )
            next_steps = [
                "Zaroori documents (Aadhaar, Aamdani Praman Patra, Project Report) taiyar karein.",
                "Apne nazdeeki channel partner (SCA / Bank) branch mein sampark karein.",
                "Official portal par jakar online aavedan form bharein."
            ]
        elif eval_res.status == "PARTIALLY_ELIGIBLE":
            plain_explanation = (
                f"Aapki profile '{scheme.name}' ke mukhya niyamon ko poora karti hai, kintu kuch niyam jaise "
                f"{', '.join(eval_res.failed_rules)} par vishesh dhyan dene ki zaroorat hai."
            )
            next_steps = [
                "What-If simulator mein jaakar dekhein ki kya badlav se poori eligibility mil sakti hai.",
                "Channel partner se special subvention ya relaxation ke vishay mein paramarsh lein."
            ]
        elif eval_res.status == "NOT_ELIGIBLE":
            plain_explanation = (
                f"Vartaman jaankari ke anusar aap '{scheme.name}' ke liye eligible nahi hain kyunki "
                f"{', '.join(eval_res.failed_rules)} shart poori nahi hui."
            )
            next_steps = [
                "Dusri sambandhit sarkari schemes check karein jo aapke profile se match karein.",
                "Profile attributes ki jaanch karein ki koi jankari galat to darj nahi hui."
            ]
        else:
            plain_explanation = (
                f"'{scheme.name}' ke liye aapki poori eligibility tay karne ke liye kuch jankari "
                f"({', '.join(eval_res.missing_information)}) baaki hai."
            )
            next_steps = [
                "Apni profile mein baaki bache huye fields ko update karein.",
                "Documents upload karein taaki auto-verification ho sake."
            ]

        grounding_source = scheme.official_url or "Official MoSJE Portal"

        return AIExplainResponse(
            scheme_id=scheme.scheme_id,
            language=req.language,
            decision=eval_res.status,
            plain_explanation=plain_explanation,
            key_points=key_points,
            next_steps=next_steps,
            grounding_source=grounding_source
        )
