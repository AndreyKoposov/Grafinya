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
async def get_processes(request: Request,
                  service: ProcessService = Depends(get_process_service)):
    user_id = request.cookies.get('grafinya_session')
    pr_list = []
    if user_id:
        for pr in await service.get_all(user_id):
            pr_list.append({
                'id': pr.id,
                'name': pr.name,
                'avatar': pr.name[0],
                'created': pr.created_at.strftime("%Y-%m-%d"),
                'option': 0,
                'count': 2
            })

    return {
        'processes': pr_list
    }

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
