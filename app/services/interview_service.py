"""Conversational AI Interview service for structured profile extraction."""
import os
import re
import logging
from typing import Dict, Any, List, Tuple, Optional
import httpx
from app.config import settings
from app.schemas.interview import InterviewTurnRequest, InterviewTurnResponse

logger = logging.getLogger(__name__)

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

        # 0. Applicant Name extraction
        name_patterns = [
            r'(?:my\s+name\s+is|i\s+am|i\'m|this\s+is)\s+([A-Za-z\u0900-\u097F]+(?:\s+[A-Za-z\u0900-\u097F]+){0,2})',
            r'(?:mera\s+naam|mera\s+name|humara\s+naam|मेरा\s+नाम)\s+(?:hai\s+)?([A-Za-z\u0900-\u097F]+(?:\s+[A-Za-z\u0900-\u097F]+){0,2})',
            r'(?:naam|name)\s*[:=-]\s*([A-Za-z\u0900-\u097F]+(?:\s+[A-Za-z\u0900-\u097F]+){0,2})',
            r'main\s+([A-Za-z\u0900-\u097F]+(?:\s+[A-Za-z\u0900-\u097F]+){0,2})\s+(?:bol\s+raha\s+hoon|bol\s+rahi\s+hoon|hoon)',
        ]
        stop_words = {
            "new", "business", "start", "shuru", "naya", "tailoring", "silai", "carpenter", "carpentry",
            "dairy", "shop", "ka", "ki", "ke", "hai", "karna", "chahiye", "ek", "mujhe", "mera", "meri", "hum",
            "and", "aur", "or", "from", "se", "in", "mein", "i", "run", "work", "live", "stay"
        }
        for pat in name_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                cand = m.group(1).strip().strip(".,;:!?")
                cand_words = []
                for w in cand.split():
                    if w.lower() in stop_words:
                        break
                    cand_words.append(w)
                if cand_words:
                    extracted["name"] = " ".join(w.capitalize() for w in cand_words)
                    break

        # 1. Business Type extraction
        if any(w in t for w in ["silai", "tailoring", "cloth", "garment", "kapde", "boutique", "stitching"]):
            extracted["business_type"] = "tailoring"
        elif any(w in t for w in ["carpentry", "carpenter", "badhai", "wood", "furniture", "lakdi"]):
            extracted["business_type"] = "carpentry"
        elif any(w in t for w in ["handicraft", "hastshilp", "handloom", "dastkari", "pottery", "bunkar"]):
            extracted["business_type"] = "handicraft"
        elif any(w in t for w in ["dairy", "doodh", "dairy farm", "pashupalan", "cattle", "gaay", "bhains"]):
            extracted["business_type"] = "dairy"
        elif any(w in t for w in ["kirana", "dukaan", "retail", "shop", "store", "grocery"]):
            extracted["business_type"] = "retail_store"
        elif any(w in t for w in ["food", "restaurant", "dhaba", "mithai", "bakery", "catering", "hotel"]):
            extracted["business_type"] = "food_processing"
        elif any(w in t for w in ["beauty", "parlour", "parlor", "salon", "barber", "hair"]):
            extracted["business_type"] = "salon"
        elif any(w in t for w in ["welding", "fabrication", "loha", "workshop", "garage", "mechanic", "repair"]):
            extracted["business_type"] = "workshop"
        elif any(w in t for w in ["electric", "electrical", "wiring", "electronics"]):
            extracted["business_type"] = "electrical"

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

        # 5. Category extraction (boundary-safe to prevent false positives on 'scheme', 'describe', etc.)
        if re.search(r'\b(?:sc|scheduled\s+caste|dalit|अनुसूचित\s+जाति)\b', t):
            extracted["caste_category"] = "SC"
        elif re.search(r'\b(?:st|scheduled\s+tribe|adivasi|tribal|अनुसूचित\s+जनजाति)\b', t):
            extracted["caste_category"] = "ST"
        elif re.search(r'\b(?:obc|other\s+backward|backward|pichhda|अन्य\s+पिछड़ा)\b', t):
            extracted["caste_category"] = "OBC"
        elif re.search(r'\b(?:general|samanya|सामान्य|ews)\b', t):
            extracted["caste_category"] = "GENERAL"

        # 6. Location / District / State extraction
        if re.search(r'\b(?:uttar\s+pradesh|up|u\.p\.)\b', t):
            extracted["state"] = "Uttar Pradesh"
        elif re.search(r'\bdelhi\b', t):
            extracted["state"] = "Delhi"
            extracted["district"] = "New Delhi"
        elif re.search(r'\bmaharashtra\b', t):
            extracted["state"] = "Maharashtra"

        districts = ["bijnor", "meerut", "lucknow", "varanasi", "kanpur", "agra", "pune", "mumbai", "ghaziabad", "noida"]
        for d in districts:
            if re.search(rf'\b{d}\b', t):
                extracted["district"] = d.title()
                break

        return extracted

    @classmethod
    def query_external_llm(cls, prompt: str, lang: str, attributes_so_far: Dict[str, Any]) -> Optional[str]:
        """Query Gemini or OpenAI if API keys are configured in settings or environment."""
        gemini_key = (
            getattr(settings, "GEMINI_API_KEY", "") 
            or os.environ.get("GEMINI_API_KEY", "") 
            or os.environ.get("GOOGLE_API_KEY", "")
        ).strip()
        openai_key = (
            getattr(settings, "OPENAI_API_KEY", "") 
            or os.environ.get("OPENAI_API_KEY", "")
        ).strip()

        sys_prompt = (
            "You are Entrepreneur Mitra (उद्यमी मित्र), an empathetic official AI assistant for the Ministry of Social Justice and Empowerment (MoSJE), Government of India. "
            "Your role is to guide marginalized entrepreneurs (SC, OBC, Safai Karamcharis, Divyangjan, Women) about concessional credit schemes "
            "(such as NBCFDC up to ₹15 Lakhs at 6% p.a., New Swarnima for women up to ₹2 Lakhs at 5% p.a., NSFDC up to ₹50 Lakhs, Stand-Up India up to ₹1 Crore, PMEGP up to 35% subsidy). "
            f"Respond concisely (2-3 sentences max) in {lang.upper()} (use polite, natural, encouraging tone). "
            f"Known applicant details so far: {attributes_so_far}. "
            "Never invent false schemes. Ground your answers in official MoSJE guidelines. "
            "Encourage the applicant and guide them toward completing their profile and reviewing matching schemes."
        )

        # 1. Try Google Gemini
        if gemini_key:
            for model_name in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}"
                    payload = {
                        "contents": [{
                            "parts": [{"text": f"{sys_prompt}\n\nUser Question: {prompt}"}]
                        }],
                        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 220}
                    }
                    with httpx.Client(timeout=6.0) as client:
                        resp = client.post(url, json=payload)
                        if resp.status_code == 200:
                            data = resp.json()
                            candidates = data.get("candidates", [])
                            if candidates:
                                parts = candidates[0].get("content", {}).get("parts", [])
                                if parts and "text" in parts[0]:
                                    return parts[0]["text"].strip()
                except Exception as e:
                    logger.warning(f"Gemini model {model_name} call failed: {e}")
                    continue

        # 2. Try OpenAI
        if openai_key:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 220
                }
                with httpx.Client(timeout=6.0) as client:
                    resp = client.post(url, json=payload, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        if content:
                            return content.strip()
            except Exception as e:
                logger.warning(f"OpenAI call failed: {e}")

        return None

    @classmethod
    def generate_smart_response(cls, text: str, lang: str, extracted: Dict[str, Any], next_prompt: Optional[str]) -> str:
        """Intelligent conversational reasoning engine for grounded MoSJE advice when offline or zero-key."""
        t = text.lower()

        # If entities were extracted, prioritize acknowledging them
        if extracted:
            found_items = []
            for k, v in extracted.items():
                if k == "name":
                    label = "Applicant Name" if lang == "en" else ("नाम" if lang == "hi" else "Name")
                elif k == "business_type":
                    label = "Business" if lang == "en" else ("व्यवसाय" if lang == "hi" else "Business")
                elif k == "project_cost":
                    label = "Project Cost" if lang == "en" else ("लागत" if lang == "hi" else "Project Cost")
                    v = f"₹{v:,}"
                elif k == "caste_category":
                    label = "Category" if lang == "en" else ("वर्ग" if lang == "hi" else "Category")
                elif k == "annual_family_income":
                    label = "Family Income" if lang == "en" else ("वार्षिक आय" if lang == "hi" else "Income")
                    v = f"₹{v:,}"
                elif k == "state":
                    label = "State" if lang == "en" else ("राज्य" if lang == "hi" else "State")
                elif k == "district":
                    label = "District" if lang == "en" else ("ज़िला" if lang == "hi" else "District")
                else:
                    label = k.replace("_", " ").title()
                found_items.append(f"{label}: {v}")
            found_str = ", ".join(found_items)

            followup = next_prompt if next_prompt else (
                "You can now review your verified government schemes." if lang == "en"
                else ("अब आप अपनी पात्र सरकारी योजनाएं देख सकते हैं।" if lang == "hi"
                else "Ab aap apni eligible sarkari schemes dekh sakte hain.")
            )

            if lang == "hi":
                return f"मैंने यह जानकारी नोट कर ली ({found_str})। {followup}"
            elif lang == "hinglish":
                return f"Maine ye jaankari note kar li ({found_str}). {followup}"
            else:
                return f"I have recorded these details ({found_str}). {followup}"

        # 1. Application Process / How to Apply
        if any(w in t for w in ["apply", "kaise apply", "kahan jana", "how to apply", "process", "portal", "form", "karna hoga", "steps"]):
            if lang == "hi":
                return (
                    "आवेदन की 3 सरल प्रक्रियाएं हैं: 1) अपनी प्रोफाइल पूरी कर 'योजनाएं' टैब में पात्र स्कीम चुनें, "
                    "2) 'दस्तावेज़' टैब में DigiLocker से 1-क्लिक सत्यापन करें, 3) 'सहयोगी केंद्र' (Channel Partners) टैब में अपने नज़दीकी बैंक या SCA शाखा में जाएं। "
                    f"{next_prompt or 'कृपया अपने व्यवसाय या अपेक्षित ऋण राशि के बारे में बताएं।'}"
                )
            elif lang == "hinglish":
                return (
                    "Apply karne ke 3 aasan steps hain: 1) Profile complete karke 'Schemes' tab me match dekhein, "
                    "2) 'Documents' tab me DigiLocker se 1-click verify karein, 3) 'Partners' tab se nazdeeki bank branch ya SCA office me apply karein. "
                    f"{next_prompt or 'Kripya apne business ya zaroori loan amount ke baare mein batayein.'}"
                )
            else:
                return (
                    "3 Simple steps to apply: 1) Complete your profile and check eligible matches in 'Schemes' tab, "
                    "2) Perform instant paperless verification via DigiLocker in 'Documents' tab, "
                    "3) Connect with your nearest State Channelising Agency (SCA) or Bank in 'Partners' tab. "
                    f"{next_prompt or 'Please share your enterprise type or loan requirement.'}"
                )

        # 2. Scheme Inquiries
        if any(w in t for w in ["scheme", "yojana", "loan", "subsidies", "nbcfdc", "nsfdc", "nskfdc", "swarnima", "pmegp", "standup", "batao", "kaunsi", "konsi"]):
            if lang == "hi":
                return (
                    "MoSJE के अंतर्गत प्रमुख रियायती योजनाएं: "
                    "1) NBCFDC सामान्य ऋण योजना (₹15 लाख तक, 6% ब्याज दर), "
                    "2) नई स्वर्णिमा योजना (महिलाओं हेतु ₹2 लाख, 5% ब्याज, 0% मार्जिन), "
                    "3) Stand-Up India (₹10 लाख से ₹1 करोड़), "
                    "4) PMEGP (35% तक ग्रामीण पूंजीगत सब्सिडी)। "
                    f"{next_prompt or 'आपका व्यवसाय किस राज्य (State) या जिले में स्थित है?'}"
                )
            elif lang == "hinglish":
                return (
                    "MoSJE ke antargat mukhya schemes: "
                    "1) NBCFDC General Term Loan (up to Rs. 15 Lakhs, 6% interest), "
                    "2) New Swarnima for Women (up to Rs. 2 Lakhs, 5% interest), "
                    "3) PMEGP (up to 35% capital subsidy), "
                    "4) Stand-Up India (Rs. 10 Lakhs to Rs. 1 Crore). "
                    f"{next_prompt or 'Aapka business kis rajya (State) ya zila (District) mein sthit hai?'}"
                )
            else:
                return (
                    "Key MoSJE concessional schemes available: "
                    "1) NBCFDC General Term Loan (up to ₹15 Lakhs at 6% p.a.), "
                    "2) New Swarnima Scheme for Women (up to ₹2 Lakhs at 5% p.a., 0% margin money), "
                    "3) Stand-Up India (₹10 Lakhs to ₹1 Crore), "
                    "4) PMEGP (up to 35% rural capital subsidy). "
                    f"{next_prompt or 'In which state or district is your business located?'}"
                )

        # 3. Interest / Rate / Tenure / Moratorium Inquiries
        if any(w in t for w in ["interest", "byaj", "byaaj", "kitna loan", "amount", "tenure", "rate", "moratorium", "emi"]):
            if lang == "hi":
                return (
                    "सरकारी योजनाओं में ब्याज दर केवल 4% से 6% प्रति वर्ष होती है (सामान्य बैंक ऋण 12-16% के मुकाबले) "
                    "और 6 से 36 महीने का मोराटोरियम (EMI छूट) मिलता है। 'कैलकुलेटर' टैब में आप अपनी सटीक EMI देख सकते हैं। "
                    f"{next_prompt or 'आपका व्यवसाय किस राज्य (State) या जिले में स्थित है?'}"
                )
            elif lang == "hinglish":
                return (
                    "Sarkari concessional schemes mein byaj dar sirf 4% se 6% p.a. hoti hai "
                    "(market rate 12-16% ke muqable) aur 6-36 mahine ka moratorium milta hai. 'Calculator' tab se aap apni EMI nikaal sakte hain. "
                    f"{next_prompt or 'Aapka business kis rajya (State) ya zila (District) mein sthit hai?'}"
                )
            else:
                return (
                    "Government concessional schemes offer preferential interest rates of 4% to 6% per annum "
                    "(compared to commercial 12-16%) with a 6 to 36 month repayment moratorium. Use our 'Calculator' tab to simulate exact EMIs. "
                    f"{next_prompt or 'In which state or district is your business located?'}"
                )

        # 4. Subsidy / Subvention Inquiries
        if any(w in t for w in ["subsidy", "choot", "discount", "free", "anudaan", "grant"]):
            if lang == "hi":
                return (
                    "PMEGP एवं MoSJE योजनाओं में ग्रामीण क्षेत्र के विशेष वर्गों (SC/ST/OBC/महिला) को 25% से 35% तक पूंजीगत सब्सिडी (Capital Subsidy) मिलती है, "
                    "जो कि वापस नहीं लौटानी होती। "
                    f"{next_prompt or 'आपका उद्यम किस जिले या राज्य में स्थित है?'}"
                )
            elif lang == "hinglish":
                return (
                    "PMEGP aur MoSJE schemes mein rural SC/ST/OBC aur women entrepreneurs ko 25% se 35% tak capital subsidy milti hai, "
                    "jo wapas nahi karni hoti. "
                    f"{next_prompt or 'Aapka udhyam kis zila ya rajya mein sthit hai?'}"
                )
            else:
                return (
                    "Under PMEGP and MoSJE programs, special category entrepreneurs (SC/ST/OBC/Women) in rural areas can receive 25% to 35% non-refundable capital subsidy. "
                    f"{next_prompt or 'In which state or district is your enterprise located?'}"
                )

        # 5. Documents / DigiLocker Inquiries
        if any(w in t for w in ["document", "documents", "kagaz", "praman patra", "certificate", "aadhaar", "digilocker", "verify", "sand box", "sandbox"]):
            if lang == "hi":
                return (
                    "मुख्य आवश्यक दस्तावेज़: 1) जाति प्रमाण पत्र (Caste Certificate), 2) आय प्रमाण पत्र (Income < ₹3 Lakh), "
                    "3) आधार कार्ड, 4) प्रोजेक्ट रिपोर्ट। आप 'दस्तावेज़' टैब में जाकर DigiLocker से 1-क्लिक में तुरंत सत्यापित कर सकते हैं। "
                    f"{next_prompt or 'आपका व्यवसाय किस राज्य (State) या जिले में स्थित है?'}"
                )
            elif lang == "hinglish":
                return (
                    "Zaroori documents: 1) Caste Certificate, 2) Income Certificate (under Rs 3 Lakh), "
                    "3) Aadhaar Card, 4) Project Proposal. DigiLocker tab se aap 1-click paperless verify kar sakte hain. "
                    f"{next_prompt or 'Aapka business kis rajya (State) ya zila (District) mein sthit hai?'}"
                )
            else:
                return (
                    "Key required documents: 1) Caste Certificate, 2) Income Certificate (family income under ₹3 Lakh/year), "
                    "3) Aadhaar Card, 4) Project Quotation. You can use DigiLocker Sandbox in the Documents tab for instant paperless verification. "
                    f"{next_prompt or 'In which state or district is your business located?'}"
                )

        # 6. Partners / Bank branches / Where to visit
        if any(w in t for w in ["partner", "bank", "branch", "sca", "kahan milega", "kahan se", "address", "kendra", "office"]):
            if lang == "hi":
                return (
                    "आप हमारे 'सहयोगी केंद्र' (Channel Partners) टैब में जाकर अपने जिले के सभी राज्य चैनेलाइजिंग एजेंसी (SCA), "
                    "बैंक और कॉमन सर्विस सेंटर (CSC) का पता, दूरी और फ़ोन नंबर देख सकते हैं। "
                    f"{next_prompt or 'कृपया अपने व्यवसाय या अपेक्षित ऋण राशि के बारे में बताएं।'}"
                )
            elif lang == "hinglish":
                return (
                    "Aap hamare 'Partners' tab mein jaakar apne zila ke State Channelising Agency (SCA), "
                    "lead bank branch aur CSC centers ka address, distance aur contact number dekh sakte hain. "
                    f"{next_prompt or 'Kripya apne business ya zaroori loan amount ke baare mein batayein.'}"
                )
            else:
                return (
                    "You can visit the 'Partners' tab to locate your nearest State Channelising Agencies (SCAs), "
                    "commercial bank branches, and Common Service Centers with turn-by-turn routing and contact details. "
                    f"{next_prompt or 'Please share your enterprise type or loan requirement.'}"
                )

        # 7. Greetings / Polite conversation
        if any(w in t for w in ["namaste", "hello", "hi", "hey", "pranam", "kese ho", "kaise ho", "help", "shuru", "start"]):
            if lang == "hi":
                return (
                    "नमस्ते! मैं उद्यमी मित्र हूँ। सामाजिक न्याय और अधिकारिता मंत्रालय (MoSJE) की रियायती योजनाओं से ऋण व सब्सिडी पाने में मैं आपकी पूरी सहायता करूँगा। "
                    "कृपया बताएं, आप किस प्रकार का व्यवसाय शुरू करना चाहते हैं या करते हैं?"
                )
            elif lang == "hinglish":
                return (
                    "Namaste! Main Entrepreneur Mitra hoon. MoSJE ki concessional schemes aur loan pane mein aapki poori madad karunga. "
                    "Kripya batayein, aap kis tarah ka business karte hain ya shuru karna chahte hain?"
                )
            else:
                return (
                    "Hello! I am Entrepreneur Mitra. I will help connect you to verified concessional loans and subsidies under the Ministry of Social Justice and Empowerment. "
                    "What type of business or trade do you operate or want to start?"
                )

        # 8. Gratitude / Affirmation
        if any(w in t for w in ["thank", "dhanyawad", "shukriya", "theek hai", "ok", "acha", "achha", "sahi"]):
            if lang == "hi":
                return (
                    "आपका स्वागत है! यदि आपके कोई और प्रश्न हैं, तो निसंकोच पूछें या 'योजनाएं' टैब में जाकर अपनी उपयुक्त योजनाएं देखें। "
                    f"{next_prompt or ''}"
                )
            elif lang == "hinglish":
                return (
                    "Aapka swagat hai! Agar koi aur sawaal ho to zaroor poochein, ya 'Schemes' tab me jaakar eligible yojnaayein dekhein. "
                    f"{next_prompt or ''}"
                )
            else:
                return (
                    "You are welcome! Feel free to ask any other questions or check your eligible schemes in the 'Schemes' tab. "
                    f"{next_prompt or ''}"
                )

        # Default dynamic response: helpful, encouraging, and never rigid
        if lang == "hi":
            return f"समझ गया। {next_prompt or 'कृपया अपने व्यवसाय या अपेक्षित ऋण राशि के बारे में बताएं, ताकि मैं सबसे उपयुक्त योजना खोज सकूँ।'}"
        elif lang == "hinglish":
            return f"Samajh gaya. {next_prompt or 'Kripya apne business ya zaroori loan amount ke baare mein batayein, taaki main sabse behtar scheme dhoondh sakoon.'}"
        else:
            return f"Understood. {next_prompt or 'Please tell me about your business or expected loan amount so I can find the best matching schemes for you.'}"

    @classmethod
    def process_turn(
        cls,
        turn_req: InterviewTurnRequest,
        existing_attributes: Dict[str, Any]
    ) -> InterviewTurnResponse:
        """Processes one conversational turn and decides the next question in selected language."""
        lang = (turn_req.language or "en").lower()
        prompt_list = CORE_FIELD_PROMPTS.get(lang) or CORE_FIELD_PROMPTS.get("en")
        
        req_text = turn_req.get_text() if hasattr(turn_req, "get_text") else (getattr(turn_req, "text", "") or "")
        extracted = cls.extract_fields_from_utterance(req_text)
        
        # Merge existing with newly extracted
        merged = existing_attributes.copy()
        merged.update(extracted)

        # Find next missing core field
        next_field = None
        next_prompt = None
        for field, prompt in prompt_list:
            if field not in merged or merged[field] is None or merged[field] == "":
                next_field = field
                next_prompt = prompt
                break

        # Calculate progress
        filled_count = sum(1 for f, _ in prompt_list if f in merged and merged[f] is not None and merged[f] != "")
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
            # 1. Check if an external LLM key is configured (Gemini or OpenAI)
            llm_reply = cls.query_external_llm(req_text, lang, merged)
            if llm_reply:
                reply = llm_reply
            else:
                # 2. Use intelligent grounded conversational engine
                reply = cls.generate_smart_response(req_text, lang, extracted, next_prompt)
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
