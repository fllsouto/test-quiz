import pytest
from model import Question

@pytest.fixture
def question():
    return Question(title='q1')

@pytest.fixture
def question_with_choices(question):
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)
    return question

# t1: create question with valid title
def test_create_question():
    question = Question(title='q1')
    assert question.id != None

# t2: create multiple questions with unique ids
def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

# t3: create question with invalid title
def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

# t4: create question with valid points
def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

# t5: create choice for question
def test_create_choice(question):
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# t6: create question with invalid points
def test_create_question_with_invalid_points():
    error_message = "Points must be between 1 and 100"

    with pytest.raises(Exception) as exc:
        Question("q1", points=0)
    assert error_message in str(exc.value)

    with pytest.raises(Exception) as exc:
        Question("q1", points=101)
    assert error_message in str(exc.value)

# t7: create choice with invalid text size |a| < |text| < |b|
def test_create_choice_with_invalid_text_size(question):
    message_a = ""
    message_b = "a"*101
    error_message_a = 'Text cannot be empty'
    error_message_b = 'Text cannot be longer than 100 characters'

    with pytest.raises(Exception) as exc:
        question.add_choice(message_a, False)
    assert error_message_a in str(exc.value)

    with pytest.raises(Exception) as exc:
        question.add_choice(message_b, False)
    assert error_message_b in str(exc.value)

# t8: create question with multiple choices
def test_create_question_with_multiple_questions(question):
    choice_list = [
        ('a', False),
        ('b', False),
        ('c', False),
        ('d', False),
        ('e', False),
    ]

    for choice in choice_list:
        question.add_choice(choice[0], choice[1])

    assert len(question.choices) == len(choice_list)

# t9: selected one choice in unique select question
def test_correct_one_selected_choice():
    question = Question(title='q1', max_selections=1)
    correct_choices = []
    question.add_choice('a', False)
    correct_choices.append(question.add_choice('b', True).id)
    question.add_choice('c', False)
    
    selected_choices = question.correct_selected_choices(correct_choices)
    assert len(selected_choices) == len(correct_choices)
    assert correct_choices[0] in selected_choices

# t10: selected more choices than max selection
def test_select_more_choices_than_max_selections():
    MAX_SELECTIONS = 1
    error_message = f"Cannot select more than {MAX_SELECTIONS} choices"
    question = Question(title='q1', max_selections=MAX_SELECTIONS)
    correct_choices = []
    question.add_choice('a', False)
    correct_choices.append(question.add_choice('b', True).id)
    correct_choices.append(question.add_choice('c', True).id)

    with pytest.raises(Exception) as exc:
        question.correct_selected_choices(correct_choices)

    assert error_message in str(exc.value)

# t11: selected more choices in multi select question
def test_select_more_choices_in_multi_select_question():
    MAX_SELECTIONS = 3
    question = Question(title='q1', max_selections=MAX_SELECTIONS)
    correct_choices = []
    question.add_choice('a', False)
    correct_choices.append(question.add_choice('b', True).id)
    correct_choices.append(question.add_choice('c', True).id)

    selected_correct_choices = question.correct_selected_choices(correct_choices)

    assert len(selected_correct_choices) == len(correct_choices)
    for correct_choice in correct_choices:
        assert correct_choice in selected_correct_choices

# t12: remove all choices from question
def test_remove_all_choices_from_question(question_with_choices):
    question_with_choices.remove_all_choices()

    assert len(question_with_choices.choices) == 0


# t13: set one correct choice for question
def test_set_correct_choice_for_question():
    correct_choices_to_set = []
    question = Question(title='q1', max_selections=2)
    question.add_choice('a', False)
    question.add_choice('b', False)
    correct_choices_to_set.append(question.add_choice('c', False).id)

    question.set_correct_choices(correct_choices_to_set)
    
    selected_correct_choices = question.correct_selected_choices(correct_choices_to_set)

    assert len(selected_correct_choices) == len(correct_choices_to_set)
    for correct_choice in correct_choices_to_set:
        assert correct_choice in selected_correct_choices


# t14: set wrong correct choice for questions
def test_set_wrong_correct_choice_for_questions(question):
    mapped_choice_id = question.add_choice('a', False).id
    unmaped_choice_id = 99
    error_message = f'Invalid choice id {unmaped_choice_id}'

    with pytest.raises(Exception) as exc:
        question.set_correct_choices([mapped_choice_id, unmaped_choice_id])

    assert error_message in str(exc.value)

# t15: remove choice by id
def test_remove_choice_by_id(question):
    question.add_choice('a', False)
    removed_choice_id = question.add_choice('b', False).id
    question.add_choice('c', False)

    question.remove_choice_by_id(removed_choice_id)
    remain_choices_id = [choice.id for choice in question.choices]
    assert len(remain_choices_id) == 2
    assert removed_choice_id not in remain_choices_id