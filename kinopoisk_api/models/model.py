from typing import List, Optional, Union

from pydantic import BaseModel, Field, model_serializer, validator

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


class Fact(BaseModel):
    text: str = Field(
        ...,
        example="В эпизоде, где Тринити и Нео в поисках Морфиуса оказываются на крыше...",
    )
    type: FactType = Field(..., example="BLOOPER")
    spoiler: bool = Field(..., example=False)


class BoxOffice(BaseModel):
    type: str = Field(..., example="BUDGET")
    amount: int = Field(..., example=63000000)
    currency_code: str = Field(..., example="USD", alias="currencyCode")
    name: str = Field(..., example="US Dollar")
    symbol: str = Field(..., example="$")


class AwardPerson(BaseModel):
    kinopoisk_id: int = Field(..., example=1937039, alias="kinopoiskId")
    web_url: str = Field(
        ..., example="https://www.kinopoisk.ru/name/1937039/", alias="webUrl"
    )
    name_ru: Optional[str] = Field(..., example="Джон Т. Рейц", alias="nameRu")
    name_en: Optional[str] = Field(..., example="John T. Reitz", alias="nameEn")
    sex: str = Field(..., example="MALE")
    poster_url: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/actor_posters/kp/1937039.jpg",
        alias="posterUrl",
    )
    growth: Optional[int] = Field(..., example=178)
    birthday: Optional[str] = Field(..., example="1955-11-02")
    death: Optional[str] = Field(..., example="2019-01-06")
    age: Optional[int] = Field(..., example=21)
    birthplace: Optional[str] = Field(..., example="Лос-Анджелес, Калифорния, США")
    deathplace: Optional[str] = Field(..., example="Лос-Анджелес, Калифорния, США")
    profession: Optional[str] = Field(..., example="Монтажер, Продюсер")


class Company(BaseModel):
    name: str = Field(..., example="Каро-Премьер")

    @model_serializer
    def ser_model(self) -> str:
        return self.name


class Episode(BaseModel):
    season_number: int = Field(..., example=1, alias="seasonNumber")
    episode_number: int = Field(..., example=1, alias="episodeNumber")
    name_ru: Optional[str] = Field(
        ..., example="Глава первая: Исчезновение Уилла Байерса", alias="nameRu"
    )
    name_en: Optional[str] = Field(
        ..., example="Chapter One: The Vanishing of Will Byers", alias="nameEn"
    )
    synopsis: Optional[str] = Field(..., example="The Vanishing of Will Byers...")
    releaseDate: Optional[str] = Field(..., example="2016-07-15")


class Country(BaseModel):
    country: str = Field(..., example="США")

    @model_serializer
    def ser_model(self) -> str:
        return self.country


class Genre(BaseModel):
    genre: str = Field(..., example="фантастика")

    @model_serializer
    def ser_model(self) -> str:
        return self.genre


class FilmSequelsAndPrequelsResponse(BaseModel):
    film_id: int = Field(..., example=301, alias="filmId")
    name_ru: str = Field(..., example="Матрица", alias="nameRu")
    name_en: str = Field(..., example="The Matrix", alias="nameEn")
    name_original: str = Field(..., example="The Matrix", alias="nameOriginal")
    poster_url: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg",
        alias="posterUrl",
    )
    poster_url_preview: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
        alias="posterUrlPreview",
    )
    relation_type: RelationType = Field(..., example="SEQUEL", alias="relationType")


class StaffResponse(BaseModel):
    staff_id: int = Field(..., example=66539, alias="staffId")
    name_ru: Optional[str] = Field(..., example="Винс Гиллиган", alias="nameRu")
    name_en: Optional[str] = Field(..., example="Vince Gilligan", alias="nameEn")
    description: Optional[str] = Field(..., example="Neo")
    poster_url: str = Field(
        ...,
        example="https://st.kp.yandex.net/images/actor/66539.jpg",
        alias="posterUrl",
    )
    profession_text: str = Field(..., example="Режиссеры", alias="professionText")
    profession_key: ProfessionKey = Field(
        ..., example="DIRECTOR", alias="professionKey"
    )


class PremiereResponseItem(BaseModel):
    kinopoisk_id: int = Field(..., example=301, alias="kinopoiskId")
    name_ru: Optional[str] = Field(..., example="Дитя погоды", alias="nameRu")
    name_en: Optional[str] = Field(..., example="Tenki no ko", alias="nameEn")
    year: int = Field(..., example=2019)
    poster_url: str = Field(
        ...,
        example="http://kinopoiskapiunofficial.tech/images/posters/kp/1219417.jpg",
        alias="posterUrl",
    )
    poster_url_preview: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
        alias="posterUrlPreview",
    )
    countries: List[Country]
    genres: List[Genre]
    duration: Optional[int] = Field(..., example=112)
    premiere_ru: str = Field(..., example="2020-06-01", alias="premiereRu")


class DigitalReleaseItem(BaseModel):
    film_id: int = Field(..., example=301, alias="filmId")
    name_ru: Optional[str] = Field(..., example="Дитя погоды", alias="nameRu")
    name_en: Optional[str] = Field(..., example="Tenki no ko", alias="nameEn")
    year: Optional[int] = Field(..., example=2019)
    poster_url: str = Field(
        ...,
        example="http://kinopoiskapiunofficial.tech/images/posters/kp/1219417.jpg",
        alias="posterUrl",
    )
    poster_url_preview: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
        alias="posterUrlPreview",
    )
    countries: List[Country]
    genres: List[Genre]
    rating: Optional[float] = Field(..., example=7.962)
    rating_vote_count: Optional[int] = Field(
        ..., example=14502, alias="ratingVoteCount"
    )
    expectations_rating: Optional[float] = Field(
        ..., example=99.13, alias="expectationsRating"
    )
    expectations_rating_vote_count: Optional[int] = Field(
        ..., example=1123, alias="expectationsRatingVoteCount"
    )
    duration: Optional[int] = Field(..., example=112)
    release_date: str = Field(..., example="2020-06-01", alias="releaseDate")


class ApiError(BaseModel):
    message: str = Field(..., example="User test@test.ru is inactive or deleted.")

    @model_serializer
    def ser_model(self) -> str:
        return self.message


class FiltersResponseGenres(BaseModel):
    id: Optional[int] = Field(None, example=1)
    genre: Optional[str] = Field(None, example="боевик")


class FiltersResponseCountries(BaseModel):
    id: Optional[int] = Field(None, example=1)
    country: Optional[str] = Field(None, example="США")


class FilmSearchResponseFilms(BaseModel):
    film_id: Optional[int] = Field(None, example=263531, alias="filmId")
    name_ru: Optional[str] = Field(None, example="Мстители", alias="nameRu")
    name_en: Optional[str] = Field(None, example="The Avengers", alias="nameEn")
    type: Optional[FilmType] = Field(None, example="FILM")
    year: Optional[int] = Field(None, example=2012)
    description: Optional[str] = Field(None, example="США, Джосс Уидон(фантастика)")
    film_length: Optional[str] = Field(None, example="2:17", alias="filmLength")
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating: Optional[str] = Field(
        None,
        example="NOTE!!! 7.9 for released film or 99% if film have not released yet",
    )
    rating_vote_count: Optional[int] = Field(
        None, example=284245, alias="ratingVoteCount"
    )
    poster_url: Optional[str] = Field(
        None,
        example="http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg",
        alias="posterUrl",
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
        alias="posterUrlPreview",
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


class FilmSearchByFiltersResponseItems(BaseModel):
    kinopoisk_id: Optional[int] = Field(None, example=263531, alias="kinopoiskId")
    imdb_id: Optional[str] = Field(None, example="tt0050561", alias="imdbId")
    name_ru: Optional[str] = Field(None, example="Мстители", alias="nameRu")
    name_en: Optional[str] = Field(None, example="The Avengers", alias="nameEn")
    name_original: Optional[str] = Field(
        None, example="The Avengers", alias="nameOriginal"
    )
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating_kinopoisk: Optional[float] = Field(
        None, example=7.9, alias="ratingKinopoisk"
    )
    rating_imdb: Optional[float] = Field(None, example=7.9, alias="ratingImdb")
    year: Optional[float] = Field(None, example=2012)
    type: Optional[FilmType] = Field(None, example="FILM")
    poster_url: Optional[str] = Field(
        None,
        example="http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg",
        alias="posterUrl",
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
        alias="posterUrlPreview",
    )


class RelatedFilmResponseItems(BaseModel):
    film_id: Optional[int] = Field(None, example=301, alias="filmId")
    name_ru: Optional[str] = Field(None, example="Матрица", alias="nameRu")
    name_en: Optional[str] = Field(None, example="The Matrix", alias="nameEn")
    name_original: Optional[str] = Field(
        None, example="The Matrix", alias="nameOriginal"
    )
    poster_url: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg",
        alias="posterUrl",
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
        alias="posterUrlPreview",
    )
    relation_type: Optional[RelationType1] = Field(
        None, example="SIMILAR", alias="relationType"
    )


class ReviewResponseItems(BaseModel):
    kinopoisk_id: Optional[int] = Field(None, example=2, alias="kinopoiskId")
    type: Optional[ReviewType] = None
    date: Optional[str] = Field(None, example="2010-09-05T20:37:00")
    positive_rating: Optional[int] = Field(None, example=122, alias="positiveRating")
    negative_rating: Optional[int] = Field(None, example=12, alias="negativeRating")
    author: Optional[str] = Field(None, example="Username")
    title: Optional[str] = Field(None, example="Title")
    description: Optional[str] = Field(None, example="text")


class ExternalSourceResponseItems(BaseModel):
    url: Optional[str] = Field(
        None,
        example="https://okko.tv/movie/equilibrium?utm_medium=referral&utm_source=yandex_search&utm_campaign=new_search_feed",
    )
    platform: Optional[str] = Field(None, example="Okko")
    logo_url: Optional[str] = Field(
        None,
        example="https://avatars.mds.yandex.net/get-ott/239697/7713e586-17d1-42d1-ac62-53e9ef1e70c3/orig",
        alias="logoUrl",
    )
    positive_rating: Optional[int] = Field(None, example=122, alias="positiveRating")
    negative_rating: Optional[int] = Field(None, example=12, alias="negativeRating")
    author: Optional[str] = Field(None, example="Username")
    title: Optional[str] = Field(None, example="Title")
    description: Optional[str] = Field(None, example="text")


class FilmCollectionResponseItems(BaseModel):
    kinopoisk_id: Optional[int] = Field(None, example=263531, alias="kinopoiskId")
    name_ru: Optional[str] = Field(None, example="Мстители", alias="nameRu")
    name_en: Optional[str] = Field(None, example="The Avengers", alias="nameEn")
    name_original: Optional[str] = Field(
        None, example="The Avengers", alias="nameOriginal"
    )
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating_kinopoisk: Optional[float] = Field(
        None, example=7.9, alias="ratingKinopoisk"
    )
    rating_imbd: Optional[float] = Field(None, example=7.9, alias="ratingImbd")
    year: Optional[int] = Field(None, example=2012)
    type: Optional[FilmType] = Field(None, example="FILM")
    poster_url: Optional[str] = Field(
        None,
        example="http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg",
        alias="posterUrl",
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
        alias="posterUrlPreview",
    )


class PersonResponseSpouses(BaseModel):
    person_id: Optional[int] = Field(None, example=32169, alias="personId")
    name: Optional[str] = Field(None, example="Сьюзан Дауни")
    divorced: Optional[bool] = Field(None, example=False)
    divorced_reason: Optional[str] = Field(None, example="", alias="divorcedReason")
    sex: Optional[Sex] = Field(None, example="MALE")
    children: Optional[int] = Field(None, example=2)
    web_url: Optional[str] = Field(
        None, example="https://www.kinopoisk.ru/name/32169/", alias="webUrl"
    )
    relation: Optional[str] = Field(None, example="супруга")


class PersonResponseFilms(BaseModel):
    film_id: Optional[int] = Field(None, example=32169, alias="filmId")
    name_ru: Optional[str] = Field(None, example="Солист", alias="nameRu")
    name_en: Optional[str] = Field(None, example="The Soloist", alias="nameEn")
    rating: Optional[str] = Field(
        None, example="7.2 or 76% if film has not released yet"
    )
    general: Optional[bool] = Field(None, example=False)
    description: Optional[str] = Field(None, example="Steve Lopez")
    profession_key: Optional[ProfessionKey] = Field(
        None, example="ACTOR", alias="professionKey"
    )

    @validator("rating", pre=True)
    def rating_validator(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        if v == "null":
            return None

        return str(v)


class PersonByNameResponseItems(BaseModel):
    kinopoisk_id: Optional[int] = Field(None, example=66539, alias="kinopoiskId")
    web_url: Optional[str] = Field(None, example="10096", alias="webUrl")
    name_ru: Optional[str] = Field(None, example="Винс Гиллиган", alias="nameRu")
    name_en: Optional[str] = Field(None, example="Vince Gilligan", alias="nameEn")
    sex: Optional[Sex] = Field(None, example="MALE")
    poster_url: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/actor_posters/kp/10096.jpg",
        alias="posterUrl",
    )


class ImageResponseItems(BaseModel):
    image_url: Optional[str] = Field(
        None,
        example="https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/2924f6c4-4ea0-4a1d-9a48-f29577172b27/orig",
        alias="imageUrl",
    )
    preview_url: Optional[str] = Field(
        None,
        example="https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/2924f6c4-4ea0-4a1d-9a48-f29577172b27/300x",
        alias="previewUrl",
    )


class VideoResponseItems(BaseModel):
    url: Optional[str] = Field(
        None, example="https://www.youtube.com/watch?v=gbcVZgO4n4E"
    )
    name: Optional[str] = Field(
        None, example="Мстители: Финал – официальный трейлер (16+)"
    )
    site: Optional[Site] = Field(None, example="YOUTUBE")


class KinopoiskUserVoteResponseItems(BaseModel):
    kinopoisk_id: Optional[int] = Field(None, example=263531, alias="kinopoiskId")
    name_ru: Optional[str] = Field(None, example="Мстители", alias="nameRu")
    name_en: Optional[str] = Field(None, example="The Avengers", alias="nameEn")
    name_original: Optional[str] = Field(
        None, example="The Avengers", alias="nameOriginal"
    )
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    rating_kinopoisk: Optional[float] = Field(
        None, example=7.9, alias="ratingKinopoisk"
    )
    rating_imbd: Optional[float] = Field(None, example=7.9, alias="ratingImbd")
    year: Optional[int] = Field(None, example=2012)
    type: Optional[FilmType] = Field(None, example="FILM")
    poster_url: Optional[str] = Field(
        None,
        example="http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg",
        alias="posterUrl",
    )
    poster_url_preview: Optional[str] = Field(
        None,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
        alias="posterUrlPreview",
    )
    user_rating: Optional[int] = Field(None, example=7, alias="userRating")

    @validator("year", pre=True)
    def year_validator(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        if v == "null":
            return None

        try:
            return int(v)
        except ValueError:
            raise ValueError("year must be `null` or int")


class ApiKeyResponseTotalQuota(BaseModel):
    value: int = Field(..., example=1000)
    used: int = Field(..., example=2)


class ApiKeyResponseDailyQuota(BaseModel):
    value: int = Field(..., example=500)
    used: int = Field(..., example=2)


class Film(BaseModel):
    kinopoisk_id: int = Field(..., example=301, alias="kinopoiskId")
    kinopoisk_hd_id: Optional[str] = Field(
        ..., example="4824a95e60a7db7e86f14137516ba590", alias="kinopoiskHDId"
    )
    imdb_id: Optional[str] = Field(..., example="tt0133093", alias="imdbId")
    name_ru: Optional[str] = Field(..., example="Матрица", alias="nameRu")
    name_en: Optional[str] = Field(..., example="The Matrix", alias="nameEn")
    name_original: Optional[str] = Field(
        ..., example="The Matrix", alias="nameOriginal"
    )
    poster_url: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg",
        alias="posterUrl",
    )
    poster_url_preview: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg",
        alias="posterUrlPreview",
    )
    cover_url: Optional[str] = Field(
        ...,
        example="https://avatars.mds.yandex.net/get-ott/1672343/2a0000016cc7177239d4025185c488b1bf43/orig",
        alias="coverUrl",
    )
    logo_url: Optional[str] = Field(
        ...,
        example="https://avatars.mds.yandex.net/get-ott/1648503/2a00000170a5418408119bc802b53a03007b/orig",
        alias="logoUrl",
    )
    reviews_count: int = Field(..., example=293, alias="reviewsCount")
    rating_good_eeview: Optional[float] = Field(
        ..., example=88.9, alias="ratingGoodReview"
    )
    rating_good_review_vote_count: Optional[int] = Field(
        ..., example=257, alias="ratingGoodReviewVoteCount"
    )
    rating_kinopoisk: Optional[float] = Field(..., example=8.5, alias="ratingKinopoisk")
    rating_kinopoisk_vote_count: Optional[int] = Field(
        ..., example=524108, alias="ratingKinopoiskVoteCount"
    )
    rating_imdb: Optional[float] = Field(..., example=8.7, alias="ratingImdb")
    rating_imdb_vote_count: Optional[int] = Field(
        ..., example=1729087, alias="ratingImdbVoteCount"
    )
    rating_film_critics: Optional[float] = Field(
        ..., example=7.8, alias="ratingFilmCritics"
    )
    rating_film_critics_vote_count: Optional[int] = Field(
        ..., example=155, alias="ratingFilmCriticsVoteCount"
    )
    rating_await: Optional[float] = Field(..., example=7.8, alias="ratingAwait")
    rating_await_count: Optional[int] = Field(..., example=2, alias="ratingAwaitCount")
    rating_rf_critics: Optional[float] = Field(
        ..., example=7.8, alias="ratingRfCritics"
    )
    rating_rf_critics_vote_count: Optional[int] = Field(
        ..., example=31, alias="ratingRfCriticsVoteCount"
    )
    web_url: str = Field(
        ..., example="https://www.kinopoisk.ru/film/301/", alias="webUrl"
    )
    year: Optional[int] = Field(..., example=1999)
    film_length: Optional[int] = Field(..., example=136, alias="filmLength")
    slogan: Optional[str] = Field(..., example="Добро пожаловать в реальный мир")
    description: Optional[str] = Field(
        ..., example="Жизнь Томаса Андерсона разделена на\xa0две части:"
    )
    short_description: Optional[str] = Field(
        ...,
        example="Хакер Нео узнает, что его мир — виртуальный. Выдающийся экшен, доказавший, что зрелищное кино может быть умным",
        alias="shortDescription",
    )
    editor_annotation: Optional[str] = Field(
        ...,
        example="Фильм доступен только на языке оригинала с русскими субтитрами",
        alias="editorAnnotation",
    )
    is_tickets_available: bool = Field(..., example=False, alias="isTicketsAvailable")
    production_status: Optional[ProductionStatus] = Field(
        ..., example="POST_PRODUCTION", alias="productionStatus"
    )
    type: FilmType = Field(..., example="FILM")
    rating_mpaa: Optional[str] = Field(..., example="r", alias="ratingMpaa")
    rating_age_limits: Optional[str] = Field(
        ..., example="age16", alias="ratingAgeLimits"
    )
    has_imax: Optional[bool] = Field(..., example=False, alias="hasImax")
    has_3d: Optional[bool] = Field(..., example=False, alias="has3D")
    last_sync: str = Field(..., example="2021-07-29T20:07:49.109817", alias="lastSync")
    countries: List[Country]
    genres: List[Genre]
    start_year: Optional[int] = Field(..., example=1996, alias="startYear")
    end_year: Optional[int] = Field(..., example=1996, alias="endYear")
    serial: Optional[bool] = Field(None, example=False, alias="serial")
    short_film: Optional[bool] = Field(None, example=False, alias="shortFilm")
    completed: Optional[bool] = Field(None, example=False)


class FactResponse(BaseModel):
    total: int = Field(..., example=5)
    items: List[Fact]


class BoxOfficeResponse(BaseModel):
    total: int = Field(..., example=5)
    items: List[BoxOffice]


class Award(BaseModel):
    name: str = Field(..., example="Оскар")
    win: bool = Field(..., example=True)
    image_url: Optional[str] = Field(
        ...,
        example="https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/09035193-2458-4de7-a7df-ad8f85b73798/orig",
        alias="imageUrl",
    )
    nomination_name: str = Field(..., example="Лучший звук", alias="nominationName")
    year: int = Field(..., example=2000)
    persons: Optional[List[AwardPerson]] = None


class Distribution(BaseModel):
    type: DistributionType = Field(..., example="PREMIERE")
    sub_type: Optional[ReleaseType] = Field(..., example="CINEMA", alias="subType")
    date: Optional[str] = Field(..., example="1999-05-07")
    re_release: Optional[bool] = Field(..., example=False, alias="reRelease")
    country: Optional[Country]
    companies: List[Company]


class Season(BaseModel):
    number: int = Field(..., example=1)
    episodes: List[Episode]


class FiltersResponse(BaseModel):
    genres: List[FiltersResponseGenres]
    countries: List[FiltersResponseCountries]


class FilmSearchResponse(BaseModel):
    keyword: str = Field(..., example="мстители")
    pages_count: int = Field(..., example=7, alias="pagesCount")
    search_films_count_result: int = Field(
        ..., example=134, alias="searchFilmsCountResult"
    )
    films: List[FilmSearchResponseFilms]


class FilmSearchByFiltersResponse(BaseModel):
    total: int = Field(..., example=7)
    total_pages: int = Field(..., example=1, alias="totalPages")
    items: List[FilmSearchByFiltersResponseItems]


class RelatedFilmResponse(BaseModel):
    total: int = Field(..., example=7)
    items: List[RelatedFilmResponseItems]


class ReviewResponse(BaseModel):
    total: int = Field(
        ..., description="Суммарное кол-во пользовательских рецензий", example=12
    )
    total_pages: int = Field(..., example=2, alias="totalPages")
    total_positive_reviews: int = Field(..., example=1, alias="totalPositiveReviews")
    total_negative_reviews: int = Field(..., example=7, alias="totalNegativeReviews")
    total_neutral_reviews: int = Field(..., example=12, alias="totalNeutralReviews")
    items: List[ReviewResponseItems]


class ExternalSourceResponse(BaseModel):
    total: int = Field(..., description="Суммарное кол-во сайтов", example=12)
    items: List[ExternalSourceResponseItems]


class FilmCollectionResponse(BaseModel):
    total: int = Field(..., example=200)
    total_pages: int = Field(..., example=7, alias="totalPages")
    items: List[FilmCollectionResponseItems]


class PersonResponse(BaseModel):
    person_id: int = Field(..., example=66539, alias="personId")
    web_url: Optional[str] = Field(..., example="10096", alias="webUrl")
    name_ru: Optional[str] = Field(..., example="Винс Гиллиган", alias="nameRu")
    name_en: Optional[str] = Field(..., example="Vince Gilligan", alias="nameEn")
    sex: Optional[Sex] = Field(..., example="MALE")
    poster_url: str = Field(
        ...,
        example="https://kinopoiskapiunofficial.tech/images/actor_posters/kp/10096.jpg",
        alias="posterUrl",
    )
    growth: Optional[int] = Field(..., example="174")
    birthday: Optional[str] = Field(..., example="1965-04-04")
    death: Optional[str] = Field(..., example="2008-01-22")
    age: Optional[int] = Field(..., example=55)
    birthplace: Optional[str] = Field(..., example="Манхэттэн, Нью-Йорк, США")
    deathplace: Optional[str] = Field(..., example="Манхэттэн, Нью-Йорк, США")
    has_awards: Optional[int] = Field(..., example=1, alias="hasAwards")
    profession: Optional[str] = Field(..., example="Актер, Продюсер, Сценарист")
    facts: List[str]
    spouses: List[PersonResponseSpouses]
    films: List[PersonResponseFilms]


class PersonByNameResponse(BaseModel):
    total: int = Field(..., example=35)
    items: List[PersonByNameResponseItems]


class ImageResponse(BaseModel):
    total: int = Field(..., description="Общее кол-во изображений", example=50)
    total_pages: int = Field(
        ..., description="Код-во доступных страниц", example=3, alias="totalPages"
    )
    items: List[ImageResponseItems]


class PremiereResponse(BaseModel):
    total: int = Field(..., example=34)
    items: List[PremiereResponseItem]


class DigitalReleaseResponse(BaseModel):
    page: int = Field(..., example=1)
    total: int = Field(..., example=34)
    releases: List[DigitalReleaseItem]


class VideoResponse(BaseModel):
    total: int = Field(..., example=50)
    items: List[VideoResponseItems]


class KinopoiskUserVoteResponse(BaseModel):
    total: int = Field(..., example=200)
    totalPages: int = Field(..., example=7)
    items: List[KinopoiskUserVoteResponseItems]


class ApiKeyResponse(BaseModel):
    total_quota: ApiKeyResponseTotalQuota = Field(..., alias="totalQuota")
    daily_quota: ApiKeyResponseDailyQuota = Field(..., alias="dailyQuota")
    account_type: AccountType = Field(..., example="FREE", alias="accountType")


class SeasonResponse(BaseModel):
    total: int = Field(..., example=5)
    items: List[Season]


class DistributionResponse(BaseModel):
    total: int = Field(..., example=5)
    items: List[Distribution]


class AwardResponse(BaseModel):
    total: int = Field(..., example=5)
    items: List[Award]
