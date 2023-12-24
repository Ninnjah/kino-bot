from typing import List, Optional, Union, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_serializer,
    validator,
    model_validator,
)

from .enums import (
    ProductionStatus,
    FilmType,
    FactType,
    DistributionType,
    ReleaseType,
    RelationType,
    ProfessionKey,
    Sex,
    AccountType,
    RelationType1,
    ReviewType,
    Site,
)


def to_camel(string: str) -> str:
    first, *others = string.split("_")
    return "".join([first.lower(), *map(str.title, others)])


class Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class Fact(Base):
    text: str = Field(
        ...,
        example="В эпизоде, где Тринити и Нео в поисках Морфиуса оказываются на крыше...",
    )
    type: FactType = Field(..., example="BLOOPER")
    spoiler: bool = Field(..., example=False)


class BoxOffice(Base):
    type: str = Field(..., example="BUDGET")
    amount: int = Field(..., example=63000000)
    currency_code: str = Field(..., example="USD")
    name: str = Field(..., example="US Dollar")
    symbol: str = Field(..., example="$")


class AwardPerson(Base):
    kinopoisk_id: int = Field(..., example=1937039)
    web_url: str = Field(..., example="https://www.kinopoisk.ru/name/1937039/")
    name_ru: Optional[str] = Field(..., example="Джон Т. Рейц")
    name_en: Optional[str] = Field(..., example="John T. Reitz")
    sex: str = Field(..., example="MALE")
    poster_url: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/actor_posters/kp/1937039.jpg",
    )
    growth: Optional[int] = Field(..., example=178)
    birthday: Optional[str] = Field(..., example="1955-11-02")
    death: Optional[str] = Field(..., example="2019-01-06")
    age: Optional[int] = Field(..., example=21)
    birthplace: Optional[str] = Field(..., example="Лос-Анджелес, Калифорния, США")
    deathplace: Optional[str] = Field(
        ..., example="Лос-Анджbeforeелес, Калифорния, США"
    )
    profession: Optional[str] = Field(..., example="Монтажер, Продюсер")


class Company(Base):
    name: str = Field(..., example="Каmodel_validatorро-Премьер")

    @model_serializer
    def ser_model(self) -> str:
        return self.name

    @model_validator(mode="before")
    @classmethod
    def val_model(cls, data: Any) -> Any:
        if isinstance(data, str):
            return {"name": data}
        return data


class Episode(Base):
    season_number: int = Field(..., example=1)
    episode_number: int = Field(..., example=1)
    name_ru: Optional[str] = Field(
        ..., example="Глава первая: Исчезновение Уилла Байерса"
    )
    name_en: Optional[str] = Field(
        ..., example="Chapter One: The Vanishing of Will Byers"
    )
    synopsis: Optional[str] = Field(..., example="The Vanishing of Will Byers...")
    releaseDate: Optional[str] = Field(..., example="2016-07-15")


class Country(Base):
    country: str = Field(..., example="США")

    @model_serializer
    def ser_model(self) -> str:
        return self.country

    @model_validator(mode="before")
    @classmethod
    def val_model(cls, data: Any) -> Any:
        if isinstance(data, str):
            return {"country": data}
        return data


class Genre(Base):
    genre: str = Field(..., example="фантастика")

    @model_serializer
    def ser_model(self) -> str:
        return self.genre

    @model_validator(mode="before")
    @classmethod
    def val_model(cls, data: Any) -> Any:
        if isinstance(data, str):
            return {"genre": data}
        return data


class FilmSequelsAndPrequelsResponse(Base):
    film_id: int = Field(..., example=301)
    name_ru: str = Field(..., example="Матрица")
    name_en: str = Field(..., example="The Matrix")
    name_original: str = Field(..., example="The Matrix")
    poster_url: str = Field(
        ..., example="https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg"
    )
    poster_url_preview: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
    )
    relation_type: RelationType = Field(..., example="SEQUEL")


class StaffResponse(Base):
    staff_id: int = Field(..., example=66539)
    name_ru: Optional[str] = Field(..., example="Винс Гиллиган")
    name_en: Optional[str] = Field(..., example="Vince Gilligan")
    description: Optional[str] = Field(..., example="Neo")
    poster_url: str = Field(
        ..., example="https://st.kp.yandex.net/images/actor/66539.jpg"
    )
    profession_text: str = Field(..., example="Режиссеры")
    profession_key: ProfessionKey = Field(..., example="DIRECTOR")


class PremiereResponseItem(Base):
    kinopoisk_id: int = Field(..., example=1219417)
    name_ru: Optional[str] = Field(..., example="Дитя погоды")
    name_en: Optional[str] = Field(..., example="Tenki no ko")
    year: int = Field(..., example=2019)
    poster_url: str = Field(
        ..., example="http://kinopoiskapiunofficial.tech/images/posters/kp/1219417.jpg"
    )
    poster_url_preview: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
    )
    countries: List[Country]
    genres: List[Genre]
    duration: Optional[int] = Field(..., example=112)
    premiere_ru: str = Field(..., example="2020-06-01")


class DigitalReleaseItem(Base):
    film_id: int = Field(..., example=301)
    name_ru: Optional[str] = Field(..., example="Дитя погоды")
    name_en: Optional[str] = Field(..., example="Tenki no ko")
    year: Optional[int] = Field(..., example=2019)
    poster_url: str = Field(
        ..., example="http://kinopoiskapiunofficial.tech/images/posters/kp/1219417.jpg"
    )
    poster_url_preview: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
    )
    countries: List[Country]
    genres: List[Genre]
    rating: Optional[float] = Field(..., example=7.962)
    rating_vote_count: Optional[int] = Field(..., example=14502)
    expectations_rating: Optional[float] = Field(..., example=99.13)
    expectations_rating_vote_count: Optional[int] = Field(..., example=1123)
    duration: Optional[int] = Field(..., example=112)
    release_date: str = Field(..., example="2020-06-01")


class ApiError(Base):
    message: str = Field(..., example="User test@test.ru is inactive or deleted.")

    @model_serializer
    def ser_model(self) -> str:
        return self.message

    @model_validator(mode="before")
    @classmethod
    def val_model(cls, data: Any) -> Any:
        if isinstance(data, str):
            return {"message": data}
        return data


class FiltersResponseGenres(Base):
    id: Optional[int] = Field(None, example=1)
    genre: Optional[str] = Field(None, example="боевик")


class FiltersResponseCountries(Base):
    id: Optional[int] = Field(None, example=1)
    country: Optional[str] = Field(None, example="США")


class FilmSearchResponseFilms(Base):
    film_id: Optional[int] = Field(None, example=263531)
    name_ru: Optional[str] = Field(None, example="Мстители")
    name_en: Optional[str] = Field(None, example="The Avengers")
    type: Optional[FilmType] = Field(None, example="FILM")
    year: Optional[int] = Field(None, example=2012)
    description: Optional[str] = Field(None, example="США, Джосс Уидон(фантастика)")
    film_length: Optional[str] = Field(None, example="2:17")
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating: Optional[str] = Field(
        None,
        example="NOTE!!! 7.9 for released film or 99% if film have not released yet",
    )
    rating_vote_count: Optional[int] = Field(None, example=284245)
    poster_url: Optional[str] = Field(
        None, example="http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg"
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
    )

    @validator("year", pre=True)
    def year_validator(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        if v == "null":
            return None

        try:
            return int(v)
        except ValueError:
            raise ValueError("year must be `null` or int")

    @validator("rating", pre=True)
    def rating_validator(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        if v == "null":
            return None

        return str(v)


class FilmSearchByFiltersResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, example=263531)
    imdb_id: Optional[str] = Field(None, example="tt0050561")
    name_ru: Optional[str] = Field(None, example="Мстители")
    name_en: Optional[str] = Field(None, example="The Avengers")
    name_original: Optional[str] = Field(None, example="The Avengers")
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating_kinopoisk: Optional[float] = Field(None, example=7.9)
    rating_imdb: Optional[float] = Field(None, example=7.9)
    year: Optional[float] = Field(None, example=2012)
    type: Optional[FilmType] = Field(None, example="FILM")
    poster_url: Optional[str] = Field(
        None, example="http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg"
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
    )


class RelatedFilmResponseItems(Base):
    film_id: Optional[int] = Field(None, example=301)
    name_ru: Optional[str] = Field(None, example="Матрица")
    name_en: Optional[str] = Field(None, example="The Matrix")
    name_original: Optional[str] = Field(None, example="The Matrix")
    poster_url: Optional[str] = Field(
        None, example="https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg"
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
    )
    relation_type: Optional[RelationType1] = Field(None, example="SIMILAR")


class ReviewResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, example=2)
    type: Optional[ReviewType] = None
    date: Optional[str] = Field(None, example="2010-09-05T20:37:00")
    positive_rating: Optional[int] = Field(None, example=122)
    negative_rating: Optional[int] = Field(None, example=12)
    author: Optional[str] = Field(None, example="Username")
    title: Optional[str] = Field(None, example="Title")
    description: Optional[str] = Field(None, example="text")


class ExternalSourceResponseItems(Base):
    url: Optional[str] = Field(
        None,
        example="https://okko.tv/movie/equilibrium?utm_medium=referral&utm_source=yandex_search&utm_campaign=new_search_feed",
    )
    platform: Optional[str] = Field(None, example="Okko")
    logo_url: Optional[str] = Field(
        None,
        example="https://avatars.mds.yandex.net/get-ott/239697/7713e586-17d1-42d1-ac62-53e9ef1e70c3/orig",
    )
    positive_rating: Optional[int] = Field(None, example=122)
    negative_rating: Optional[int] = Field(None, example=12)
    author: Optional[str] = Field(None, example="Username")
    title: Optional[str] = Field(None, example="Title")
    description: Optional[str] = Field(None, example="text")


class FilmCollectionResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, example=263531)
    name_ru: Optional[str] = Field(None, example="Мстители")
    name_en: Optional[str] = Field(None, example="The Avengers")
    name_original: Optional[str] = Field(None, example="The Avengers")
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating_kinopoisk: Optional[float] = Field(None, example=7.9)
    rating_imbd: Optional[float] = Field(None, example=7.9)
    year: Optional[int] = Field(None, example=2012)
    type: Optional[FilmType] = Field(None, example="FILM")
    poster_url: Optional[str] = Field(
        None, example="http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg"
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
    )


class PersonResponseSpouses(Base):
    person_id: Optional[int] = Field(None, example=32169)
    name: Optional[str] = Field(None, example="Сьюзан Дауни")
    divorced: Optional[bool] = Field(None, example=False)
    divorced_reason: Optional[str] = Field(None, example="")
    sex: Optional[Sex] = Field(None, example="MALE")
    children: Optional[int] = Field(None, example=2)
    web_url: Optional[str] = Field(None, example="https://www.kinopoisk.ru/name/32169/")
    relation: Optional[str] = Field(None, example="супруга")


class PersonResponseFilms(Base):
    film_id: Optional[int] = Field(None, example=32169)
    name_ru: Optional[str] = Field(None, example="Солист")
    name_en: Optional[str] = Field(None, example="The Soloist")
    rating: Optional[str] = Field(
        None, example="7.2 or 76% if film has not released yet"
    )
    general: Optional[bool] = Field(None, example=False)
    description: Optional[str] = Field(None, example="Steve Lopez")
    profession_key: Optional[ProfessionKey] = Field(None, example="ACTOR")

    @validator("rating", pre=True)
    def rating_validator(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        if v == "null":
            return None

        return str(v)


class PersonByNameResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, example=66539)
    web_url: Optional[str] = Field(None, example="10096")
    name_ru: Optional[str] = Field(None, example="Винс Гиллиган")
    name_en: Optional[str] = Field(None, example="Vince Gilligan")
    sex: Optional[Sex] = Field(None, example="MALE")
    poster_url: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/actor_posters/kp/10096.jpg",
    )


class ImageResponseItems(Base):
    image_url: Optional[str] = Field(
        None,
        example="https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/2924f6c4-4ea0-4a1d-9a48-f29577172b27/orig",
    )
    preview_url: Optional[str] = Field(
        None,
        example="https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/2924f6c4-4ea0-4a1d-9a48-f29577172b27/300x",
    )


class VideoResponseItems(Base):
    url: Optional[str] = Field(
        None, example="https://www.youtube.com/watch?v=gbcVZgO4n4E"
    )
    name: Optional[str] = Field(
        None, example="Мстители: Финал – официальный трейлер (16+)"
    )
    site: Optional[Site] = Field(None, example="YOUTUBE")


class KinopoiskUserVoteResponseItems(Base):
    kinopoisk_id: Optional[int] = Field(None, example=263531)
    name_ru: Optional[str] = Field(None, example="Мстители")
    name_en: Optional[str] = Field(None, example="The Avengers")
    name_original: Optional[str] = Field(None, example="The Avengers")
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating_kinopoisk: Optional[float] = Field(None, example=7.9)
    rating_imbd: Optional[float] = Field(None, example=7.9)
    year: Optional[int] = Field(None, example=2012)
    type: Optional[FilmType] = Field(None, example="FILM")
    poster_url: Optional[str] = Field(
        None, example="http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg"
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
    )
    user_rating: Optional[int] = Field(None, example=7)

    @validator("year", pre=True)
    def year_validator(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        if v == "null":
            return None

        try:
            return int(v)
        except ValueError:
            raise ValueError("year must be `null` or int")


class ApiKeyResponseTotalQuota(Base):
    value: int = Field(..., example=1000)
    used: int = Field(..., example=2)


class ApiKeyResponseDailyQuota(Base):
    value: int = Field(..., example=500)
    used: int = Field(..., example=2)


class Film(Base):
    kinopoisk_id: int = Field(..., example=301)
    kinopoisk_hd_id: Optional[str] = Field(
        ..., example="4824a95e60a7db7e86f14137516ba590"
    )
    imdb_id: Optional[str] = Field(..., example="tt0133093")
    name_ru: Optional[str] = Field(..., example="Матрица")
    name_en: Optional[str] = Field(..., example="The Matrix")
    name_original: Optional[str] = Field(..., example="The Matrix")
    poster_url: str = Field(
        ..., example="https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg"
    )
    poster_url_preview: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
    )
    cover_url: Optional[str] = Field(
        ...,
        example="https://avatars.mds.yandex.net/get-ott/1672343/2a0000016cc7177239d4025185c488b1bf43/orig",
    )
    logo_url: Optional[str] = Field(
        ...,
        example="https://avatars.mds.yandex.net/get-ott/1648503/2a00000170a5418408119bc802b53a03007b/orig",
    )
    reviews_count: int = Field(..., example=293)
    rating_good_eeview: Optional[float] = Field(..., example=88.9)
    rating_good_review_vote_count: Optional[int] = Field(..., example=257)
    rating_kinopoisk: Optional[float] = Field(..., example=8.5)
    rating_kinopoisk_vote_count: Optional[int] = Field(..., example=524108)
    rating_imdb: Optional[float] = Field(..., example=8.7)
    rating_imdb_vote_count: Optional[int] = Field(..., example=1729087)
    rating_film_critics: Optional[float] = Field(..., example=7.8)
    rating_film_critics_vote_count: Optional[int] = Field(..., example=155)
    rating_await: Optional[float] = Field(..., example=7.8)
    rating_await_count: Optional[int] = Field(..., example=2)
    rating_rf_critics: Optional[float] = Field(..., example=7.8)
    rating_rf_critics_vote_count: Optional[int] = Field(..., example=31)
    web_url: str = Field(..., example="https://www.kinopoisk.ru/film/301/")
    year: Optional[int] = Field(..., example=1999)
    film_length: Optional[int] = Field(..., example=136)
    slogan: Optional[str] = Field(..., example="Добро пожаловать в реальный мир")
    description: Optional[str] = Field(
        ..., example="Жизнь Томаса Андерсона разделена на\xa0две части:"
    )
    short_description: Optional[str] = Field(
        ...,
        example="Хакер Нео узнает, что его мир — виртуальный. Выдающийся экшен, доказавший, что зрелищное кино может быть умным",
    )
    editor_annotation: Optional[str] = Field(
        ..., example="Фильм доступен только на языке оригинала с русскими субтитрами"
    )
    is_tickets_available: bool = Field(..., example=False)
    production_status: Optional[ProductionStatus] = Field(
        ..., example="POST_PRODUCTION"
    )
    type: FilmType = Field(..., example="FILM")
    rating_mpaa: Optional[str] = Field(..., example="r")
    rating_age_limits: Optional[str] = Field(..., example="age16")
    has_imax: Optional[bool] = Field(..., example=False)
    has_3d: Optional[bool] = Field(..., example=False)
    last_sync: str = Field(..., example="2021-07-29T20:07:49.109817")
    countries: List[Country]
    genres: List[Genre]
    start_year: Optional[int] = Field(..., example=1996)
    end_year: Optional[int] = Field(..., example=1996)
    serial: Optional[bool] = Field(None, example=False)
    short_film: Optional[bool] = Field(None, example=False)
    completed: Optional[bool] = Field(None, example=False)


class FactResponse(Base):
    total: int = Field(..., example=5)
    items: List[Fact]


class BoxOfficeResponse(Base):
    total: int = Field(..., example=5)
    items: List[BoxOffice]


class Award(Base):
    name: str = Field(..., example="Оскар")
    win: bool = Field(..., example=True)
    image_url: Optional[str] = Field(
        ...,
        example="https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/09035193-2458-4de7-a7df-ad8f85b73798/orig",
    )
    nomination_name: str = Field(..., example="Лучший звук")
    year: int = Field(..., example=2000)
    persons: Optional[List[AwardPerson]] = None


class Distribution(Base):
    type: DistributionType = Field(..., example="PREMIERE")
    sub_type: Optional[ReleaseType] = Field(..., example="CINEMA")
    date: Optional[str] = Field(..., example="1999-05-07")
    re_release: Optional[bool] = Field(..., example=False)
    country: Optional[Country]
    companies: List[Company]


class Season(Base):
    number: int = Field(..., example=1)
    episodes: List[Episode]


class FiltersResponse(Base):
    genres: List[FiltersResponseGenres]
    countries: List[FiltersResponseCountries]


class FilmSearchResponse(Base):
    keyword: str = Field(..., example="мстители")
    pages_count: int = Field(..., example=7)
    search_films_count_result: int = Field(..., example=134)
    films: List[FilmSearchResponseFilms]


class FilmSearchByFiltersResponse(Base):
    total: int = Field(..., example=7)
    total_pages: int = Field(..., example=1)
    items: List[FilmSearchByFiltersResponseItems]


class RelatedFilmResponse(Base):
    total: int = Field(..., example=7)
    items: List[RelatedFilmResponseItems]


class ReviewResponse(Base):
    total: int = Field(
        ..., description="Суммарное кол-во пользовательских рецензий", example=12
    )
    total_pages: int = Field(..., example=2)
    total_positive_reviews: int = Field(..., example=1)
    total_negative_reviews: int = Field(..., example=7)
    total_neutral_reviews: int = Field(..., example=12)
    items: List[ReviewResponseItems]


class ExternalSourceResponse(Base):
    total: int = Field(..., description="Суммарное кол-во сайтов", example=12)
    items: List[ExternalSourceResponseItems]


class FilmCollectionResponse(Base):
    total: int = Field(..., example=200)
    total_pages: int = Field(..., example=7)
    items: List[FilmCollectionResponseItems]


class PersonResponse(Base):
    person_id: int = Field(..., example=66539)
    web_url: Optional[str] = Field(..., example="10096")
    name_ru: Optional[str] = Field(..., example="Винс Гиллиган")
    name_en: Optional[str] = Field(..., example="Vince Gilligan")
    sex: Optional[Sex] = Field(..., example="MALE")
    poster_url: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/actor_posters/kp/10096.jpg",
    )
    growth: Optional[int] = Field(..., example="174")
    birthday: Optional[str] = Field(..., example="1965-04-04")
    death: Optional[str] = Field(..., example="2008-01-22")
    age: Optional[int] = Field(..., example=55)
    birthplace: Optional[str] = Field(..., example="Манхэттэн, Нью-Йорк, США")
    deathplace: Optional[str] = Field(..., example="Манхэттэн, Нью-Йорк, США")
    has_awards: Optional[int] = Field(..., example=1)
    profession: Optional[str] = Field(..., example="Актер, Продюсер, Сценарист")
    facts: List[str]
    spouses: List[PersonResponseSpouses]
    films: List[PersonResponseFilms]


class PersonByNameResponse(Base):
    total: int = Field(..., example=35)
    items: List[PersonByNameResponseItems]


class ImageResponse(Base):
    total: int = Field(..., description="Общее кол-во изображений", example=50)
    total_pages: int = Field(..., description="Код-во доступных страниц", example=3)
    items: List[ImageResponseItems]


class PremiereResponse(Base):
    total: int = Field(..., example=34)
    items: List[PremiereResponseItem]


class DigitalReleaseResponse(Base):
    page: int = Field(..., example=1)
    total: int = Field(..., example=34)
    releases: List[DigitalReleaseItem]


class VideoResponse(Base):
    total: int = Field(..., example=50)
    items: List[VideoResponseItems]


class KinopoiskUserVoteResponse(Base):
    total: int = Field(..., example=200)
    totalPages: int = Field(..., example=7)
    items: List[KinopoiskUserVoteResponseItems]


class ApiKeyResponse(Base):
    total_quota: ApiKeyResponseTotalQuota = Field(...)
    daily_quota: ApiKeyResponseDailyQuota = Field(...)
    account_type: AccountType = Field(..., example="FREE")


class SeasonResponse(Base):
    total: int = Field(..., example=5)
    items: List[Season]


class DistributionResponse(Base):
    total: int = Field(..., example=5)
    items: List[Distribution]


class AwardResponse(Base):
    total: int = Field(..., example=5)
    items: List[Award]
    items: List[Award]
