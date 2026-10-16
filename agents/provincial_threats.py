# Provincial Threat Matrix for Michael AI
# "Regional Intelligence & Risk Assessment Across South Africa"

def get_provincial_threat_level(province: str) -> dict:
    """
    Returns the risk tier and telemetry profile for a given South African province.
    """
    threat_data = {
        "Gauteng": {"risk_tier": "CRITICAL", "primary_vectors": ["Forced Entry", "Vehicle Hijacking", "Perimeter Breach"]},
        "Western Cape": {"risk_tier": "HIGH", "primary_vectors": ["Perimeter Breach", "Burglary"]},
        "KwaZulu-Natal": {"risk_tier": "CRITICAL", "primary_vectors": ["Armed Assault", "Home Invasion"]},
        "Eastern Cape": {"risk_tier": "MODERATE", "primary_vectors": ["Property Theft"]},
        "Free State": {"risk_tier": "MODERATE", "primary_vectors": ["Rural Intrusion"]},
        "Mpumalanga": {"risk_tier": "MODERATE", "primary_vectors": ["Perimeter Breach"]},
        "Limpopo": {"risk_tier": "MODERATE", "primary_vectors": ["Property Theft"]},
        "North West": {"risk_tier": "HIGH", "primary_vectors": ["Armed Assault", "Vehicle Theft"]},
        "Northern Cape": {"risk_tier": "LOW", "primary_vectors": ["Trespassing"]}
    }
    
    return threat_data.get(province, {"risk_tier": "UNKNOWN", "primary_vectors": ["General Intrusion"]})
