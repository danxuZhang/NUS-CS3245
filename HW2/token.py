import sortedlist

class Token:
    def __init__(self, term: str, posting_id=-1):
        self._term = term
        self._posting_id = posting_id
        self._doc_freq = 0

    def set_posting_id(self, posting_id: SortedList) -> None:
        self._posting_id = posting_id

    def increment_freq_by_one(self):
        self._doc_freq += 1

    def get_term(self) -> str:
        return self._term

    def get_doc_freq(self) -> int:
        return self._doc_freq

    def get_posting_id(self) -> int:
        return self._posting_id

    def __str__(self) -> str:
        return f"({self._term}, freq:{self._doc_freq}, {self._posting_id})"
