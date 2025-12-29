# konnektr_graph/models.py
"""
Konnektr Graph SDK models (Azure-free)
"""
from typing import Any, List, Optional


class QueryResult:
    """Result of a query_twins call."""

    def __init__(self, value: List[Any], next_link: Optional[str] = None):
        self.value = value
        self.next_link = next_link

    @classmethod
    def from_dict(cls, data: dict):
        value = data.get("value", [])
        next_link = data.get("nextLink")
        return cls(value, next_link)
