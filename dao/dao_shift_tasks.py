from sqlalchemy import Result, select, and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
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

    async def update_shift_task(
        self,
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

            shift_task.date_time_shift_start = update_data["date_time_shift_start"] \
                if ("date_time_shift_start" in update_data) else shift_task.date_time_shift_start

            shift_task.date_time_shift_end = update_data["date_time_shift_end"] \
                if ("date_time_shift_end" in update_data) else shift_task.date_time_shift_end

            session.add(shift_task)
            await session.commit()
            return shift_task

        else:
            response = ErrorResponse(code=404, message=f"Сменное задание с id {shift_task_id} не найдено")
            return response

    @staticmethod
    async def find_by_party_number_and_party_data(
        session: AsyncSession,
        party_number: int,
        party_data: datetime.date
    ) -> ShiftTask | ErrorResponse:
        """
        Метод находит объект класса ShiftTask по двум параметрам: НомерПартии и ДатаПартии.
        Возвращает объект класса ShiftTask если он найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param party_number: НомерПартии
        :param party_data: ДатаПартии
        :return: объект класса ShiftTask или ErrorResponse
        """
        try:
            stmt = select(ShiftTask).where(and_(
                ShiftTask.party_number == party_number,
                ShiftTask.party_data == party_data
            ))

            result: Result = await session.execute(stmt)
            if isinstance(result, Result):
                shift_task = result.scalar()
                if isinstance(shift_task, ShiftTask):
                    return shift_task
                else:
                    response = ErrorResponse(
                        code=404,
                        message=f"Сменное задание НомерПартии {party_number} и ДатаПартии {party_data} не найдено"
                    )
                    return response

        except SQLAlchemyError:
            response = ErrorResponse(code=500, message=f"База данных недоступна")
            return response

    async def create_shift_task(
        self,
        session: AsyncSession,
        closing_status: bool,
        view_task_to_shift: str,
        line: str,
        shift: str,
        team: str,
        party_number: int,
        party_data: datetime.date,
        nomenclature: str,
        code_ekn: str,
        id_of_the_rc: str,
        date_time_shift_start: datetime.datetime,
        date_time_shift_end: datetime.datetime,
    ) -> ShiftTask | ErrorResponse:
        """
        Метод записывает новое сменное задание в БД
        :param session: объект асинхронной сессии AsyncSession
        :param closing_status: СтатусЗакрытия
        :param view_task_to_shift: ПредставлениеЗаданияНаСмену
        :param line: Линия
        :param shift: Смена
        :param team: Бригада
        :param party_number: НомерПартии
        :param party_data: ДатаПартии
        :param nomenclature: Номенклатура
        :param code_ekn: КодЕКН
        :param id_of_the_rc: ИдентификаторРЦ
        :param date_time_shift_start: ДатаВремяНачалаСмены
        :param date_time_shift_end: ДатаВремяОкончанияСмены
        :return: объект класса ShiftTask | ErrorResponse
        """

        shift_task = await self.find_by_party_number_and_party_data(
            session=session,
            party_number=party_number,
            party_data=party_data,
        )

        if isinstance(shift_task, ShiftTask):
            update_data = {
                "СтатусЗакрытия": closing_status,
                "ПредставлениеЗаданияНаСмену": view_task_to_shift,
                "Линия": line,
                "Смена": shift,
                "Бригада": team,
                "НомерПартии": party_number,
                "ДатаПартии": party_data,
                "Номенклатура": nomenclature,
                "КодЕКН": code_ekn,
                "ИдентификаторРЦ": id_of_the_rc,
                "ДатаВремяНачалаСмены": date_time_shift_start,
                "ДатаВремяОкончанияСмены": date_time_shift_end,
            }

            shift_task_to_return = await self.update_shift_task(
                session=session,
                shift_task_id=shift_task.id,
                update_data=update_data,
            )

            return shift_task_to_return

        else:
            try:
                new_shift_task = ShiftTask(
                    closing_status=closing_status,
                    view_task_to_shift=view_task_to_shift,
                    line=line,
                    shift=shift,
                    team=team,
                    party_number=party_number,
                    party_data=party_data,
                    nomenclature=nomenclature,
                    code_ekn=code_ekn,
                    id_of_the_rc=id_of_the_rc,
                    date_time_shift_start=date_time_shift_start,
                    date_time_shift_end=date_time_shift_end,
                )

                session.add(new_shift_task)
                try:
                    await session.commit()
                    await session.refresh(new_shift_task)
                    return new_shift_task
                except IntegrityError:
                    response = ErrorResponse(
                        code=409,
                        message=f"Пара НомерПартии {party_number} и ДатаПартии {party_data} всегда уникальна!"
                    )
                    return response

            except SQLAlchemyError:
                response = ErrorResponse(code=500, message=f"База данных недоступна")
                return response

    async def find_by_several_params(
        self,
        session: AsyncSession,
        several_params: dict,
    ) -> list[ShiftTask] | ErrorResponse:
        """
        Метод находит объекты класса ShiftTask по нескольким параметрам.
        Возвращает список объектов класса ShiftTask если хотя бы один найден в БД, иначе объект ErrorResponse
        :param session: объект асинхронной сессии AsyncSession
        :param several_params: словарь с параметрами поискового запроса
        :return: list объектов класса ShiftTask или ErrorResponse
        """

        #  данное решение не является оптимальным с точки зрения использования памяти
        #  так как из БД берутся все записи, а после происходит их фильтрация python методами
        #  есть над чем подумать, чтобы фильтрация происходила сразу на уровне БД

        results = await self.find_all(session=session)

        if isinstance(results, list):

            #  немного хардкодинга

            if "closing_status" in several_params:
                results = [task for task in results if task.closing_status == several_params["closing_status"]]
            if "party_number" in several_params:
                results = [task for task in results if task.party_number == several_params["party_number"]]
            if "party_data" in several_params:
                results = [task for task in results if task.party_data == several_params["party_data"]]
            if "shift" in several_params:
                results = [task for task in results if task.shift == several_params["shift"]]
            if "team" in several_params:
                results = [task for task in results if task.team == several_params["team"]]
            if "nomenclature" in several_params:
                results = [task for task in results if task.nomenclature == several_params["nomenclature"]]
            if "code_ekn" in several_params:
                results = [task for task in results if task.code_ekn == several_params["code_ekn"]]
            if "id_of_the_rc" in several_params:
                results = [task for task in results if task.id_of_the_rc == several_params["id_of_the_rc"]]
            if "date_time_shift_start" in several_params:
                results = [task for task in results
                           if task.date_time_shift_start == several_params["date_time_shift_start"]]
            if "date_time_shift_end" in several_params:
                results = [task for task in results
                           if task.date_time_shift_end == several_params["date_time_shift_end"]]

        return results
