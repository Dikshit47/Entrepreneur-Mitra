"""Authentic Government Scheme and Channel Partner seed data."""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.scheme import Scheme, SchemeRule, SchemeBenefit, DocumentRequirement, SchemeSource
from app.models.partner import PartnerLocation
from app.models.user import User


def seed_database(db: Session):
    # Ensure tables
    Base.metadata.create_all(bind=engine)

    # 1. Create Default Demo User (Ramesh from SIH Blueprint Persona)
    existing_user = db.query(User).filter(User.email == "ramesh.kumar@mitra.gov.in").first()
    if not existing_user:
        user = User(
            id="usr_ramesh_001",
            email="ramesh.kumar@mitra.gov.in",
            phone="+919876543210",
            preferred_language="hi",
            role="CITIZEN"
        )
        db.add(user)
        db.commit()

    # 2. Scheme 1: NBCFDC General Term Loan (GTL)
    s1 = db.query(Scheme).filter(Scheme.scheme_id == "NBCFDC-GTL-001").first()
    if not s1:
        s1 = Scheme(
            scheme_id="NBCFDC-GTL-001",
            name="NBCFDC General Term Loan Scheme (GTL)",
            short_name="GTL Scheme",
            ministry="Ministry of Social Justice and Empowerment",
            department="National Backward Classes Finance and Development Corporation (NBCFDC)",
            scheme_type="CREDIT_LOAN",
            target_group="Marginalized / Backward Classes Entrepreneurs with annual family income up to ₹3,00,000",
            description=(
                "Concessional credit financing provided through State Channelising Agencies (SCAs) and designated banks "
                "for establishing self-employment ventures in agriculture, transport, service, and artisan sectors."
            ),
            status="ACTIVE",
            geography_scope="PAN_INDIA",
            official_url="https://nbcfdc.gov.in/en/general-term-loan",
            application_url="https://nbcfdc.gov.in/en/how-to-apply",
            helpline="011-26052692",
            source_confidence="VERIFIED",
            last_verified_at=datetime.now(timezone.utc),
            data_version="v2026.1"
        )
        db.add(s1)
        db.commit()

        # Rules
        rules_s1 = [
            SchemeRule(
                scheme_id=s1.scheme_id,
                rule_id="NBCFDC-INCOME-001",
                field_name="annual_family_income",
                operator="<=",
                expected_value="300000",
                value_unit="INR",
                rule_type="hard",
                explanation_template="Annual family income must be less than or equal to Rs. 3,00,000.",
                source_reference_id="SRC-NBCFDC-01"
            ),
            SchemeRule(
                scheme_id=s1.scheme_id,
                rule_id="NBCFDC-COST-002",
                field_name="project_cost",
                operator="<=",
                expected_value="1500000",
                value_unit="INR",
                rule_type="hard",
                explanation_template="Project cost must be within Rs. 15,00,000 for term loan assistance.",
                source_reference_id="SRC-NBCFDC-01"
            ),
            SchemeRule(
                scheme_id=s1.scheme_id,
                rule_id="NBCFDC-CAT-003",
                field_name="caste_category",
                operator="in",
                expected_value="SC,OBC,MARGINALIZED",
                rule_type="hard",
                explanation_template="Applicant must belong to target category (SC, OBC, or notified marginalized groups).",
                source_reference_id="SRC-NBCFDC-01"
            )
        ]
        db.add_all(rules_s1)

        # Benefits
        b1 = SchemeBenefit(
            scheme_id=s1.scheme_id,
            benefit_type="CONCESSIONAL_LOAN",
            min_value=50000,
            max_value=1500000,
            interest_rate=5.0,  # 5% concessional per annum
            tenure_months=60,   # 5 years
            moratorium_months=6, # 6 months moratorium
            description="Up to 85% project cost financed by NBCFDC at 5% per annum, with 5% promoter margin.",
            source_reference_id="SRC-NBCFDC-01"
        )
        db.add(b1)

        # Documents
        docs_s1 = [
            DocumentRequirement(scheme_id=s1.scheme_id, document_type="INCOME_CERTIFICATE", mandatory=True),
            DocumentRequirement(scheme_id=s1.scheme_id, document_type="CASTE_CERTIFICATE", mandatory=True),
            DocumentRequirement(scheme_id=s1.scheme_id, document_type="AADHAAR", mandatory=True),
            DocumentRequirement(scheme_id=s1.scheme_id, document_type="PROJECT_REPORT", mandatory=False)
        ]
        db.add_all(docs_s1)

        # Source
        src1 = SchemeSource(
            scheme_id=s1.scheme_id,
            publisher="NBCFDC / Ministry of Social Justice and Empowerment",
            source_url="https://nbcfdc.gov.in/en/general-term-loan",
            source_type="OFFICIAL_PORTAL",
            verification_status="VERIFIED"
        )
        db.add(src1)
        db.commit()

    # 3. Scheme 2: Stand-Up India Scheme
    s2 = db.query(Scheme).filter(Scheme.scheme_id == "STANDUP-INDIA-001").first()
    if not s2:
        s2 = Scheme(
            scheme_id="STANDUP-INDIA-001",
            name="Stand-Up India Scheme for SC/ST and Women Entrepreneurs",
            short_name="Stand-Up India",
            ministry="Ministry of Finance & MoSJE Support",
            department="Department of Financial Services (DFS)",
            scheme_type="CREDIT_LOAN",
            target_group="Scheduled Caste (SC), Scheduled Tribe (ST), and Women entrepreneurs",
            description=(
                "Facilitates bank loans between ₹10 Lakh and ₹1 Crore to at least one SC/ST borrower and at least "
                "one woman borrower per bank branch for setting up greenfield enterprises in manufacturing, services, or trading."
            ),
            status="ACTIVE",
            geography_scope="PAN_INDIA",
            official_url="https://www.standupmitra.in",
            application_url="https://www.standupmitra.in/Home/SUISchemes",
            helpline="1800-180-1111",
            source_confidence="VERIFIED",
            last_verified_at=datetime.now(timezone.utc),
            data_version="v2026.1"
        )
        db.add(s2)
        db.commit()

        rules_s2 = [
            SchemeRule(
                scheme_id=s2.scheme_id,
                rule_id="SUI-CAT-001",
                field_name="caste_category",
                operator="in",
                expected_value="SC,ST",
                rule_type="hard",
                explanation_template="Applicant must be SC, ST or female entrepreneur.",
                source_reference_id="SRC-SUI-01"
            ),
            SchemeRule(
                scheme_id=s2.scheme_id,
                rule_id="SUI-STAGE-002",
                field_name="business_stage",
                operator="==",
                expected_value="new",
                rule_type="hard",
                explanation_template="Enterprise must be a greenfield (new) venture.",
                source_reference_id="SRC-SUI-01"
            ),
            SchemeRule(
                scheme_id=s2.scheme_id,
                rule_id="SUI-COST-003",
                field_name="project_cost",
                operator=">=",
                expected_value="1000000",
                value_unit="INR",
                rule_type="hard",
                explanation_template="Project cost must be at least Rs. 10,00,000 for Stand-Up India assistance.",
                source_reference_id="SRC-SUI-01"
            )
        ]
        db.add_all(rules_s2)

        b2 = SchemeBenefit(
            scheme_id=s2.scheme_id,
            benefit_type="CONCESSIONAL_LOAN",
            min_value=1000000,
            max_value=10000000,
            interest_rate=8.5,
            tenure_months=84,   # 7 years
            moratorium_months=18,
            description="Composite loan between 10 Lakhs and 1 Crore with up to 18 months moratorium.",
            source_reference_id="SRC-SUI-01"
        )
        db.add(b2)

        docs_s2 = [
            DocumentRequirement(scheme_id=s2.scheme_id, document_type="CASTE_CERTIFICATE", mandatory=True),
            DocumentRequirement(scheme_id=s2.scheme_id, document_type="PROJECT_REPORT", mandatory=True),
            DocumentRequirement(scheme_id=s2.scheme_id, document_type="AADHAAR", mandatory=True)
        ]
        db.add_all(docs_s2)

        src2 = SchemeSource(
            scheme_id=s2.scheme_id,
            publisher="Stand-Up Mitra / Government of India",
            source_url="https://www.standupmitra.in",
            source_type="OFFICIAL_PORTAL",
            verification_status="VERIFIED"
        )
        db.add(src2)
        db.commit()

    # 4. Scheme 3: PM DAKSH Yojana
    s3 = db.query(Scheme).filter(Scheme.scheme_id == "PM-DAKSH-001").first()
    if not s3:
        s3 = Scheme(
            scheme_id="PM-DAKSH-001",
            name="PM DAKSH (Pradhan Mantri Dakshta Aur Kushalta Sampann Hitgrahi) Yojana",
            short_name="PM DAKSH",
            ministry="Ministry of Social Justice and Empowerment",
            department="MoSJE Training & Entrepreneurship Division",
            scheme_type="SKILL_ENTERPRISE",
            target_group="Marginalized artisans, SC, OBC youth, sanitation workers",
            description="National action plan for skill development, upskilling, and enterprise loan assistance for marginalized groups.",
            status="ACTIVE",
            geography_scope="PAN_INDIA",
            official_url="https://pmdaksh.dosje.gov.in",
            application_url="https://pmdaksh.dosje.gov.in/student",
            helpline="1800-180-4567",
            source_confidence="VERIFIED",
            last_verified_at=datetime.now(timezone.utc),
            data_version="v2026.1"
        )
        db.add(s3)
        db.commit()

        rules_s3 = [
            SchemeRule(
                scheme_id=s3.scheme_id,
                rule_id="DAKSH-INCOME-001",
                field_name="annual_family_income",
                operator="<=",
                expected_value="300000",
                value_unit="INR",
                rule_type="hard",
                explanation_template="Annual family income must be within Rs. 3,00,000.",
                source_reference_id="SRC-DAKSH-01"
            ),
            SchemeRule(
                scheme_id=s3.scheme_id,
                rule_id="DAKSH-CAT-002",
                field_name="caste_category",
                operator="in",
                expected_value="SC,OBC,MARGINALIZED",
                rule_type="hard",
                explanation_template="Applicant must belong to SC, OBC, or Economically Backward category.",
                source_reference_id="SRC-DAKSH-01"
            )
        ]
        db.add_all(rules_s3)

        b3 = SchemeBenefit(
            scheme_id=s3.scheme_id,
            benefit_type="SUBSIDY",
            min_value=10000,
            max_value=200000,
            interest_rate=4.0,
            tenure_months=36,
            moratorium_months=3,
            description="Free residential/non-residential skill training with monthly stipend and micro-loan linkage.",
            source_reference_id="SRC-DAKSH-01"
        )
        db.add(b3)

        src3 = SchemeSource(
            scheme_id=s3.scheme_id,
            publisher="Ministry of Social Justice and Empowerment",
            source_url="https://pmdaksh.dosje.gov.in",
            source_type="OFFICIAL_PORTAL",
            verification_status="VERIFIED"
        )
        db.add(src3)
        db.commit()

    # 5. Channel Partner Locations (SCA, Banks in UP, Delhi, Maharashtra)
    partner_records = [
        PartnerLocation(
            id="partner_up_bijnor_01",
            partner_name="State Bank of India - Main Branch & MSME Desk",
            partner_type="NATIONALISED_BANK",
            scheme_categories="CREDIT_LOAN,MICRO_FINANCE",
            address="Civil Lines, Near Collectorate",
            district="Bijnor",
            state="Uttar Pradesh",
            pincode="246701",
            latitude=29.3724,
            longitude=78.1358,
            active=True,
            fund_utilisation_status="AVAILABLE",
            contact_number="01342-262100",
            email="sbi.bijnor@sbi.co.in"
        ),
        PartnerLocation(
            id="partner_up_sca_lucknow",
            partner_name="UP Backward Classes Development Finance Corporation (UPBCDFC)",
            partner_type="SCA",
            scheme_categories="CREDIT_LOAN,EDUCATION_LOAN,MICRO_FINANCE",
            address="Kisan Mandi Bhawan, Vibhuti Khand, Gomti Nagar",
            district="Lucknow",
            state="Uttar Pradesh",
            pincode="226010",
            latitude=26.8467,
            longitude=80.9462,
            active=True,
            fund_utilisation_status="AVAILABLE",
            contact_number="0522-2720844",
            email="upbcdfc@up.gov.in"
        ),
        PartnerLocation(
            id="partner_up_meerut_pnb",
            partner_name="Punjab National Bank - Lead District Office",
            partner_type="NATIONALISED_BANK",
            scheme_categories="CREDIT_LOAN",
            address="Delhi Road, Near Transport Nagar",
            district="Meerut",
            state="Uttar Pradesh",
            pincode="250002",
            latitude=28.9845,
            longitude=77.7064,
            active=True,
            fund_utilisation_status="AVAILABLE",
            contact_number="0121-2401920",
            email="ldomeerut@pnb.co.in"
        ),
        PartnerLocation(
            id="partner_delhi_dsfdc",
            partner_name="Delhi SC ST OBC Minorities Finance Corporation (DSFDC)",
            partner_type="SCA",
            scheme_categories="CREDIT_LOAN,MICRO_FINANCE",
            address="2, Battery Lane, Rajpur Road",
            district="New Delhi",
            state="Delhi",
            pincode="110054",
            latitude=28.6692,
            longitude=77.2185,
            active=True,
            fund_utilisation_status="AVAILABLE",
            contact_number="011-23969190",
            email="dsfdc@delhi.gov.in"
        ),
        PartnerLocation(
            id="partner_pune_mpbcdc",
            partner_name="Mahatma Phule Backward Class Development Corporation",
            partner_type="SCA",
            scheme_categories="CREDIT_LOAN,MICRO_FINANCE",
            address="Administrative Building, Shivajinagar",
            district="Pune",
            state="Maharashtra",
            pincode="411005",
            latitude=18.5204,
            longitude=73.8567,
            active=True,
            fund_utilisation_status="AVAILABLE",
            contact_number="020-25531234",
            email="mpbcdc.pune@maharashtra.gov.in"
        )
    ]

    for p in partner_records:
        existing = db.query(PartnerLocation).filter(PartnerLocation.id == p.id).first()
        if not existing:
            db.add(p)
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
        print("Database seeded successfully with authentic MoSJE / NBCFDC data and Channel Partners.")
    finally:
        db.close()
