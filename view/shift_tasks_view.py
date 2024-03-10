from typing import Annotated
from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
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


@router.put("/shift_task/{shift_task_id}")
async def update_shift_task_by_id(
    shift_task_id: Annotated[int, Path()],
    update_data: dict,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    response = await dao_obj.update_shift_task(session=session, shift_task_id=shift_task_id, update_data=update_data)
    if isinstance(response, ShiftTask):
        shift_task = dto_obj.get_shift_task_dto(response)
        return shift_task
    else:
        raise ShiftTaskException(
            message=response.message,
            status_code=response.code
        )

@router.post("/shift_task", status_code=201)
async def add_shift_task(
    shift_task_list: list[dict],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    task_list_to_return = []
    for task in shift_task_list:
        response = await dao_obj.create_shift_task(
            session=session,
            closing_status=task["СтатусЗакрытия"],
            view_task_to_shift=task["ПредставлениеЗаданияНаСмену"],
            line=task["Линия"],
            shift=task["Смена"],
            team=task["Бригада"],
            party_number=task["НомерПартии"],
            party_data=datetime.datetime.strptime(task["ДатаПартии"], "%Y-%m-%d").date(),
            nomenclature=task["Номенклатура"],
            code_ekn=task["КодЕКН"],
            id_of_the_rc=task["ИдентификаторРЦ"],
            date_time_shift_start=datetime.datetime.fromisoformat(
                task["ДатаВремяНачалаСмены"]).replace(tzinfo=None),
            date_time_shift_end=datetime.datetime.fromisoformat(
                task["ДатаВремяОкончанияСмены"]).replace(tzinfo=None),
        )

        if isinstance(response, ShiftTask):
            shift_task = dto_obj.get_shift_task_dto(response)
            task_list_to_return.append(shift_task)
        else:
            raise ShiftTaskException(
                message=response.message,
                status_code=response.code
            )

    return task_list_to_return
