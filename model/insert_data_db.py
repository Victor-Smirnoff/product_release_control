import asyncio
import datetime

from sqlalchemy import select, and_

from model.database import Base, db_helper
from model.models import ShiftTask, UniqueProductIdentifiers
from model.static_data_for_db import shift_tasks, unique_product_identifiers


engine = db_helper.engine
session_factory = db_helper.session_factory


class CreateTablesDataBase:
    @staticmethod
    def drop_tables():
        """
        Метод удаляет все записи из БД и удаляет таблицы из базы данных product_release_control
        :return: None
        """
        Base.metadata.drop_all(engine)

    @staticmethod
    async def create_tables():
        """
        Метод создает две таблицы в базе данных product_release_control:
        shift_tasks - таблица с данными по сменным заданиям
        unique_product_identifiers - таблица с данными по уникальным айди продукции
        :return: None
        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_data_shift_tasks():
        task_list = [
            ShiftTask(
                closing_status=task["СтатусЗакрытия"],
                view_task_to_shift=task["ПредставлениеЗаданияНаСмену"],
                work_center=task["РабочийЦентр"],
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
            for task in shift_tasks
        ]

        async with session_factory() as session:
            session.add_all(task_list)
            await session.commit()

    async def insert_data_unique_product_identifiers(self):
        unique_product_identifier_list = []

        for product_identifier in unique_product_identifiers:
            party_number = product_identifier["НомерПартии"]
            party_data = datetime.datetime.strptime(product_identifier["ДатаПартии"], "%Y-%m-%d").date()

            shift_task = await self.find_unique_shift_task(
                party_number=party_number,
                party_data=party_data,
            )

            if type(shift_task) is ShiftTask:
                new_product = UniqueProductIdentifiers(
                    unique_product_code=product_identifier["УникальныйКодПродукта"],
                    shift_task_id=shift_task.id,
                    is_aggregated=False,
                    aggregated_at=None
                )
                unique_product_identifier_list.append(new_product)

        if unique_product_identifier_list:
            async with session_factory() as session:
                session.add_all(unique_product_identifier_list)
                await session.commit()
        else:
            print("unique_product_identifier_list пустой вышел!!!!")

    @staticmethod
    async def find_unique_shift_task(party_number: int, party_data: datetime.date) -> ShiftTask | None:
        async with session_factory() as session:
            query = select(ShiftTask).where(and_(
                ShiftTask.party_number == party_number,
                ShiftTask.party_data == party_data
                )
            )
            result = await session.execute(query)
            shift_task = result.scalars().one()
            return shift_task if shift_task else None

    async def main(self):
        """
        Метод запускает все необходимые методы для первоначальной инициализации таблиц БД и их наполнения
        :return: None
        """
        await self.create_tables()
        await self.insert_data_shift_tasks()
        await self.insert_data_unique_product_identifiers()


if __name__ == '__main__':
    data_base_obj = CreateTablesDataBase()
    asyncio.run(data_base_obj.main())
