from abc import ABC


class Normalizer(ABC):

    def period(self, text: str) -> str: ...

    def normalize_date(self, text: str) -> str: ...