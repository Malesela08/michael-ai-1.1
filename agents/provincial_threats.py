# Provincial Threat Matrix & Specific Crime Vectors for Michael AI
# "Zero-Tolerance Intelligence Against Hijackings, Cable Theft & Infrastructure Sabotage"

def get_provincial_threat_level(province: str) -> dict:
    """
    Returns the risk tier, primary vector profiles, and high-priority enemy targets for a given South African province.
    """
    threat_data = {
        "Gauteng": {
            "risk_tier": "CRITICAL", 
            "primary_vectors": [
                "VEHICLE_HIJACKING", 
                "STOLEN_CARS", 
                "ARMED_ROBBERY", 
                "CABLE_THEFT", 
                "INFRASTRUCTURE_SABOTAGE",
                "FORCED_ENTRY"
            ]
        },
        "Western Cape": {
            "risk_tier": "HIGH", 
            "primary_vectors": ["ARMED_ROBBERY", "PERIMETER_BREACH", "VEHICLE_THEFT", "CABLE_THEFT"]
        },
        "KwaZulu-Natal": {
            "risk_tier": "CRITICAL", 
            "primary_vectors": ["VEHICLE_HIJACKING", "ARMED_ASSAULT", "HOME_INVASION", "INFRASTRUCTURE_SABOTAGE"]
        },
        "Eastern Cape": {
            "risk_tier": "MODERATE", 
            "primary_vectors": ["PROPERTY_THEFT", "CABLE_THEFT", "ARMED_ROBBERY"]
        },
        "Free State": {
            "risk_tier": "MODERATE", 
            "primary_vectors": ["INFRASTRUCTURE_SABOTAGE", "RURAL_INTRUSION", "VEHICLE_THEFT"]
        },
        "Mpumalanga": {
            "risk_tier": "MODERATE", 
            "primary_vectors": ["CABLE_THEFT", "VEHICLE_HIJACKING", "PERIMETER_BREACH"]
        },
        "Limpopo": {
            "risk_tier": "MODERATE", 
            "primary_vectors": ["VEHICLE_THEFT", "INFRASTRUCTURE_SABOTAGE", "PROPERTY_THEFT"]
        },
        "North West": {
            "risk_tier": "HIGH", 
            "primary_vectors": ["ARMED_ASSAULT", "VEHICLE_HIJACKING", "CABLE_THEFT"]
        },
        "Northern Cape": {
            "risk_tier": "LOW", 
            "primary_vectors": ["TRESPASSING", "INFRASTRUCTURE_SABOTAGE"]
        }
    }
    
    return threat_data.get(province, {"risk_tier": "UNKNOWN", "primary_vectors": ["GENERAL_INTRUSION"]})
