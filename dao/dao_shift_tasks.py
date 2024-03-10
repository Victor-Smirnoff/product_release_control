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
            list_all_currencies = result.scalars().all()
            return list(list_all_currencies)
        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response
