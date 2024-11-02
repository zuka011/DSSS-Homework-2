from typing import Protocol
from dataclasses import dataclass, field


import random


class Operator(Protocol):
    def operate(self, left_operand: int, right_operand: int) -> int:
        """Performs a mathematical operation on the provided operands."""
        ...

    def stringify(self) -> str:
        """Returns a human-readable string representation of the operator."""
        ...


class Addition:
    def operate(self, left_operand: int, right_operand: int) -> int:
        return left_operand + right_operand

    def stringify(self) -> str:
        return "+"


class Subtraction:
    def operate(self, left_operand: int, right_operand: int) -> int:
        return left_operand - right_operand

    def stringify(self) -> str:
        return "-"


class Multiplication:
    def operate(self, left_operand: int, right_operand: int) -> int:
        return left_operand * right_operand

    def stringify(self) -> str:
        return "*"


@dataclass(frozen=True)
class Answer:
    is_correct: bool

    @staticmethod
    def missing() -> "Answer":
        return Answer(is_correct=False)


@dataclass
class Question:
    _left_operand: int
    _right_operand: int
    _operator: Operator
    _answer: Answer = Answer.missing()

    def present(self) -> None:
        print(f"Question: {self.formatted()} = ?")

    def formatted(self) -> str:
        return (
            f"{self._left_operand} {self._operator.stringify()} {self._right_operand}"
        )

    def answered_with(self, answer: int) -> "Answer":
        self._answer = Answer(is_correct=answer == self.correct_answer())
        return self._answer

    def correct_answer(self) -> int:
        return self._operator.operate(self._left_operand, self._right_operand)

    @property
    def answer(self) -> Answer:
        return self._answer


@dataclass(frozen=True)
class QuestionSet:
    question_count: int
    left_range: tuple[int, int]
    right_range: tuple[int, int]
    _generated_questions: list[Question] = field(default_factory=list)

    @staticmethod
    def of_size(question_count: int) -> "QuestionSet.Builder":
        return QuestionSet.Builder(question_count)

    def __iter__(self) -> "QuestionSet":
        return self

    def __next__(self) -> Question:
        if len(self._generated_questions) == self.question_count:
            raise StopIteration

        question = generate_question(
            left_operand=self._left_operand(),
            right_operand=self._right_operand(),
            operator=self._operator(),
        )

        self._generated_questions.append(question)

        return question

    def present_results(self) -> None:
        correct_count = sum(
            1 for question in self._generated_questions if question.answer.is_correct
        )
        print(f"\nGame over! Your score is: {correct_count}/{self.question_count}")

    @dataclass
    class Builder:
        question_count: int
        left_range: tuple[int, int] = (1, 10)

        def with_left_operands_from(
            self, start: int, /, *, to: int
        ) -> "QuestionSet.Builder":
            self.left_range = (start, to)
            return self

        def and_right_operands_from(self, start: int, /, *, to: int) -> "QuestionSet":
            return QuestionSet(
                question_count=self.question_count,
                left_range=self.left_range,
                right_range=(start, to),
            )

    def _left_operand(self) -> int:
        return random_integer_from(self.left_range[0], to=self.right_range[1])

    def _right_operand(self) -> int:
        return random_integer_from(self.right_range[0], to=self.right_range[1])

    def _operator(self) -> Operator:
        return random_operator()


def random_integer_from(start: int, /, *, to: int) -> int:
    """Generates a random integer between the specified `start` and `to` values. The range is inclusive.

    Example:
        >>> random_integer_from(1, to=10)
        7
        >>> random_integer_from(1, to=10)
        3
    """
    return random.randint(start, to)


def random_operator() -> Operator:
    """Generates a random operator from the set of supported operators.

    Example:
        >>> operator = random_operator()
        >>> operator.stringify()
        '+'
        >>> operator.operate(5, 2)
        7
    """
    return random.choice([Addition(), Subtraction(), Multiplication()])


def generate_question(
    *, left_operand: int, right_operand: int, operator: Operator
) -> Question:
    """Generates a math question with the provided operands and operator.

    Example:
        >>> question = generate_question(left_operand=5, right_operand=2, operator=Addition())
        >>> question.present()
        Question: 5 + 2 = ?
        >>> question.correct_answer()
        7
        >>> answer = question.answered_with(7)
        >>> answer.is_correct
        True
    """
    return Question(left_operand, right_operand, operator)


def present_introduction() -> None:
    print("Welcome to the Math Quiz Game!")
    print(
        "You will be presented with math problems, and you need to provide the correct answers."
    )


def get_user_input() -> int:
    return int(input("Your answer: "))


def math_quiz() -> None:
    question_set = (
        QuestionSet.of_size(5)
        .with_left_operands_from(1, to=10)
        .and_right_operands_from(1, to=5)
    )

    present_introduction()

    for question in question_set:
        question.present()
        user_input = get_user_input()

        if question.answered_with(user_input).is_correct:
            print("Correct! You earned a point.")
        else:
            print(f"Wrong answer. The correct answer is {question.correct_answer()}")

    question_set.present_results()


if __name__ == "__main__":
    math_quiz()
