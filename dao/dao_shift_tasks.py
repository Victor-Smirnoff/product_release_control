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
                                **kwargs
                                ) -> ShiftTask | ErrorResponse:
        """
        Метод изменяет существующий объект класса ShiftTask.
        Возвращает объект класса ShiftTask если он найден в БД и успешно изменен, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param shift_task_id: айди сменного задания
        :param kwargs: аргументы для изменения
        :return: объект класса ShiftTask или ErrorResponse
        """

        shift_task = self.find_by_id(session=session, shift_task_id=shift_task_id)

        if isinstance(shift_task, ShiftTask):
            if "closing_status" in kwargs:
                if shift_task.closing_status is False and kwargs["closing_status"] is True:
                    shift_task.closed_at = datetime.datetime.now()
                if shift_task.closing_status is True and kwargs["closing_status"] is False:
                    shift_task.closed_at = None
                shift_task.closing_status = kwargs["closing_status"]

            shift_task.view_task_to_shift = kwargs["view_task_to_shift"] if "view_task_to_shift" in kwargs \
                else shift_task.view_task_to_shift

            shift_task.work_center = kwargs["work_center"] if "work_center" in kwargs \
                else shift_task.work_center

            shift_task.line = kwargs["line"] if "line" in kwargs else shift_task.line
            shift_task.shift = kwargs["shift"] if "shift" in kwargs else shift_task.shift
            shift_task.team = kwargs["team"] if "team" in kwargs else shift_task.team
            shift_task.party_number = kwargs["party_number"] if "party_number" in kwargs else shift_task.party_number
            shift_task.party_data = kwargs["party_data"] if "party_data" in kwargs else shift_task.party_data
            shift_task.nomenclature = kwargs["nomenclature"] if "nomenclature" in kwargs else shift_task.nomenclature
            shift_task.code_ekn = kwargs["code_ekn"] if "code_ekn" in kwargs else shift_task.code_ekn
            shift_task.id_of_the_rc = kwargs["id_of_the_rc"] if "id_of_the_rc" in kwargs else shift_task.id_of_the_rc

            shift_task.date_time_shift_start = kwargs["date_time_shift_start"] if "date_time_shift_start" in kwargs \
                else shift_task.date_time_shift_start

            shift_task.date_time_shift_end = kwargs["date_time_shift_end"] if "date_time_shift_end" in kwargs \
                else shift_task.date_time_shift_end

            session.add(shift_task)
            await session.commit()
            return shift_task

        else:
            response = ErrorResponse(code=404, message=f"Сменное задание с id {shift_task_id} не найдено")
            return response
