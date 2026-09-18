class Theme:
    # Color palette (Modern minimal)
    PRIMARY = "#1f538d"
    PRIMARY_HOVER = "#14375e"
    
    BG_COLOR = "#f0f2f5"       # Light theme bg
    BG_DARK = "#242424"        # Dark theme bg
    
    CARD_BG_LIGHT = "#ffffff"
    CARD_BG_DARK = "#2b2b2b"
    
    TEXT_LIGHT = "#000000"
    TEXT_DARK = "#ffffff"
    
    # Semantic Colors
    SUCCESS = "#2ecc71"
    WARNING = "#f39c12"
    DANGER = "#e74c3c"
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    HEADER_FONT = (FONT_FAMILY, 24, "bold")
    TITLE_FONT = (FONT_FAMILY, 18, "bold")
    NORMAL_FONT = (FONT_FAMILY, 14)
    SMALL_FONT = (FONT_FAMILY, 12)

def get_risk_color(risk_level: str) -> str:
    level = risk_level.strip().upper()
    if level == "LOW":
        return Theme.SUCCESS
    elif level == "MEDIUM":
        return Theme.WARNING
    elif level == "HIGH":
        return Theme.DANGER
    return Theme.PRIMARY
