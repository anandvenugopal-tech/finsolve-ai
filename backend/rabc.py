ROLE_PERMISSIONS = {
    "finance":     ["finance", "general"],
    "marketing":   ["marketing", "general"],
    "hr":          ["hr", "general"],
    "engineering": ["engineering", "general"],
    "c_level":     ["finance", "marketing", "hr", "engineering", "general"],
    "employee":    ["general"],
}

def get_allowed_permissions(role: str) -> list[str]:
    return ROLE_PERMISSIONS.get(role, ['general'])