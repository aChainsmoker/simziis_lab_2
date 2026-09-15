from dataclasses import dataclass


@dataclass
class DataRecord:
    id: int
    user_id: int
    title: str
    content: str

