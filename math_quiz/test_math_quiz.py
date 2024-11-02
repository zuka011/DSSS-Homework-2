from pytest import mark
from hypothesis import given, assume, example, settings
from hypothesis.strategies import integers, data


from math_quiz import (
    random_integer_from,
    random_operator,
    generate_question,
    Operator,
    Addition,
    Subtraction,
    Multiplication,
)


@given(min_val=integers(), max_val=integers())
@example(min_val=1, max_val=10)
@example(min_val=5, max_val=5)
def test_should_generate_a_random_integer_within_the_specified_range(
    min_val: int, max_val: int
) -> None:
    assume(min_val <= max_val)  # Ensure our min_val, max_val range is valid

    random_number = random_integer_from(min_val, to=max_val)
    assert min_val <= random_number <= max_val


@given(data())
@settings(max_examples=20)
def test_should_generate_a_valid_random_operator(_) -> None:
    assert random_operator().stringify() in {"+", "-", "*"}


@mark.parametrize(
    [
        "left_operand",
        "right_operand",
        "operator",
        "expected_question",
        "expected_answer",
    ],
    [
        (5, 2, Addition(), "5 + 2", 7),
        (5, 2, Subtraction(), "5 - 2", 3),
        (5, 2, Multiplication(), "5 * 2", 10),
    ],
)
def test_should_generate_a_question_with_the_provided_operands_and_operator(
    left_operand: int,
    right_operand: int,
    operator: Operator,
    expected_question: str,
    expected_answer: int,
) -> None:
    question = generate_question(
        left_operand=left_operand, right_operand=right_operand, operator=operator
    )

    assert question.formatted() == expected_question
    assert question.correct_answer() == expected_answer
