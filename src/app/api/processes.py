from fastapi.routing import APIRouter
from fastapi import Depends, Request

from src.app.schemas.process import ProcessData
from src.app.services.process import ProcessService
from src.app.repositories.process import ProcessRepo
from src.app.db.engine import get_session


router = APIRouter()

async def get_process_service(session=Depends(get_session, scope='function')) -> ProcessService:
    user_repo = ProcessRepo(session)
    return ProcessService(user_repo)

@router.get('/')
def get_processes():
    pass

@router.get('/id')
def get_process():
    pass

@router.post('/create')
async def create_process(request: Request,
                   proc_data: ProcessData,
                   service: ProcessService = Depends(get_process_service)):
    user_id = request.cookies.get('grafinya_session')
    if user_id:
        await service.create(user_id, proc_data.name)


@router.post('/edit')
def edit_process():
    pass

@router.get('/delete')
def delete_process():
    pass
