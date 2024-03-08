import asyncio
from sqlalchemy import select
from model.database import Base, db_helper
from model.models import ShiftTask, UniqueProductIdentifiers


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

    async def main(self):
        """
        Метод запускает все необходимые методы для первоначальной инициализации таблиц БД и их наполнения
        :return: None
        """
        # self.create_tables()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


if __name__ == '__main__':
    data_base_obj = CreateTablesDataBase()
    asyncio.run(data_base_obj.main())
