from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

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
