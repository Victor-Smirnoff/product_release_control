from typing import Annotated
from fastapi import APIRouter, Path, Depends, Query
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


@router.get("/shift_task")
async def get_shift_task_by_several_params(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100),
    closing_status: bool = Query(None),
    party_number: int = Query(None),
    party_data: datetime.date = Query(None),
    shift: str = Query(None, min_length=1, max_length=100),
    team: str = Query(None, min_length=1, max_length=100),
    nomenclature: str = Query(None, min_length=1, max_length=100),
    code_ekn: str = Query(None, min_length=1, max_length=100),
    id_of_the_rc: str = Query(None, min_length=1, max_length=100),
    date_time_shift_start: datetime.datetime = Query(None),
    date_time_shift_end: datetime.datetime = Query(None),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    several_params = {}
    #  тоже немного хардкодинга
    if closing_status is not None:
        several_params["closing_status"] = closing_status
    if party_number is not None:
        several_params["party_number"] = party_number
    if party_data is not None:
        several_params["party_data"] = party_data
    if shift is not None:
        several_params["shift"] = shift
    if team is not None:
        several_params["team"] = team
    if nomenclature is not None:
        several_params["nomenclature"] = nomenclature
    if code_ekn is not None:
        several_params["code_ekn"] = code_ekn
    if id_of_the_rc is not None:
        several_params["id_of_the_rc"] = id_of_the_rc
    if date_time_shift_start is not None:
        several_params["date_time_shift_start"] = date_time_shift_start
    if date_time_shift_end is not None:
        several_params["date_time_shift_end"] = date_time_shift_end

    response = await dao_obj.find_by_several_params(
        session=session,
        several_params=several_params
    )

    if isinstance(response, list):
        task_list_to_return = []
        for task in response:
            shift_task = dto_obj.get_shift_task_dto(task)
            task_list_to_return.append(shift_task)

        start = offset
        end = offset + limit
        return task_list_to_return[start:end]
    else:
        raise ShiftTaskException(
            message=response.message,
            status_code=response.code
        )
