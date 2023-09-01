from abc import ABC
from typing import Dict, Iterable, List, Optional, Union

import sgqlc


class AiApiBase(ABC):
    _resource: str = None
    BASE_FIELDS: List[str] = []
    EXTRA_FIELDS: List[str] = []

    def __init__(self, organization_id: Optional[int] = None, user_id: Optional[int] = None):
        from .session import MetaAISession

        self.ai_session = MetaAISession(organization_id=organization_id, owner_id=user_id)

    @property
    def resource(self) -> str:
        return self._resource

    @classmethod
    def _fields(cls, verbose: bool) -> List[str]:
        return cls.BASE_FIELDS + cls.EXTRA_FIELDS if verbose else cls.BASE_FIELDS

    @staticmethod
    def _output_formatter(
        entries: Union[Iterable[sgqlc.types.Type], sgqlc.types.Type], to_json: bool, snake_case: bool = True
    ) -> Union[List[sgqlc.types.Type], List[Dict], sgqlc.types.Type, Dict]:
        """Format the output to either json or sgqlc type"""

        def transform_snake_case(entry: sgqlc.types.Type) -> Dict:
            """Some GraphQL types are stored as camelCase, this function converts them to snake_case for SDK consistency"""
            # Use internal represention of SGQLC type which is stored as snake_case
            return {k: entry[k] for k in entry}

        if not to_json:
            return entries

        if isinstance(entries, (list, tuple)):
            if snake_case:
                formatted_entries = [transform_snake_case(entry) for entry in entries]
            else:
                formatted_entries = [entry.__json_data__ for entry in entries]
        else:
            if snake_case:
                formatted_entries = transform_snake_case(entries)
            else:
                formatted_entries = entries.__json_data__  # single instance
        return formatted_entries
