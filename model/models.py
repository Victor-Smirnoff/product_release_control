from model.database import Base


class ShiftTask(Base):
    __tablename__ = "shift_tasks"


class UniqueProductIdentifiers(Base):
    __tablename__ = "unique_product_identifiers"
