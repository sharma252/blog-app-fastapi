from fastapi import APIRouter, Depends
from .deps import get_current_user
from ..schemas import UserOut
from ..models import User

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
