"""
Small compatibility layer used when google-genai/google-adk are not installed.

The lab skeleton uses Google ADK callback types. The guardrail logic itself is
provider-independent, so these minimal classes let local tests and the Alibaba
runner use the same plugin interface.
"""
from types import SimpleNamespace


class Part:
    """Minimal replacement for google.genai.types.Part."""

    def __init__(self, text: str = ""):
        self.text = text

    @classmethod
    def from_text(cls, text: str):
        """Create a text part using the same method name as google-genai."""
        return cls(text=text)


class Content:
    """Minimal replacement for google.genai.types.Content."""

    def __init__(self, role: str, parts: list | None = None):
        self.role = role
        self.parts = parts or []


class BasePlugin:
    """Minimal replacement for google.adk.plugins.base_plugin.BasePlugin."""

    def __init__(self, name: str):
        self.name = name


types = SimpleNamespace(Content=Content, Part=Part)
base_plugin = SimpleNamespace(BasePlugin=BasePlugin)
