from typing import List, Optional, Dict, Type, Union

from aiogram.types import (
    PhotoSize,
    Video,
    Audio,
    Document,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAudio,
    InputMediaDocument,
    Message,
)
from pydantic import BaseModel


Media = Union[PhotoSize, Video, Audio, Document]
InputMedia = Union[
    InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
]
INPUT_TYPES: Dict[str, Type[InputMedia]] = {
    "photo": InputMediaPhoto,
    "video": InputMediaVideo,
    "audio": InputMediaAudio,
    "document": InputMediaDocument,
}


class Album(BaseModel):
    photo: Optional[List[PhotoSize]] = None
    video: Optional[List[Video]] = None
    audio: Optional[List[Audio]] = None
    document: Optional[List[Document]] = None
    caption: Optional[str] = None
    messages: List[Message]

    @property
    def media_types(self) -> List[str]:
        return [media_type for media_type in INPUT_TYPES if getattr(self, media_type)]

    @property
    def as_media_group(self) -> List[InputMedia]:
        group = [
            INPUT_TYPES[media_type](
                type=media_type,
                media=media.file_id,
                caption=self.caption if i == 0 else None,
            )
            for media_type in self.media_types
            for i, media in enumerate(getattr(self, media_type))
        ]

        return group
