import pytest

from resolveai.analyzer import Analyzer

#Pytest file that checks whether the analyzer is able to extract the correct structure from various failure texts

def test_analyzer_extracts_assertion_error():
    failure = """
    ============================= test session starts =============================
    ___________________________ test_addition ___________________________

    def test_addition():
        assert add(2, 2) == 5

    E       AssertionError: assert 4 == 5
    """

    analyzer = Analyzer()
    result = analyzer.analyze(failure)

    assert result.error_type == "AssertionError"
    assert result.error_message == "assert 4 == 5"
    assert result.category == "Logic"


def test_analyzer_extracts_traceback_location():
    failure = '''
    Traceback (most recent call last):
      File "calculator.py", line 15, in calculate
        result = numbers[index]
    IndexError: list index out of range
    '''

    analyzer = Analyzer()
    result = analyzer.analyze(failure)

    assert result.error_type == "IndexError"
    assert result.error_message == "list index out of range"
    assert result.file_path == "calculator.py"
    assert result.line_number == 15
    assert result.category == "Runtime"


def test_analyzer_classifies_syntax_error():
    failure = """
    File "calculator.py", line 8
        return x +
                 ^
    SyntaxError: invalid syntax
    """

    analyzer = Analyzer()
    result = analyzer.analyze(failure)

    assert result.error_type == "SyntaxError"
    assert result.category == "Syntax"


def test_analyzer_rejects_empty_input():
    analyzer = Analyzer()

    with pytest.raises(ValueError):
        analyzer.analyze("")