from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..main import ReviewCode

def validator(state: ReviewCode):
    """
    Validates the scanned codebase against the generated review plan.
    """
    review_plan = state["review_plan"]
    scanned_files = state.get("scanned_files", [])

    if not scanned_files:
        return {
            **state,
            "validation_result": {
                "valid": False,
                "message": "No files were scanned from the project."
            }
        }
    if not review_plan:
        return {
            **state,
            "validation_result": {
                "valid": False,
                "message": "No review plan was generated."
            }
        }
    # Basic validation checks
    required_sections = [
        "security",
        "bugs",
        "performance",
        "code_quality"
    ]
    missing_sections = []

    # if review_plan directory
    if isinstance(review_plan, dict):
        for section in required_sections:
            if section not in review_plan:
                missing_sections.append(section)

    validation_result = {
        "valid": len(missing_sections) == 0,
        "files_scanned": len(scanned_files),
        "missing_sections": missing_sections,
    }

    return {
        **state,
        "validation_result": validation_result
    }