from dto import ShiftTaskDTO
from model import ShiftTask


class ShiftTaskDtoService:

    def get_shift_task_dto(self, shift_task: ShiftTask) -> ShiftTaskDTO:

        shift_task_dto = ShiftTaskDTO(
            closing_status=shift_task.closing_status,
            view_task_to_shift=shift_task.view_task_to_shift,
            line=shift_task.line,
            shift=shift_task.shift,
            team=shift_task.team,
            party_number=shift_task.party_number,
            party_data=shift_task.party_data,
            nomenclature=shift_task.nomenclature,
            code_ekn=shift_task.code_ekn,
            id_of_the_rc=shift_task.id_of_the_rc,
            date_time_shift_start=shift_task.date_time_shift_start,
            date_time_shift_end=shift_task.date_time_shift_end,
        )

        return shift_task_dto
