"""
Unit tests for the LLM Gateway mechanics.
"""
import pytest
from app.core.prompts import PromptRegistry
from app.services.telemetry import TelemetryLogger

def test_prompt_registry_retrieval():
    """Verify that required prompts are registered and versioned correctly."""
    prompts = PromptRegistry.list_all()
    names = [p["name"] for p in prompts]
    
    assert "jd_generation" in names
    assert "resume_parsing" in names
    assert "fit_score_evaluation" in names

    # Test retrieval
    jd_prompt = PromptRegistry.get("jd_generation", "v1")
    assert "{title}" in jd_prompt.user_template
    assert "{department}" in jd_prompt.user_template

def test_prompt_registry_missing():
    """Verify registry raises KeyError on missing prompts."""
    with pytest.raises(KeyError):
        PromptRegistry.get("does_not_exist")

def test_telemetry_logging():
    """Verify telemetry ring buffer correctly aggregates stats."""
    # Use a fresh logger for tests to avoid side effects
    telemetry = TelemetryLogger()
    
    # Simulate two calls via the event class
    from app.services.telemetry import LLMTelemetryEvent
    
    event1 = LLMTelemetryEvent(
        model="anthropic/claude-sonnet-4-20250514",
        prompt_name="test_prompt",
        total_tokens=1500,
        estimated_cost_usd=0.015,
        anonymization_applied=True,
        caller_service="test"
    )
    telemetry.log(event1)
    
    event2 = LLMTelemetryEvent(
        model="gemini/gemini-2.0-flash",
        prompt_name="test_prompt",
        total_tokens=500,
        estimated_cost_usd=0.001,
        anonymization_applied=False,
        caller_service="test"
    )
    telemetry.log(event2)
    
    stats = telemetry.get_stats()
    
    assert stats["total_calls"] == 2
    assert stats["total_tokens"] == 2000
    assert stats["total_cost_usd"] == 0.016
    assert stats["buffer_size"] == 2
    
    recent = telemetry.get_recent(n=1)
    assert len(recent) == 1
    assert recent[0]["model"] == "gemini/gemini-2.0-flash"

