import typing
from pydantic import BaseModel
from pydantic import Field

# Максимальная длина data в базе данных
data_length = 10


# Модель для ввода данных
class InputData(BaseModel):
    data: str = Field(..., title="Data", description="Retrieved data", max_length=data_length)  # данные


# Модель единичной записи данных
class Data(BaseModel):

    data_id: int  # ID данных в базе данных
    data: str = Field(..., title="Data", description="Retrieved data", max_length=data_length)  # данные


# Общая модель данных
class GeneralData(BaseModel):

    dataOutput: typing.List[Data] = []