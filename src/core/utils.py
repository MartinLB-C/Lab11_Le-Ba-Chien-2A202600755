"""
Lab 11 - Helper utilities.
"""
from core.compat import types


def extract_text_from_content(content) -> str:
    """Extract all text parts from a Content-like object."""
    text = ""
    if content and getattr(content, "parts", None):
        for part in content.parts:
            if hasattr(part, "text") and part.text:
                text += part.text
    return text


def make_content(role: str, text: str):
    """Create a lightweight Content object for the local Alibaba runner."""
    return types.Content(role=role, parts=[types.Part.from_text(text=text)])


async def chat_with_agent(agent, runner, user_message: str, session_id=None):
    """Send a message to the local Alibaba runner.

    Args:
        agent: The agent instance.
        runner: SimpleAlibabaRunner.
        user_message: Plain text message to send.
        session_id: Kept for backward-compatible call sites.

    Returns:
        Tuple of (response_text, session).
    """
    if hasattr(runner, "chat"):
        response = await runner.chat(user_message, user_id="student")
        return response, None

    user_id = "student"
    app_name = runner.app_name

    session = None
    if session_id is not None:
        try:
            session = await runner.session_service.get_session(
                app_name=app_name, user_id=user_id, session_id=session_id
            )
        except (ValueError, KeyError):
            pass

    if session is None:
        session = await runner.session_service.create_session(
            app_name=app_name, user_id=user_id
        )

    content = make_content(role="user", text=user_message)

    final_response = ""
    async for event in runner.run_async(
        user_id=user_id, session_id=session.id, new_message=content
    ):
        if hasattr(event, "content") and event.content and event.content.parts:
            final_response += extract_text_from_content(event.content)

    return final_response, session
