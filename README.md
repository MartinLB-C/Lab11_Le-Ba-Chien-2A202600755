# Lab 11 - Guardrails, HITL & Responsible AI

Du an nay trien khai Lab 11 ve guardrails, human-in-the-loop (HITL), red teaming va kiem thu an toan cho AI banking assistant.

Runtime chinh chi dung Alibaba Cloud Model Studio / DashScope. Code khong phu thuoc provider khac trong luong chinh. Neu chua co `DASHSCOPE_API_KEY`, project se dung local fallback responses de van chay duoc demo va test.

## 1. Cau truc thu muc

```text
.
|-- notebooks/
|   |-- attack_defense_arena.ipynb
|   `-- lab11_guardrails_hitl.ipynb
|-- src/
|   |-- main.py
|   |-- agents/
|   |-- attacks/
|   |-- core/
|   |-- guardrails/
|   |-- hitl/
|   `-- testing/
|-- .env
|-- .env.example
|-- .gitignore
|-- requirements.txt
|-- requirements-nemo.txt
`-- README.md
```

## 2. Cau hinh API key

File `.env` dung de luu API key that. File nay da nam trong `.gitignore`, khong commit len Git.

Noi dung `.env`:

```env
DASHSCOPE_API_KEY=your_real_dashscope_api_key
DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
ALIBABA_MODEL=qwen-plus
```

File `.env.example` la file mau an toan de commit.

## 3. Tao moi truong Python

Khuyen nghi dung Python 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Core runtime hien chi dung Python standard library de goi DashScope bang `urllib`, nen `requirements.txt` khong can package ngoai. File nay duoc giu lai de workflow cai dat thong nhat.

NeMo Guardrails la optional:

```powershell
python -m pip install -r requirements-nemo.txt
```

Neu cai NeMo loi o package `annoy` voi thong bao can Microsoft C++ Build Tools, cai Visual C++ Build Tools roi chay lai lenh install. Neu chua cai NeMo, phan NeMo se tu skip; cac phan chinh van chay binh thuong.

## 4. Chay project

Chay toan bo lab:

```powershell
python src\main.py
```

Chay tung phan:

```powershell
python src\main.py --part 1
python src\main.py --part 2
python src\main.py --part 3
python src\main.py --part 4
```

Co the chay theo module tu thu muc goc:

```powershell
python -m src.main --part 4
```

## 5. Chay test nhanh

```powershell
python -m compileall src
python src\guardrails\input_guardrails.py
python src\guardrails\output_guardrails.py
python src\hitl\hitl.py
python src\testing\testing.py
```

## 6. Notebook

Hai notebook trong `notebooks/` da duoc chuyen sang dung code Alibaba/DashScope trong `src/`.

```text
notebooks/lab11_guardrails_hitl.ipynb
notebooks/attack_defense_arena.ipynb
```

Khi mo notebook, chay cell setup dau tien de them `src/` vao `sys.path`, sau do chay cac cell theo thu tu.

## 7. Cac file chinh

- `src/core/alibaba_client.py`: DashScope OpenAI-compatible Chat Completions client bang `urllib`.
- `src/core/config.py`: doc `.env`, cau hinh `DASHSCOPE_API_KEY`, `DASHSCOPE_BASE_URL`, `ALIBABA_MODEL`.
- `src/agents/agent.py`: unsafe/protected Alibaba-compatible agent va local fallback runner.
- `src/attacks/attacks.py`: manual adversarial prompts va AI red teaming bang Alibaba/Qwen.
- `src/guardrails/input_guardrails.py`: prompt injection detection, topic filter, input guardrail plugin.
- `src/guardrails/output_guardrails.py`: redact PII/secret, Alibaba/Qwen safety judge, output guardrail plugin.
- `src/guardrails/nemo_guardrails.py`: optional NeMo Guardrails / Colang config.
- `src/testing/testing.py`: before/after comparison va automated security test pipeline.
- `src/hitl/hitl.py`: confidence router va 3 HITL decision points.

## 8. Ghi chu bao mat

- Khong commit `.env`.
- Chi commit `.env.example`.
- Khong ghi API key truc tiep vao code, notebook, README hoac report.
- Neu can doi region DashScope, sua `DASHSCOPE_BASE_URL` trong `.env`.
- Neu chua co `DASHSCOPE_API_KEY`, code se in thong bao va dung local fallback responses.

## 9. Troubleshooting

Neu chay project va thay:

```text
No Alibaba API key found. Using local fallback responses.
```

Nghia la `.env` chua co `DASHSCOPE_API_KEY` hoac key dang rong.

Neu PowerShell chan activate virtualenv:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Neu muon kiem tra `.env` co bi Git ignore khong:

```powershell
git check-ignore -v .env
```
