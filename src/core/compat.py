"""Small content/plugin compatibility layer for the Alibaba-only runner."""
from types import SimpleNamespace


class Part:
    """Minimal text part."""

    def __init__(self, text: str = ""):
        self.text = text

    @classmethod
    def from_text(cls, text: str):
        """Create a text part."""
        return cls(text=text)


class Content:
    """Minimal chat content container."""

    def __init__(self, role: str, parts: list | None = None):
        self.role = role
        self.parts = parts or []


class BasePlugin:
    """Minimal base plugin used by the local runner callbacks."""

    def __init__(self, name: str):
        self.name = name


types = SimpleNamespace(Content=Content, Part=Part)
base_plugin = SimpleNamespace(BasePlugin=BasePlugin)
