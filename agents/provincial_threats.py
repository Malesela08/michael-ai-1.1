# Provincial Threat Intelligence Module for Michael AI

PROVINCIAL_THREAT_MATRIX = {
    "Gauteng": {
        "risk_level": "CRITICAL",
        "primary_vectors": ["Driveway Ambushes", "Signal Jamming", "Residential Home Invasions"],
        "peak_windows": ["06:00-09:00", "18:00-21:00"],
        "asset_focus": ["High-End Vehicles", "Residential Perimeters"]
    },
    "KwaZulu-Natal": {
        "risk_level": "CRITICAL",
        "primary_vectors": ["Armed Interceptions", "Courier Hijackings", "Arterial Ambushes"],
        "peak_windows": ["17:00-22:00"],
        "asset_focus": ["Fleet Vehicles", "Private Sedans"]
    },
    "Western Cape": {
        "risk_level": "HIGH",
        "primary_vectors": ["Highway Staged Breakdowns", "Parking Lot Jamming", "Perimeter Breaches"],
        "peak_windows": ["07:00-09:00", "19:00-23:00"],
        "asset_focus": ["Commercial Assets", "Residential Properties"]
    },
    "Mpumalanga": {
        "risk_level": "HIGH",
        "primary_vectors": ["Cross-Border Smuggling", "Transit Stop Ambushes"],
        "peak_windows": ["Night Operations"],
        "asset_focus": ["SUV/4x4 Vehicles", "Perimeter Security"]
    },
    "Limpopo": {
        "risk_level": "MEDIUM-HIGH",
        "primary_vectors": ["Border Corridor Trafficking", "Rural Perimeter Breaches"],
        "peak_windows": ["20:00-04:00"],
        "asset_focus": ["Stolen Fleet/Transit", "Farm/Rural Assets"]
    },
    "North West": {
        "risk_level": "MEDIUM-HIGH",
        "primary_vectors": ["Mining Hub Transit Theft", "Residential Gate Ambushes"],
        "peak_windows": ["05:00-08:00", "18:00-20:00"],
        "asset_focus": ["Utility Vehicles", "Suburban Homes"]
    },
    "Eastern Cape": {
        "risk_level": "HIGH",
        "primary_vectors": ["Delivery Vehicle Targeting", "Armed Residential Break-ins"],
        "peak_windows": ["16:00-20:00"],
        "asset_focus": ["Commercial Delivery", "Urban Residences"]
    },
    "Free State": {
        "risk_level": "MEDIUM",
        "primary_vectors": ["Agricultural Asset Theft", "Transit Corridor Interceptions"],
        "peak_windows": ["Night Operations"],
        "asset_focus": ["Farm Infrastructure", "Long-Distance Transit"]
    },
    "Northern Cape": {
        "risk_level": "MODERATE",
        "primary_vectors": ["Remote Solar/Infrastructure Theft", "Unmonitored Perimeters"],
        "peak_windows": ["Unmonitored Hours"],
        "asset_focus": ["Solar Arrays", "Remote Outposts"]
    }
}

def get_province_threat_profile(province_name: str):
    """Retrieves threat intelligence parameters for a specific South African province."""
    return PROVINCIAL_THREAT_MATRIX.get(province_name, {"risk_level": "UNKNOWN", "primary_vectors": [], "peak_windows": []})
