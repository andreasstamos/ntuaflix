from typing import Optional, Annotated
from pydantic import Field, validator, root_validator, StringConstraints

from .basic import ORMModel, QueryModel

class NameTitle(ORMModel):
    tconst: str = Field(..., alias="titleID")
    category: str

    @validator('category', pre=True)
    def get_category_name(cls, value):
        return value.name

class NameObject(ORMModel):
    nconst: str = Field(..., alias="nameID")
    primary_name: str = Field(..., alias="name")
    image_url: Optional[str] = Field(..., alias="namePoster")
    birth_year: str = Field(..., alias="birthYr")
    death_year: str = Field(..., alias="deathYr")

    primary_professions: str = Field(..., alias="profession")

    titles_as_principal: list[NameTitle]

    @validator('primary_professions', pre=True)
    def concat_professions(cls, value) -> str:
        return ','.join([profession.name for profession in value])

    @validator('birth_year', 'death_year', pre=True)
    def int_to_str(cls, value: int) -> str:
        return str(value)


class NqueryObject(QueryModel):
    namePart: str

