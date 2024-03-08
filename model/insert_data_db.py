import asyncio
import datetime
from model.database import Base, db_helper
from model.models import ShiftTask
from model.static_data_for_db import shift_tasks


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
                shift=task["Смена"],
                team=task["Бригада"],
                party_number=task["НомерПартии"],
                party_data=datetime.datetime.strptime(task["ДатаПартии"], "%Y-%m-%d").date(),
                nomenclature=task["Номенклатура"],
                code_ekn=task["КодЕКН"],
                id_of_the_rc=task["ИдентификаторРЦ"],
                date_time_shift_start=datetime.datetime.fromisoformat(task["ДатаВремяНачалаСмены"]).replace(tzinfo=None),
                date_time_shift_end=datetime.datetime.fromisoformat(task["ДатаВремяОкончанияСмены"]).replace(tzinfo=None),
            )
            for task in shift_tasks
        ]

        async with session_factory() as session:
            session.add_all(task_list)
            await session.commit()

    async def main(self):
        """
        Метод запускает все необходимые методы для первоначальной инициализации таблиц БД и их наполнения
        :return: None
        """
        await self.create_tables()
        await self.insert_data_shift_tasks()


if __name__ == '__main__':
    data_base_obj = CreateTablesDataBase()
    asyncio.run(data_base_obj.main())
