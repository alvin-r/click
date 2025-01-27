from __future__ import annotations

import collections.abc as cabc
import textwrap
from contextlib import contextmanager


class TextWrapper(textwrap.TextWrapper):
    def _handle_long_word(
        self,
        reversed_chunks: list[str],
        cur_line: list[str],
        cur_len: int,
        width: int,
    ) -> None:
        space_left = max(width - cur_len, 1)

        if self.break_long_words:
            last = reversed_chunks[-1]
            cut = last[:space_left]
            res = last[space_left:]
            cur_line.append(cut)
            reversed_chunks[-1] = res
        elif not cur_line:
            cur_line.append(reversed_chunks.pop())

    @contextmanager
    def extra_indent(self, indent: str) -> cabc.Iterator[None]:
        old_initial_indent = self.initial_indent
        old_subsequent_indent = self.subsequent_indent
        self.initial_indent += indent
        self.subsequent_indent += indent

        try:
            yield
        finally:
            self.initial_indent = old_initial_indent
            self.subsequent_indent = old_subsequent_indent

    def indent_only(self, text: str) -> str:
        lines = text.splitlines()
        if not lines:
            return ""

        initial_indent = self.initial_indent
        subsequent_indent = self.subsequent_indent

        # Use list comprehension and join in one go for better efficiency
        indented_lines = [f"{initial_indent}{lines[0]}"] + [
            f"{subsequent_indent}{line}" for line in lines[1:]
        ]

        return "\n".join(indented_lines)
