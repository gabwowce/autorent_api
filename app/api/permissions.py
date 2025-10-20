# app/core/permissions.py
from enum import Enum
from fastapi import Depends, HTTPException
from app.api.deps import get_current_user

class Perm(str, Enum):
    VIEW = "view"
    EDIT = "edit"
    ADMIN = "admin"

ROLE_PERMS = {
    "Guest": {Perm.VIEW},
    "Emplo": {Perm.VIEW, Perm.EDIT},   # jei nori – pervadink į "Employee"
    "Admin": {Perm.VIEW, Perm.EDIT, Perm.ADMIN},
}

def require_perm(perm: Perm):
    def dep(user = Depends(get_current_user)):
        role = getattr(user, "role", None) or getattr(user, "pareigos", None)
        if perm not in ROLE_PERMS.get(role, set()):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return dep
