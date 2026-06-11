"""
Lab 11 - Configuration and API key setup.
"""
import os


def setup_api_key():
    """Configure the selected LLM provider for the lab.

    The original lab used Gemini through Google ADK. This version defaults to
    Alibaba Cloud Model Studio / DashScope because the assignment is being run
    with an Alibaba API key. If no API key is available, deterministic local
    fallback responses are used so guardrail tests can still run.
    """
    provider = get_ai_provider()
    if provider == "alibaba":
        if "DASHSCOPE_API_KEY" not in os.environ and "ALIBABA_API_KEY" in os.environ:
            os.environ["DASHSCOPE_API_KEY"] = os.environ["ALIBABA_API_KEY"]
        os.environ.setdefault(
            "DASHSCOPE_BASE_URL",
            "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
        os.environ.setdefault("ALIBABA_MODEL", "qwen-plus")
        if "DASHSCOPE_API_KEY" in os.environ:
            print("Alibaba DashScope API key loaded.")
        else:
            print("No Alibaba API key found. Using local fallback responses.")
        return

    if provider == "google":
        if "GOOGLE_API_KEY" not in os.environ:
            print("GOOGLE_API_KEY not found. Google ADK calls may fail.")
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "0"
        print("Google provider selected.")
        return

    raise ValueError(f"Unsupported AI_PROVIDER: {provider}")


def get_ai_provider() -> str:
    """Return the configured LLM provider name."""
    return os.getenv("AI_PROVIDER", "alibaba").lower()


def get_alibaba_model() -> str:
    """Return the Alibaba/Qwen model used for generation and judging."""
    return os.getenv("ALIBABA_MODEL", "qwen-plus")


# Allowed banking topics used by topic_filter. The list contains English,
# Vietnamese with accents, and Vietnamese without accents for terminal input.
ALLOWED_TOPICS = [
    "banking", "bank", "vinbank", "account", "transaction", "transfer",
    "loan", "interest", "savings", "credit", "deposit", "withdrawal",
    "balance", "payment", "card", "atm", "limit", "joint account",
    "money", "vnd", "rate", "finance", "financial",
    "tai khoan", "tai khoản", "giao dich", "giao dịch",
    "tiet kiem", "tiết kiệm", "lai suat", "lãi suất",
    "chuyen tien", "chuyển tiền", "the tin dung", "thẻ tín dụng",
    "so du", "số dư", "vay", "ngan hang", "ngân hàng",
    "rut tien", "rút tiền", "nap tien", "nạp tiền",
]


# Blocked topics that should be rejected even if a banking word is present.
BLOCKED_TOPICS = [
    "hack", "exploit", "weapon", "drug", "illegal", "violence", "gambling",
    "bomb", "kill", "steal", "malware", "phishing", "credential stuffing",
    "sql injection", "select * from", "drop table", "bypass", "admin password",
    "api key", "secret key", "database connection string", "system prompt",
    "mat khau admin", "mật khẩu admin", "khoa api", "khóa api",
]
