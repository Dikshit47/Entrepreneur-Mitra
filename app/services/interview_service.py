"""Conversational AI Interview service for structured profile extraction."""
import re
from typing import Dict, Any, List, Tuple
from app.schemas.interview import InterviewTurnRequest, InterviewTurnResponse

CORE_FIELD_PROMPTS = [
    ("business_type", "Aap kis tarah ka business karte hain ya shuru karna chahte hain? (Jaise Silai, Handicraft, Dairy, Dukaan)"),
    ("project_cost", "Aapke business mein lagbhag kitne rupaye ki zaroorat hai?"),
    ("state", "Aapka business kis rajya (State) mein sthit hai?"),
    ("district", "Aap kis zila (District) mein apna business shuru karna chahte hain?"),
    ("annual_family_income", "Aapke parivar ki saalana aamdani (Annual Family Income) lagbhag kitni hai?"),
    ("caste_category", "Sarkari scheme labh ke liye, aap kis category se sambandhit hain? (SC / OBC / EWS / General)"),
    ("business_stage", "Kya ye naya business hai ya pehle se chal raha hai?")
]


class InterviewService:
    @staticmethod
    def extract_fields_from_utterance(text: str) -> Dict[str, Any]:
        """
        Extracts structured profile attributes from conversational speech/text.
        Deterministic regex/NLP extraction with validation.
        """
        extracted: Dict[str, Any] = {}
        t = text.lower()

        # 1. Business Type extraction
        if any(w in t for w in ["silai", "tailoring", "cloth", "garment", "kapde"]):
            extracted["business_type"] = "tailoring"
        elif any(w in t for w in ["handicraft", "hastshilp", "handloom", "dastkari"]):
            extracted["business_type"] = "handicraft"
        elif any(w in t for w in ["dairy", "doodh", "dairy farm", "pashupalan"]):
            extracted["business_type"] = "dairy"
        elif any(w in t for w in ["kirana", "dukaan", "retail", "shop"]):
            extracted["business_type"] = "retail_store"
        elif any(w in t for w in ["food", "restaurant", "dhaba", "mithai", "bakery"]):
            extracted["business_type"] = "food_processing"

        # 2. Business Stage extraction
        if any(w in t for w in ["shuru", "naya", "new", "start", "fresh"]):
            extracted["business_stage"] = "new"
        elif any(w in t for w in ["chal raha", "purana", "expansion", "badhana", "existing"]):
            extracted["business_stage"] = "expansion"

        # 3. Project Cost / Loan extraction (e.g. 3 lakh, 50000, 2.5L)
        lakh_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|laakh|lac|l)\b', t)
        if lakh_match:
            val = float(lakh_match.group(1)) * 100000
            extracted["project_cost"] = int(val)
            extracted["loan_required"] = int(val)
        else:
            num_match = re.search(r'\b(?:rs\.?|inr|rupaye|rupees)?\s*(\d{4,8})\b', t)
            if num_match:
                val = int(num_match.group(1))
                extracted["project_cost"] = val
                extracted["loan_required"] = val

        # 4. Income extraction
        income_match = re.search(r'(?:income|aamdani|kamai)\s*(?:hai)?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lac)?', t)
        if income_match:
            val_str = income_match.group(1)
            val = float(val_str)
            if "lakh" in t or "lac" in t or val < 100:
                val = val * 100000
            extracted["annual_family_income"] = int(val)

        # 5. Category extraction
        if "sc" in t or "scheduled caste" in t or "dalit" in t:
            extracted["caste_category"] = "SC"
        elif "obc" in t or "backward" in t or "pichhda" in t:
            extracted["caste_category"] = "OBC"
        elif "general" in t or "samanya" in t:
            extracted["caste_category"] = "GENERAL"

        # 6. Location / District / State extraction
        if "uttar pradesh" in t or "up" in t.split():
            extracted["state"] = "Uttar Pradesh"
        elif "delhi" in t:
            extracted["state"] = "Delhi"
            extracted["district"] = "New Delhi"
        elif "maharashtra" in t:
            extracted["state"] = "Maharashtra"

        districts = ["bijnor", "meerut", "lucknow", "varanasi", "kanpur", "agra", "pune", "mumbai"]
        for d in districts:
            if d in t:
                extracted["district"] = d.title()
                break

        return extracted

    @classmethod
    def process_turn(
        cls,
        turn_req: InterviewTurnRequest,
        existing_attributes: Dict[str, Any]
    ) -> InterviewTurnResponse:
        """Processes one conversational turn and decides the next question."""
        extracted = cls.extract_fields_from_utterance(turn_req.text)
        
        # Merge existing with newly extracted
        merged = existing_attributes.copy()
        merged.update(extracted)

        # Find next missing core field
        next_field = None
        next_prompt = None
        for field, prompt in CORE_FIELD_PROMPTS:
            if field not in merged or merged[field] is None:
                next_field = field
                next_prompt = prompt
                break

        # Calculate progress
        filled_count = sum(1 for f, _ in CORE_FIELD_PROMPTS if f in merged and merged[f] is not None)
        completeness = int((filled_count / len(CORE_FIELD_PROMPTS)) * 100)

        if next_field is None:
            reply = (
                "Dhanyawad! Aapki sabhi mukhya jaankari darj ho gayi hai. "
                "Ab aap apni profile confirm karke eligible sarkari schemes dekh sakte hain."
            )
            state = "ready_for_matching"
        else:
            if extracted:
                found_str = ", ".join(f"{k}: {v}" for k, v in extracted.items())
                reply = f"Maine ye jaankari note kar li ({found_str}). {next_prompt}"
            else:
                reply = f"Samajh gaya. {next_prompt}"
            state = "in_progress"

        return InterviewTurnResponse(
            assistant_message=reply,
            reply=reply,
            extracted_attributes=extracted,
            extracted_fields=extracted,
            next_required_field=next_field,
            next_question=next_prompt,
            requires_confirmation=True if extracted else False,
            profile_completeness_pct=completeness,
            conversation_state=state
        )
