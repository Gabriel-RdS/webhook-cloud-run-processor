from enum import Enum

class Segment(Enum):
    AYABOOKS = "ayabooksexatecnologia"
    EXA = "exatecnologia"

    @classmethod
    def get_base_path(cls, segment_name: str) -> str:
        segment_paths = {
            cls.AYABOOKS.value: "staging/insider/ayabooksexatecnologia",
            cls.EXA.value: "staging/insider/exatecnologia"
        }
        return segment_paths.get(segment_name)

    @classmethod
    def is_valid(cls, segment_name: str) -> bool:
        return segment_name in [segment.value for segment in cls]