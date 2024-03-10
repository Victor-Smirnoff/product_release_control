from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from dto import ErrorResponse
from model.models import ShiftTask


class DaoShiftTaskRepository:
    """
    Класс для выполнения основных операций в БД над таблицей ShiftTask
    """

    @staticmethod
    async def find_all(session: AsyncSession) -> list[ShiftTask] | ErrorResponse:
        """
        Метод возвращает список объектов класса ShiftTask или объект ошибки ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :return: list[ShiftTask] или ErrorResponse
        """
        try:
            stmt = select(ShiftTask).order_by(ShiftTask.id)
            result: Result = await session.execute(stmt)
            list_all_shift_tasks = result.scalars().all()
            return list(list_all_shift_tasks)
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    @staticmethod
    async def find_by_id(session: AsyncSession, shift_task_id: int) -> ShiftTask | ErrorResponse:
        """
        Метод возвращает найденный объект класса ShiftTask если он найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param shift_task_id: айди сменного задания
        :return: объект класса ShiftTask или ErrorResponse
        """
        try:
            shift_task = await session.get(ShiftTask, shift_task_id)
            if isinstance(shift_task, ShiftTask):
                return shift_task
            else:
                response = ErrorResponse(code=404, message=f"Сменное задание с id {shift_task_id} не найдено")
                return response
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    async def update_shift_task(self,
                                session: AsyncSession,
                                shift_task_id: int,
                                update_data: dict
                                ) -> ShiftTask | ErrorResponse:
        """
        Метод изменяет существующий объект класса ShiftTask.
        Возвращает объект класса ShiftTask если он найден в БД и успешно изменен, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param shift_task_id: айди сменного задания
        :param update_data: словарь с полями для изменения
        :return: объект класса ShiftTask или ErrorResponse
        """

        shift_task = await self.find_by_id(session=session, shift_task_id=shift_task_id)

        if isinstance(shift_task, ShiftTask):
            if "closing_status" in update_data:
                if shift_task.closing_status is False and update_data["closing_status"] is True:
                    shift_task.closed_at = datetime.datetime.now()
                if shift_task.closing_status is True and update_data["closing_status"] is False:
                    shift_task.closed_at = None
                shift_task.closing_status = update_data["closing_status"]

            shift_task.view_task_to_shift = update_data["view_task_to_shift"] if "view_task_to_shift" in update_data \
                else shift_task.view_task_to_shift

            shift_task.work_center = update_data["work_center"] if "work_center" in update_data \
                else shift_task.work_center

            shift_task.line = update_data["line"] if "line" in update_data else shift_task.line
            shift_task.shift = update_data["shift"] if "shift" in update_data else shift_task.shift
            shift_task.team = update_data["team"] if "team" in update_data else shift_task.team
            shift_task.party_number = update_data["party_number"] if "party_number" in update_data \
                else shift_task.party_number
            shift_task.party_data = update_data["party_data"] if "party_data" in update_data \
                else shift_task.party_data
            shift_task.nomenclature = update_data["nomenclature"] if "nomenclature" in update_data \
                else shift_task.nomenclature
            shift_task.code_ekn = update_data["code_ekn"] if "code_ekn" in update_data else shift_task.code_ekn
            shift_task.id_of_the_rc = update_data["id_of_the_rc"] if "id_of_the_rc" in update_data \
                else shift_task.id_of_the_rc

            shift_task.date_time_shift_start = update_data["date_time_shift_start"] if ("date_time_shift_start"
                in update_data) else shift_task.date_time_shift_start

            shift_task.date_time_shift_end = update_data["date_time_shift_end"] if ("date_time_shift_end"
                in update_data) else shift_task.date_time_shift_end

            session.add(shift_task)
            await session.commit()
            return shift_task

        else:
            response = ErrorResponse(code=404, message=f"Сменное задание с id {shift_task_id} не найдено")
            return response
