import datetime

from pydantic import BaseModel, Field


class ShiftTaskDTO(BaseModel):

    closing_status: bool = Field(..., serialization_alias="СтатусЗакрытия")
    view_task_to_shift: str = Field(..., serialization_alias="ПредставлениеЗаданияНаСмену")
    line: str = Field(..., serialization_alias="Линия")
    shift: str = Field(..., serialization_alias="Смена")
    team: str = Field(..., serialization_alias="Бригада")
    party_number: int = Field(..., serialization_alias="НомерПартии")
    party_data: datetime.date = Field(..., serialization_alias="ДатаПартии")
    nomenclature: str = Field(..., serialization_alias="Номенклатура")
    code_ekn: str = Field(..., serialization_alias="КодЕКН")
    id_of_the_rc: str = Field(..., serialization_alias="ИдентификаторРЦ")
    date_time_shift_start: datetime.datetime = Field(..., serialization_alias="ДатаВремяНачалаСмены")
    date_time_shift_end: datetime.datetime = Field(..., serialization_alias="ДатаВремяОкончанияСмены")
