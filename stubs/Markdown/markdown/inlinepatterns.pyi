import re
from collections.abc import Collection
from typing import Any, ClassVar, NamedTuple
from xml.etree.ElementTree import Element

from markdown import util
from markdown.core import Markdown

def build_inlinepatterns(md: Markdown, **kwargs) -> util.Registry[Pattern]: ...

NOIMG: str
BACKTICK_RE: str
ESCAPE_RE: str
EMPHASIS_RE: str
STRONG_RE: str
SMART_STRONG_RE: str
SMART_EMPHASIS_RE: str
SMART_STRONG_EM_RE: str
EM_STRONG_RE: str
EM_STRONG2_RE: str
STRONG_EM_RE: str
STRONG_EM2_RE: str
STRONG_EM3_RE: str
LINK_RE: str
IMAGE_LINK_RE: str
REFERENCE_RE: str
IMAGE_REFERENCE_RE: str
NOT_STRONG_RE: str
AUTOLINK_RE: str
AUTOMAIL_RE: str
HTML_RE: str
ENTITY_RE: str
LINE_BREAK_RE: str

def dequote(string: str) -> str: ...

class EmStrongItem(NamedTuple):
    pattern: re.Pattern[str]
    builder: str
    tags: str

class Pattern:
    ANCESTOR_EXCLUDES: ClassVar[Collection[str]]
    pattern: str
    compiled_re: re.Pattern[str]
    md: Markdown
    def __init__(self, pattern: str, md: Markdown | None = None) -> None: ...
    def getCompiledRegExp(self) -> re.Pattern[str]: ...
    def handleMatch(self, m: re.Match[str]) -> str | Element | None: ...
    def type(self) -> str: ...
    def unescape(self, text: str) -> str: ...

class InlineProcessor(Pattern):
    safe_mode: bool
    def __init__(self, pattern: str, md: Markdown | None = None) -> None: ...
    def handleMatch(self, m: re.Match[str], data) -> tuple[Element, int, int] | tuple[None, None, None]: ...  # type: ignore[override]

class SimpleTextPattern(Pattern): ...
class SimpleTextInlineProcessor(InlineProcessor): ...
class EscapeInlineProcessor(InlineProcessor): ...

class SimpleTagPattern(Pattern):
    tag: Any
    def __init__(self, pattern: str, tag: str) -> None: ...

class SimpleTagInlineProcessor(InlineProcessor):
    tag: Any
    def __init__(self, pattern: str, tag: str) -> None: ...

class SubstituteTagPattern(SimpleTagPattern): ...
class SubstituteTagInlineProcessor(SimpleTagInlineProcessor): ...

class BacktickInlineProcessor(InlineProcessor):
    ESCAPED_BSLASH: Any
    tag: str
    def __init__(self, pattern: str) -> None: ...

class DoubleTagPattern(SimpleTagPattern): ...
class DoubleTagInlineProcessor(SimpleTagInlineProcessor): ...
class HtmlInlineProcessor(InlineProcessor): ...

class AsteriskProcessor(InlineProcessor):
    PATTERNS: ClassVar[list[EmStrongItem]]
    def build_single(self, m: re.Match[str], tag: str, idx: int) -> Element: ...
    def build_double(self, m: re.Match[str], tags: str, idx: int) -> Element: ...
    def build_double2(self, m: re.Match[str], tags: str, idx: int) -> Element: ...
    def parse_sub_patterns(self, data: str, parent: Element, last: Element | None, idx: int) -> None: ...
    def build_element(self, m: re.Match[str], builder: str, tags: str, index: int) -> Element: ...

class UnderscoreProcessor(AsteriskProcessor): ...

class LinkInlineProcessor(InlineProcessor):
    RE_LINK: ClassVar[re.Pattern[str]]
    RE_TITLE_CLEAN: ClassVar[re.Pattern[str]]
    def getLink(self, data: str, index: int): ...
    def getText(self, data: str, index: int): ...

class ImageInlineProcessor(LinkInlineProcessor): ...

class ReferenceInlineProcessor(LinkInlineProcessor):
    NEWLINE_CLEANUP_RE: ClassVar[re.Pattern[str]]
    def evalId(self, data: str, index: int, text: str): ...
    def makeTag(self, href: str, title: str, text: str) -> Element: ...

class ShortReferenceInlineProcessor(ReferenceInlineProcessor): ...
class ImageReferenceInlineProcessor(ReferenceInlineProcessor): ...
class AutolinkInlineProcessor(InlineProcessor): ...
class AutomailInlineProcessor(InlineProcessor): ...
