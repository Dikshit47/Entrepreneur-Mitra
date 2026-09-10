"""Conversational AI Interview service for structured profile extraction."""
import re
from typing import Dict, Any, List, Tuple
from app.schemas.interview import InterviewTurnRequest, InterviewTurnResponse

CORE_FIELD_PROMPTS: Dict[str, List[Tuple[str, str]]] = {
    "en": [
        ("business_type", "What type of business or trade do you operate or want to start? (e.g., Tailoring, Handicraft, Dairy, Retail store)"),
        ("project_cost", "Approximately how much project funding or loan amount is required?"),
        ("state", "In which state is your business or enterprise located?"),
        ("district", "In which district are you establishing your business?"),
        ("annual_family_income", "What is your approximate annual family income in Rupees?"),
        ("caste_category", "For targeted government concessional schemes, which category do you belong to? (SC / OBC / EWS / General)"),
        ("business_stage", "Is this a new startup venture or an existing enterprise expansion?")
    ],
    "hi": [
        ("business_type", "आप किस प्रकार का व्यवसाय शुरू करना चाहते हैं या करते हैं? (जैसे सिलाई, हस्तशिल्प, डेयरी, दुकान)"),
        ("project_cost", "आपके व्यवसाय के लिए लगभग कितनी वित्तीय सहायता या ऋण की आवश्यकता है?"),
        ("state", "आपका व्यवसाय किस राज्य (State) में स्थित है?"),
        ("district", "आप किस जिले (District) में अपना उद्यम स्थापित कर रहे हैं?"),
        ("annual_family_income", "आपके परिवार की कुल वार्षिक आय (Annual Family Income) लगभग कितनी है?"),
        ("caste_category", "सरकारी रियायती योजना लाभ हेतु आप किस सामाजिक वर्ग से हैं? (SC / OBC / EWS / सामान्य)"),
        ("business_stage", "क्या यह नया व्यवसाय है अथवा पूर्व से चल रहे कार्य का विस्तार?")
    ],
    "hinglish": [
        ("business_type", "Aap kis tarah ka business karte hain ya shuru karna chahte hain? (Jaise Silai, Handicraft, Dairy, Dukaan)"),
        ("project_cost", "Aapke business mein lagbhag kitne rupaye ki zaroorat hai?"),
        ("state", "Aapka business kis rajya (State) mein sthit hai?"),
        ("district", "Aap kis zila (District) mein apna business shuru karna chahte hain?"),
        ("annual_family_income", "Aapke parivar ki saalana aamdani (Annual Family Income) lagbhag kitni hai?"),
        ("caste_category", "Sarkari scheme labh ke liye, aap kis category se sambandhit hain? (SC / OBC / EWS / General)"),
        ("business_stage", "Kya ye naya business hai ya pehle se chal raha hai?")
    ]
}


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
        """Processes one conversational turn and decides the next question in selected language."""
        lang = (turn_req.language or "en").lower()
        prompt_list = CORE_FIELD_PROMPTS.get(lang) or CORE_FIELD_PROMPTS.get("en")
        
        extracted = cls.extract_fields_from_utterance(turn_req.text)
        
        # Merge existing with newly extracted
        merged = existing_attributes.copy()
        merged.update(extracted)

        # Find next missing core field
        next_field = None
        next_prompt = None
        for field, prompt in prompt_list:
            if field not in merged or merged[field] is None:
                next_field = field
                next_prompt = prompt
                break

        # Calculate progress
        filled_count = sum(1 for f, _ in prompt_list if f in merged and merged[f] is not None)
        completeness = int((filled_count / len(prompt_list)) * 100)

        if next_field is None:
            if lang == "hi":
                reply = (
                    "धन्यवाद! आपकी सभी मुख्य जानकारी सफलतापूर्वक दर्ज कर ली गई है। "
                    "अब आप अपनी प्रोफ़ाइल की पुष्टि करके उपयुक्त सरकारी योजनाओं की जांच कर सकते हैं।"
                )
            elif lang == "hinglish":
                reply = (
                    "Dhanyawad! Aapki sabhi mukhya jaankari darj ho gayi hai. "
                    "Ab aap apni profile confirm karke eligible sarkari schemes dekh sakte hain."
                )
            else:
                reply = (
                    "Thank you! All your primary details have been successfully recorded. "
                    "You can now confirm your profile to discover verified government schemes."
                )
            state = "ready_for_matching"
        else:
            if extracted:
                found_str = ", ".join(f"{k}: {v}" for k, v in extracted.items())
                if lang == "hi":
                    reply = f"मैंने यह जानकारी नोट कर ली ({found_str})। {next_prompt}"
                elif lang == "hinglish":
                    reply = f"Maine ye jaankari note kar li ({found_str}). {next_prompt}"
                else:
                    reply = f"I have recorded these details ({found_str}). {next_prompt}"
            else:
                if lang == "hi":
                    reply = f"समझ गया। {next_prompt}"
                elif lang == "hinglish":
                    reply = f"Samajh gaya. {next_prompt}"
                else:
                    reply = f"Understood. {next_prompt}"
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
