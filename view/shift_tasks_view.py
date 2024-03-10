from typing import Annotated
from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dao import DaoShiftTaskRepository
from exception import ShiftTaskException
from model import db_helper
from model import ShiftTask
from service import ShiftTaskDtoService


router = APIRouter(tags=["shift_tasks"])
dao_obj = DaoShiftTaskRepository()
dto_obj = ShiftTaskDtoService()


@router.get("/shift_task/{shift_task_id}")
async def get_shift_task_by_id(
        shift_task_id: Annotated[int, Path()],
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.find_by_id(session=session, shift_task_id=shift_task_id)
    if isinstance(response, ShiftTask):
        shift_task = dto_obj.get_shift_task_dto(response)
        return shift_task
    else:
        raise ShiftTaskException(
            message=response.message,
            status_code=response.code
        )
