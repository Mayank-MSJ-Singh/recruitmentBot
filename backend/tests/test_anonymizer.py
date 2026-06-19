"""
Unit tests for the PII Anonymizer (AI Firewall).
"""
from app.services.anonymizer import Anonymizer

def test_anonymize_indian_phone_number():
    text = "My phone number is +91 9876543210 and also 09876543210."
    redacted_text, counts = Anonymizer.anonymize(text)
    
    assert "+91 9876543210" not in redacted_text
    assert "09876543210" not in redacted_text
    assert "[PHONE_REDACTED]" in redacted_text
    assert counts["phone_indian"] == 2

def test_anonymize_emails():
    text = "Contact me at candidate.name@gmail.com or support@company.co.in."
    redacted_text, counts = Anonymizer.anonymize(text)
    
    assert "candidate.name@gmail.com" not in redacted_text
    assert "support@company.co.in" not in redacted_text
    assert "[EMAIL_REDACTED]" in redacted_text
    assert counts["email"] == 2

def test_anonymize_aadhaar_pan():
    text = "My Aadhaar is 1234 5678 9012 and PAN is ABCDE1234F."
    redacted_text, counts = Anonymizer.anonymize(text)
    
    assert "1234 5678 9012" not in redacted_text
    assert "ABCDE1234F" not in redacted_text
    assert "[AADHAAR_REDACTED]" in redacted_text
    assert "[PAN_REDACTED]" in redacted_text
    assert counts["aadhaar"] == 1
    assert counts["pan"] == 1

def test_clean_text_no_redaction():
    text = "I am a software engineer with 5 years of experience in Python and AWS."
    redacted_text, counts = Anonymizer.anonymize(text)
    
    assert redacted_text == text
    assert len(counts) == 0

