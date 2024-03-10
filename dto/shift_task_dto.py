import datetime

from pydantic import BaseModel, Field


class ShiftTaskDTO(BaseModel):

    closing_status: bool = Field(..., validation_alias="СтатусЗакрытия")
    view_task_to_shift: str = Field(..., validation_alias="ПредставлениеЗаданияНаСмену")
    line: str = Field(..., validation_alias="Линия")
    shift: str = Field(..., validation_alias="Смена")
    team: str = Field(..., validation_alias="Бригада")
    party_number: int = Field(..., validation_alias="НомерПартии")
    party_data: datetime.date = Field(..., validation_alias="ДатаПартии")
    nomenclature: str = Field(..., validation_alias="Номенклатура")
    code_ekn: str = Field(..., validation_alias="КодЕКН")
    id_of_the_rc: str = Field(..., validation_alias="ИдентификаторРЦ")
    date_time_shift_start: datetime.datetime = Field(..., validation_alias="ИдентификаторРЦ")
    date_time_shift_end: datetime.datetime = Field(..., validation_alias="ИдентификаторРЦ")
