# Lab 11 - Guardrails, HITL & Responsible AI

Project này triển khai bài Lab 11 về guardrails, human-in-the-loop (HITL), red teaming và kiểm thử an toàn cho AI banking assistant. Code mặc định dùng Alibaba Cloud Model Studio / DashScope, có fallback local để vẫn chạy được khi chưa có API key.

## Cấu trúc thư mục

```text
.
├── notebooks/
│   ├── attack_defense_arena.ipynb
│   └── lab11_guardrails_hitl.ipynb
├── src/
│   ├── main.py
│   ├── agents/
│   ├── attacks/
│   ├── core/
│   ├── guardrails/
│   ├── hitl/
│   └── testing/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-nemo.txt
└── README.md
```

## File môi trường

File `.env` dùng để lưu API key thật và đã được đưa vào `.gitignore`, không commit file này lên Git.

Điền key vào `.env`:

```env
DASHSCOPE_API_KEY=your_real_dashscope_api_key
DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
ALIBABA_MODEL=qwen-plus
```

File `.env.example` là file mẫu an toàn để commit.

## Tạo môi trường Python

Khuyến nghị dùng Python 3.11 vì một số dependency của NeMo Guardrails cần package native.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

NeMo Guardrails là phần optional:

```powershell
python -m pip install -r requirements-nemo.txt
```

Nếu cài `nemoguardrails` lỗi ở package `annoy` với thông báo cần Microsoft C++ Build Tools, cài Visual C++ Build Tools rồi chạy lại lệnh install. Các phần chính của project vẫn chạy được nếu chưa cài NeMo; phần NeMo sẽ tự skip.

## Chạy project

Chạy toàn bộ lab:

```powershell
python src\main.py
```

Chạy từng phần:

```powershell
python src\main.py --part 1
python src\main.py --part 2
python src\main.py --part 3
python src\main.py --part 4
```

Có thể chạy kiểu module từ thư mục gốc:

```powershell
python -m src.main --part 4
```

## Chạy test nhanh

```powershell
python -m compileall src
python src\guardrails\input_guardrails.py
python src\guardrails\output_guardrails.py
python src\hitl\hitl.py
python src\testing\testing.py
```

## Nội dung chính

- `src/attacks/attacks.py`: 5 adversarial prompts và AI red teaming.
- `src/guardrails/input_guardrails.py`: phát hiện prompt injection, lọc topic, input guardrail plugin.
- `src/guardrails/output_guardrails.py`: redact PII/secret, LLM-as-Judge, output guardrail plugin.
- `src/guardrails/nemo_guardrails.py`: cấu hình NeMo Guardrails / Colang.
- `src/testing/testing.py`: before/after comparison và security test pipeline.
- `src/hitl/hitl.py`: confidence router và 3 HITL decision points.

## Ghi chú bảo mật

- Không commit `.env`.
- Chỉ commit `.env.example`.
- Nếu cần đổi region DashScope, sửa `DASHSCOPE_BASE_URL` trong `.env`.
- Nếu chưa có `DASHSCOPE_API_KEY`, code sẽ in thông báo và dùng local fallback responses.
