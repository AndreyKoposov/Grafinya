from fastapi import APIRouter
from . import auth, processes


router = APIRouter()

router.include_router(
    auth.router,
    prefix='/auth',
    tags=['authentication'],
)
router.include_router(
    processes.router,
    prefix='/processes',
    tags=['processes']
)
