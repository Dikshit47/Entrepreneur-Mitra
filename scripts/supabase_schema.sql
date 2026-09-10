-- ==========================================================
-- Entrepreneur Mitra (SIH26092) - Supabase PostgreSQL Schema
-- Generated via SQLAlchemy 2.0 Declarative Models
-- ==========================================================

CREATE TABLE audit_logs (
	id VARCHAR(36) NOT NULL, 
	user_id VARCHAR(36), 
	actor_type VARCHAR(30), 
	action VARCHAR(60) NOT NULL, 
	entity_type VARCHAR(50) NOT NULL, 
	entity_id VARCHAR(50) NOT NULL, 
	metadata_json TEXT, 
	timestamp TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE TABLE eligibility_evaluations (
	id VARCHAR(36) NOT NULL, 
	profile_id VARCHAR(36) NOT NULL, 
	scheme_id VARCHAR(50) NOT NULL, 
	decision VARCHAR(30) NOT NULL, 
	rule_trace_json TEXT NOT NULL, 
	engine_version VARCHAR(20), 
	evaluated_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE TABLE partner_locations (
	id VARCHAR(36) NOT NULL, 
	partner_name VARCHAR(150) NOT NULL, 
	partner_type VARCHAR(50), 
	scheme_categories VARCHAR(200), 
	address VARCHAR(255) NOT NULL, 
	district VARCHAR(60) NOT NULL, 
	state VARCHAR(60) NOT NULL, 
	pincode VARCHAR(10), 
	latitude FLOAT NOT NULL, 
	longitude FLOAT NOT NULL, 
	active BOOLEAN, 
	fund_utilisation_status VARCHAR(30), 
	contact_number VARCHAR(50), 
	email VARCHAR(100), 
	last_verified_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE TABLE schemes (
	scheme_id VARCHAR(50) NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	short_name VARCHAR(50), 
	ministry VARCHAR(150) NOT NULL, 
	department VARCHAR(150), 
	scheme_type VARCHAR(50), 
	target_group VARCHAR(255), 
	description TEXT NOT NULL, 
	status VARCHAR(20), 
	geography_scope VARCHAR(50), 
	official_url VARCHAR(300) NOT NULL, 
	application_url VARCHAR(300) NOT NULL, 
	helpline VARCHAR(100), 
	source_confidence VARCHAR(20), 
	last_verified_at TIMESTAMP WITHOUT TIME ZONE, 
	data_version VARCHAR(20), 
	effective_from TIMESTAMP WITHOUT TIME ZONE, 
	effective_to TIMESTAMP WITHOUT TIME ZONE, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	updated_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (scheme_id)
);

CREATE TABLE users (
	id VARCHAR(36) NOT NULL, 
	auth_provider_id VARCHAR(100), 
	phone VARCHAR(20), 
	email VARCHAR(120), 
	hashed_password VARCHAR(255), 
	preferred_language VARCHAR(10), 
	role VARCHAR(20), 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	updated_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE TABLE alerts (
	id VARCHAR(36) NOT NULL, 
	user_id VARCHAR(36) NOT NULL, 
	scheme_id VARCHAR(50), 
	alert_type VARCHAR(50), 
	title VARCHAR(150) NOT NULL, 
	message TEXT NOT NULL, 
	payload_json TEXT, 
	read_at TIMESTAMP WITHOUT TIME ZONE, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(scheme_id) REFERENCES schemes (scheme_id)
);

CREATE TABLE applications (
	id VARCHAR(36) NOT NULL, 
	user_id VARCHAR(36) NOT NULL, 
	scheme_id VARCHAR(50) NOT NULL, 
	selected_partner_id VARCHAR(36), 
	status VARCHAR(40), 
	copilot_step INTEGER, 
	notes TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	updated_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(scheme_id) REFERENCES schemes (scheme_id), 
	FOREIGN KEY(selected_partner_id) REFERENCES partner_locations (id)
);

CREATE TABLE document_requirements (
	id VARCHAR(36) NOT NULL, 
	scheme_id VARCHAR(50) NOT NULL, 
	document_type VARCHAR(60) NOT NULL, 
	mandatory BOOLEAN, 
	acceptable_variants VARCHAR(255), 
	verification_level VARCHAR(30), 
	source_reference_id VARCHAR(50), 
	PRIMARY KEY (id), 
	FOREIGN KEY(scheme_id) REFERENCES schemes (scheme_id)
);

CREATE TABLE entrepreneur_profiles (
	id VARCHAR(36) NOT NULL, 
	user_id VARCHAR(36), 
	profile_version INTEGER, 
	status VARCHAR(20), 
	preferred_language VARCHAR(10), 
	confirmed_at TIMESTAMP WITHOUT TIME ZONE, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	updated_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE saved_schemes (
	id VARCHAR(36) NOT NULL, 
	user_id VARCHAR(36) NOT NULL, 
	scheme_id VARCHAR(50) NOT NULL, 
	saved_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_user_scheme_saved UNIQUE (user_id, scheme_id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(scheme_id) REFERENCES schemes (scheme_id)
);

CREATE TABLE scheme_benefits (
	id VARCHAR(36) NOT NULL, 
	scheme_id VARCHAR(50) NOT NULL, 
	benefit_type VARCHAR(50), 
	min_value FLOAT, 
	max_value FLOAT, 
	percentage FLOAT, 
	interest_rate FLOAT, 
	tenure_months INTEGER, 
	moratorium_months INTEGER, 
	description TEXT NOT NULL, 
	source_reference_id VARCHAR(50), 
	PRIMARY KEY (id), 
	FOREIGN KEY(scheme_id) REFERENCES schemes (scheme_id)
);

CREATE TABLE scheme_rules (
	id VARCHAR(36) NOT NULL, 
	scheme_id VARCHAR(50) NOT NULL, 
	rule_id VARCHAR(50) NOT NULL, 
	field_name VARCHAR(60) NOT NULL, 
	operator VARCHAR(20) NOT NULL, 
	expected_value VARCHAR(255) NOT NULL, 
	value_unit VARCHAR(30), 
	condition_group VARCHAR(30), 
	rule_type VARCHAR(20), 
	explanation_template TEXT NOT NULL, 
	source_reference_id VARCHAR(50), 
	version INTEGER, 
	effective_from TIMESTAMP WITHOUT TIME ZONE, 
	effective_to TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(scheme_id) REFERENCES schemes (scheme_id)
);

CREATE TABLE scheme_sources (
	id VARCHAR(36) NOT NULL, 
	scheme_id VARCHAR(50) NOT NULL, 
	publisher VARCHAR(150) NOT NULL, 
	source_url VARCHAR(300) NOT NULL, 
	source_type VARCHAR(50), 
	retrieved_at TIMESTAMP WITHOUT TIME ZONE, 
	verified_at TIMESTAMP WITHOUT TIME ZONE, 
	content_hash VARCHAR(64), 
	verification_status VARCHAR(30), 
	PRIMARY KEY (id), 
	FOREIGN KEY(scheme_id) REFERENCES schemes (scheme_id)
);

CREATE TABLE user_documents (
	id VARCHAR(36) NOT NULL, 
	user_id VARCHAR(36), 
	document_type VARCHAR(60) NOT NULL, 
	original_filename VARCHAR(255) NOT NULL, 
	storage_key VARCHAR(255) NOT NULL, 
	mime_type VARCHAR(100) NOT NULL, 
	file_size_bytes INTEGER, 
	checksum VARCHAR(64) NOT NULL, 
	ocr_status VARCHAR(30), 
	document_status VARCHAR(30), 
	verification_status VARCHAR(40), 
	source VARCHAR(40), 
	verification_method VARCHAR(60), 
	issuer VARCHAR(150), 
	issued_date VARCHAR(50), 
	expiry_date VARCHAR(50), 
	verified_at TIMESTAMP WITHOUT TIME ZONE, 
	verification_reference VARCHAR(100), 
	is_sandbox BOOLEAN, 
	extracted_data_json TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	updated_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE profile_attributes (
	id VARCHAR(36) NOT NULL, 
	profile_id VARCHAR(36) NOT NULL, 
	attribute_key VARCHAR(60) NOT NULL, 
	attribute_value VARCHAR(255) NOT NULL, 
	data_type VARCHAR(20), 
	source VARCHAR(30), 
	confidence FLOAT, 
	user_confirmed BOOLEAN, 
	created_at TIMESTAMP WITHOUT TIME ZONE, 
	updated_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES entrepreneur_profiles (id)
);
