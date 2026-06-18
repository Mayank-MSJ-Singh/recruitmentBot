# Data Residency & Security Baseline (India Region)

This document establishes the architecture baseline for compliance with the **Digital Personal Data Protection Act, 2023 (DPDP Act, India)** and related enterprise security protocols for RecruitBot.

---

## 1. Data Residency (India Only)

To comply with local enterprise policy and the DPDP Act guidelines:
*   **Infrastructure Hosting:** All servers (FastAPI backend, Redis async queues) must be provisioned strictly within AWS India Regions (e.g., `ap-south-1` - Mumbai) or GCP India Regions (e.g., `asia-south1` - Mumbai).
*   **Data Tier Hosting:** The PostgreSQL database running `pgvector` must reside strictly in an India region RDS instance. No candidate profile, resume text, or vector representations may exit the boundary of the Indian territory.
*   **Third-Party AI Gateways (PII Stripping):** 
    *   Before sending any candidate text (resumes, video transcripts) to external foundation model APIs (e.g., Anthropic Claude, Voyage AI), the backend’s **AI Firewall** must parse and strip direct PII (Names, Phone Numbers, Exact Email Addresses).
    *   Only anonymized semantic content is processed externally.

---

## 2. Consent Management Architecture (DPDP Compliance)

Sprint 0.2 introduces a dedicated `consent` audit log table. The backend must enforce the following rules:
1.  **Affirmative Consent:** Candidates must actively toggle consent prior to resume upload/AI interview processes.
2.  **Consent Schema:**
    *   `consent_id`: UUID
    *   `candidate_id`: UUID (Foreign Key)
    *   `consent_type`: Enum (`sourcing_matching`, `ai_interviewing`, `onboarding`)
    *   `status`: Boolean (`granted`, `revoked`)
    *   `timestamp`: UTC DateTime
3.  **Right to Erase:** Upon consent revocation (`status = revoked`), an asynchronous background job must purge all candidate PII (resume documents, transcribed text) from active tables and Object Storage. Only anonymized, aggregated matching metrics may remain for analytics.

---

## 3. Data Minimization & Encryption

*   **Encryption in Transit:** All traffic flowing between the client and API Gateway, and between services internally, is secured with TLS 1.3.
*   **Encryption at Rest:** Standard AES-256 block-level encryption is enforced on the RDS volumes, S3 buckets storing resume files, and all audit logs.
*   **Decoupled PII:** Resumes and sensitive identification documents are stored in private bucket subfolders. Temporary signed URLs are generated on-demand with a maximum expiration window of 15 minutes.
