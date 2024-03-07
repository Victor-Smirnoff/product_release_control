import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from model.database import Base


class ShiftTask(Base):
    __tablename__ = "shift_tasks"

    closing_status: Mapped[bool]
    closed_at: Mapped[datetime.time] = mapped_column(default=None)
    view_task_to_shift: Mapped[str] = mapped_column(String(100))
    work_center: Mapped[str] = mapped_column(String(100))
    shift: Mapped[str] = mapped_column(String(100))
    team: Mapped[str] = mapped_column(String(100))
    party_number: Mapped[int]
    party_data: Mapped[datetime.date]
    nomenclature: Mapped[str] = mapped_column(String(100))
    code_ekn: Mapped[str] = mapped_column(String(100))
    id_of_the_rc: Mapped[str] = mapped_column(String(100))
    date_time_shift_start: Mapped[datetime.datetime]
    date_time_shift_end: Mapped[datetime.datetime]


class UniqueProductIdentifiers(Base):
    __tablename__ = "unique_product_identifiers"

    unique_product_code: Mapped[str] = mapped_column(String(100), unique=True)
    party_number: Mapped[str] = mapped_column(ForeignKey("shift_tasks.party_number"))
    party_data: Mapped[datetime.date] = mapped_column(ForeignKey("shift_tasks.party_data"))
    is_aggregated: Mapped[bool] = mapped_column(default=False)
    aggregated_at: Mapped[datetime.datetime] = mapped_column(default=None)