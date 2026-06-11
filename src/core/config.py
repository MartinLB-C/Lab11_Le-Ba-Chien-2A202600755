"""
Lab 11 - Configuration and API key setup.
"""
import os
from pathlib import Path


_ENV_LOADED = False


def load_env_file() -> None:
    """Load local .env values without overwriting existing environment vars."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        _ENV_LOADED = True
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value

    _ENV_LOADED = True


def setup_api_key():
    """Configure Alibaba Cloud Model Studio / DashScope for the lab.

    If no API key is available, deterministic local fallback responses are used
    so guardrail tests can still run.
    """
    load_env_file()
    if not os.environ.get("DASHSCOPE_API_KEY") and os.environ.get("ALIBABA_API_KEY"):
        os.environ["DASHSCOPE_API_KEY"] = os.environ["ALIBABA_API_KEY"]
    os.environ.setdefault(
        "DASHSCOPE_BASE_URL",
        "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )
    os.environ.setdefault("ALIBABA_MODEL", "qwen-plus")
    if os.environ.get("DASHSCOPE_API_KEY"):
        print("Alibaba DashScope API key loaded.")
        return

    print("No Alibaba API key found. Using local fallback responses.")


def get_alibaba_model() -> str:
    """Return the Alibaba/Qwen model used for generation and judging."""
    load_env_file()
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
