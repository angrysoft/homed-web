"""
This type stub file was generated by pyright.
"""

from collections.abc import MutableMapping
from .db import Database
from typing import Any, Dict, Iterator, Optional

class DocumentList: ...

class Document(MutableMapping):
    """Document class"""

    def __init__(
        self, _dict: Optional[Dict[Any, Any]] = ..., **kwargs: str
    ) -> None: ...
    @property
    def db(self) -> Database:
        """Database instance"""
        ...
    @db.setter
    def db(self, db_instace: Database): ...
    @property
    def id(self) -> str:
        """Document id"""
        ...
    @id.setter
    def id(self, value: str): ...
    @property
    def rev(self) -> str:
        """Document revision"""
        ...
    @rev.setter
    def rev(self, value: str): ...
    @property
    def json(self) -> str:
        """serialized to json string"""
        ...
    def pop(self, key: str, default: Any = ...) -> Any: ...
    def popitem(self) -> Any: ...
    def store(self):
        """Store document to databse if databse instance is set else raise DocumentError"""
        ...
    def store_to_databse(self, db: Database):
        """Store document to given database instace"""
        ...
    def load_from_database(self, db: Database, doc_id: str, doc_rev: str = ...):
        """Load document from given database instance and set db as current"""
        ...
    def __str__(self) -> str: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any): ...
    def __delitem__(self, v: str) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[Any]: ...
