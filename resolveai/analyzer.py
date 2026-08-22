"""Takes a raw failure and transforms it into structured information for further analysis."""

#handle pattern matching
import re
from dataclasses import dataclass
from typing import Optional # fields can be missing when analyzing failures


@dataclass
#output shape of the analysis result
class AnalysisResult:
    error_type: str
    error_message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    category: str = "Unknown"


class Analyzer:
    # Analyzes raw test failures and extracts structured information.
    def analyze(self, failure_output: str) -> AnalysisResult:
        if not failure_output or not failure_output.strip():
            raise ValueError("failure_output cannot be empty")

        error_type = self._extract_error_type(failure_output)
        error_message = self._extract_error_message(failure_output)
        file_path, line_number = self._extract_location(failure_output)
        category = self._classify_error(error_type, error_message)

        return AnalysisResult(
            error_type=error_type,
            error_message=error_message,
            file_path=file_path,
            line_number=line_number,
            category=category,
        )

    # Extract the Python exception type from traceback output.
    def _extract_error_type(self, text: str) -> str:

        pattern = r"([A-Za-z_][A-Za-z0-9_]*(?:Error|Exception))(?::|$)"

        matches = re.findall(pattern, text)

        if matches:
            return matches[-1]

        return "UnknownError"
    
    # Extract the message associated with the final exception.
    def _extract_error_message(self, text: str) -> str:

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if not lines:
            return ""

        for line in reversed(lines):
            if re.search(
                r"[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception):",
                line,
            ):
                return line.split(":", 1)[1].strip()

        return lines[-1]

    # Extract the file path and line number from a traceback.
    def _extract_location(
        self,
        text: str,
    ) -> tuple[Optional[str], Optional[int]]:

        pattern = r'File "(.+?)", line (\d+)'

        matches = re.findall(pattern, text)

        if not matches:
            return None, None

        file_path, line_number = matches[-1]

        return file_path, int(line_number)

    # Classify the failure into a broad debugging category.
    def _classify_error(
        self,
        error_type: str,
        error_message: str,
    ) -> str:

        error_lower = error_message.lower()

        if error_type in {
            "SyntaxError",
            "IndentationError",
            "TabError",
        }:
            return "Syntax"

        if error_type in {
            "TypeError",
            "ValueError",
            "AttributeError",
            "IndexError",
            "KeyError",
        }:
            return "Runtime"

        if error_type == "AssertionError":
            return "Logic"

        if error_type in {
            "ImportError",
            "ModuleNotFoundError",
        }:
            return "Dependency"

        if "timeout" in error_lower:
            return "Timeout"

        return "Unknown"