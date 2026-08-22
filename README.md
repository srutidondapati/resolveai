# ResolveAI

AI-powered debugging assistant that analyzes code, generates fixes, and verifies them through automated testing.

### Project Setup
- Created the initial ResolveAI Python project structure with separate modules for the LLM interface, static code analysis, retrieval, testing, and agent orchestration.
- Configured a Python 3.10 virtual environment and installed the initial development dependencies: OpenAI, python-dotenv, and pytest.
- Added a Python-specific .gitignore to prevent virtual environments, cached files, test artifacts, and environment variables from being committed.
- Set up Git/GitHub for version control and established the initial project structure and documentation.
- Planned a modular debugging pipeline in which AI-generated fixes will eventually be validated through automated testing rather than trusted blindly.

---

### Analyzer
- Created an Analyzer (analyzer.py) module using Python dataclasses and regex expressions to transform raw test failures and tracebacks into structured information for further analysis.
- The analyzer extracts and classifies key debugging information:
  - error_type: The type of exception raised (e.g., AssertionError, IndexError, SyntaxError)
  - error_message: The specific error message associated with the failure
  - file_path: The file where the failure occurred, when available
  - line_number: The line where the failure occurred, when available
  - category: A broad classification of the failure, such as Syntax, Runtime, Logic, Dependency, or Timeout
- Added unit tests (analyzer_test.py) to verify error extraction, traceback location parsing, error classification, and input validation.
