from fastapi.routing import APIRouter
from fastapi import Depends, Request

from src.app.schemas.process import ProcessCreateData, ProcessEditData, EntityData, ToDeleteData
from src.app.services.process import ProcessService
from src.app.db.engine import get_session


router = APIRouter()

async def get_process_service(session=Depends(get_session, scope='function')) -> ProcessService:
    return ProcessService(session)

@router.get('/')
async def get_processes(request: Request,
                        service: ProcessService = Depends(get_process_service)):
    user_id = request.cookies.get('grafinya_session')
    pr_list = []
    if user_id:
        pr_list = await service.get_all(user_id)

    return {
        'processes': pr_list
    }

@router.post('/create')
async def create_process(request: Request,
                         proc_data: ProcessCreateData,
                         service: ProcessService = Depends(get_process_service)):
    user_id = request.cookies.get('grafinya_session')
    if user_id:
        await service.create(user_id, proc_data.name)


@router.post('/rename')
async def edit_process(proc_data: ProcessEditData,
                       service: ProcessService = Depends(get_process_service)):
    await service.rename(proc_data.pr_id, proc_data.new_name)

@router.post('/delete')
async def delete_process(proc_data: ProcessEditData,
                         service: ProcessService = Depends(get_process_service)):
    await service.delete(proc_data.pr_id)

@router.get('/entities/')
async def get_entities(entity_data: EntityData,
                       service: ProcessService = Depends(get_process_service)):
    await service.update_entity(
        entity_data.proc_id,
        entity_data.entity_id,
        entity_data.name,
        entity_data.tag
    )

@router.post('/entities/update')
async def update_entity(entity_data: EntityData,
                        service: ProcessService = Depends(get_process_service)):
    await service.update_entity(
        entity_data.proc_id,
        entity_data.entity_id,
        entity_data.name,
        entity_data.tag
    )

@router.post('/entities/delete')
async def delete_entity(to_delete: ToDeleteData,
                        service: ProcessService = Depends(get_process_service)):
    await service.delete_entity(to_delete.id)
