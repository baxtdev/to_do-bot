from pydantic import BaseModel, Field, validator
from datetime import date

class TaskModel(BaseModel):
    task_name: str = Field(..., min_length=1, max_length=100, description="Название задачи")
    start_date: date
    end_date: date

    @validator("end_date")
    def end_date_must_be_after_start_date(cls, v, values):
        if "start_date" in values and v <= values["start_date"]:
            raise ValueError("Дата окончания должна быть позже даты начала")
        return v
