# Lab 11 - Guardrails, HITL & Responsible AI

Project nay trien khai Lab 11 ve guardrails, human-in-the-loop (HITL), red teaming va kiem thu an toan cho AI banking assistant.

Runtime chinh chi dung Alibaba Cloud Model Studio / DashScope. Khong con dung provider cu trong code chinh. Neu chua co `DASHSCOPE_API_KEY`, code se dung local fallback responses de van chay duoc test.

## Cau truc thu muc

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

## Cau hinh API key

File `.env` luu API key that va da nam trong `.gitignore`, khong commit file nay len Git.

Dien key vao `.env`:

```env
DASHSCOPE_API_KEY=your_real_dashscope_api_key
DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
ALIBABA_MODEL=qwen-plus
```

File `.env.example` la file mau an toan de commit.

## Tao moi truong Python

Core runtime khong can package ngoai vi goi DashScope bang Python standard library (`urllib`). `requirements.txt` duoc giu de workflow cai dat thong nhat.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

NeMo Guardrails la phan optional:

```powershell
python -m pip install -r requirements-nemo.txt
```

Neu cai `nemoguardrails` loi o package `annoy` voi thong bao can Microsoft C++ Build Tools, cai Visual C++ Build Tools roi chay lai lenh install. Cac phan chinh cua project van chay duoc neu chua cai NeMo; phan NeMo se tu skip.

## Chay project

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

Co the chay kieu module tu thu muc goc:

```powershell
python -m src.main --part 4
```

## Chay test nhanh

```powershell
python -m compileall src
python src\guardrails\input_guardrails.py
python src\guardrails\output_guardrails.py
python src\hitl\hitl.py
python src\testing\testing.py
```

## Noi dung chinh

- `src/core/alibaba_client.py`: DashScope OpenAI-compatible Chat Completions client bang `urllib`.
- `src/agents/agent.py`: unsafe/protected Alibaba-compatible agent va local fallback runner.
- `src/attacks/attacks.py`: adversarial prompts va AI red teaming bang Alibaba/Qwen.
- `src/guardrails/input_guardrails.py`: prompt injection detection, topic filter, input plugin.
- `src/guardrails/output_guardrails.py`: redact PII/secret, Alibaba/Qwen judge, output plugin.
- `src/guardrails/nemo_guardrails.py`: optional NeMo Guardrails / Colang config.
- `src/testing/testing.py`: before/after comparison va security test pipeline.
- `src/hitl/hitl.py`: confidence router va 3 HITL decision points.

## Ghi chu bao mat

- Khong commit `.env`.
- Chi commit `.env.example`.
- Neu can doi region DashScope, sua `DASHSCOPE_BASE_URL` trong `.env`.
- Neu chua co `DASHSCOPE_API_KEY`, code se in thong bao va dung local fallback responses.
