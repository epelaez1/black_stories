from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass
class Milestone:
    story_id: UUID
    milestone_id: UUID
    description: str

    def __hash__(self) -> int:
        return hash(self.milestone_id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Milestone):
            return False
        return self.milestone_id == other.milestone_id


@dataclass
class Story:
    story_id: UUID
    name: str
    description: str
    full_story: str
    milestones: list[Milestone]
