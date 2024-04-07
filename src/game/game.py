from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from enum import StrEnum

from src.game.story import Milestone
from src.game.story import Story


class Answer(StrEnum):
    YES = "yes"
    NO = "no"
    NOT_RELEVANT = "not_relevant"
    INVALID_QUESTION = "invalid_question"


class InputManager(ABC):
    @abstractmethod
    def get_question(self) -> Answer:
        raise NotImplementedError()


class OutputManager(ABC):
    @abstractmethod
    def introduce_story(self, story: Story) -> None:
        raise NotImplementedError()

    @abstractmethod
    def show_answer(self, answer: Answer) -> None:
        raise NotImplementedError()

    @abstractmethod
    def end_game(self, story: Story) -> None:
        raise NotImplementedError()


class QuestionInterpreter(ABC):
    @abstractmethod
    def answer_question(self, question: str, story: Story) -> Answer:
        raise NotImplementedError()

    @abstractmethod
    def get_discovered_milestones(self, story: Story) -> list[Milestone]:
        raise NotImplementedError()


@dataclass
class Game:
    story: Story
    discovered_milestones: set[Milestone] = field(default_factory=set)

    def play(
        self,
        input_manager: InputManager,
        output_manager: OutputManager,
        question_interpreter: QuestionInterpreter,
    ) -> None:
        output_manager.introduce_story(self.story)
        while len(self.discovered_milestones) < len(self.story.milestones) - 1:
            question = input_manager.get_question()
            answer = question_interpreter.answer_question(question, self.story)
            output_manager.show_answer(answer)
            if answer == Answer.YES:
                discovered_milestones = question_interpreter.get_discovered_milestones(self.story)
                self.discovered_milestones.update(discovered_milestones)

        output_manager.end_game(self.story)
