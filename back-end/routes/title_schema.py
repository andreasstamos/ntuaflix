from pydantic import BaseModel, Field, validator, root_validator

class ORMModel(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True

class Genre(ORMModel):
    name: str = Field(..., alias="genreName")

class TitleAka(ORMModel):
    title_name: str = Field(..., alias="akaTitle")
    region: str | None = Field(..., alias="regionAbbrev")

class Principal(ORMModel):
    nconst: str = Field(..., alias="nameID")
    primaryName: str
    category_name: str = Field(..., serialization_alias="category")

    @root_validator(pre=True)
    def get_fields(cls, data):
        data.primaryName = data.person.primary_name
        data.category_name = data.category.name
        return data

class Rating(ORMModel):
    avRating: str
    nVotes: str

class TitleObject(ORMModel):
    tconst: str = Field(..., alias="titleID")
    title_type: str = Field(..., alias="type")
    originalTitle: str = Field(..., alias="original_title")
    image_url: str | None = Field(..., alias="titlePoster")
    start_year: str = Field(..., alias="startYear")
    end_year: str = Field(..., alias="endYear")
    genres: list[Genre]
    aliases: list[TitleAka] = Field(..., alias="titleAkas")
    principals: list[Principal]
    rating: Rating

    @root_validator(pre=True)
    def get_ratings(cls, values):
        values.rating = Rating(avRating=f"{values.average_rating:.1f}", nVotes=str(values.num_votes))
        return values
    
    @validator('start_year', 'end_year', pre=True)
    def int_to_str(cls, value: int) -> str:
        return str(value)


