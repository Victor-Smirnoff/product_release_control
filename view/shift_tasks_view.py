from typing import Annotated
from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dao import DaoShiftTaskRepository
from exception import ShiftTaskException
from model import db_helper
from model import ShiftTask


router = APIRouter(tags=["shift_tasks"])
dao_obj = DaoShiftTaskRepository()



@router.get("/shift_task/{shift_task_id}")
async def get_shift_task_by_id(
        code: Annotated[str, Path(max_length=3)],
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.find_by_id(session=session, code=code)
    if isinstance(response, ShiftTask):
        currency = dao_obj.get_currency_dto(response)
        return currency
    else:
        raise ShiftTaskException(
            message=response.message,
            status_code=response.code
        )
