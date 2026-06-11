# Bao cao cong viec - Hoan thanh TODO 1-13

Ngay thuc hien: 2026-06-11

## 1. Tong quan

Da hoan thanh 13 TODO cua Lab 11 va dieu chinh code de chi dung Alibaba Cloud Model Studio / DashScope. Code co local fallback de chay test khi chua dat API key.

## 2. Ho tro Alibaba API

- Them `src/core/alibaba_client.py` de goi DashScope theo OpenAI-compatible Chat Completions API bang `urllib`.
- Cap nhat `src/core/config.py`:
  - Doc `DASHSCOPE_API_KEY` hoac `ALIBABA_API_KEY`.
  - Mac dinh `DASHSCOPE_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1`.
  - Mac dinh `ALIBABA_MODEL=qwen-plus`.
- Cap nhat `src/agents/agent.py`:
  - Them `SimpleAlibabaAgent` va `SimpleAlibabaRunner`.
  - Co local fallback response de test guardrails khi khong co API key.
- Nguon tham khao Alibaba: https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope

## 3. TODO 1-13 da hoan thanh

| TODO | Noi dung | File |
|---|---|---|
| 1 | Viet 5 adversarial prompts that su | `src/attacks/attacks.py` |
| 2 | Sinh attack prompts bang Alibaba/Qwen, co fallback | `src/attacks/attacks.py` |
| 3 | Regex prompt injection detection | `src/guardrails/input_guardrails.py` |
| 4 | Topic filter cho banking/off-topic/dangerous/edge cases | `src/guardrails/input_guardrails.py` |
| 5 | InputGuardrailPlugin chan input truoc LLM | `src/guardrails/input_guardrails.py` |
| 6 | Content filter redact PII, API key, password, internal host | `src/guardrails/output_guardrails.py` |
| 7 | LLM-as-Judge da tich hop Alibaba/Qwen, co rule fallback | `src/guardrails/output_guardrails.py` |
| 8 | OutputGuardrailPlugin redact/block output | `src/guardrails/output_guardrails.py` |
| 9 | Them NeMo Colang rules cho role confusion, encoding, Vietnamese injection | `src/guardrails/nemo_guardrails.py` |
| 10 | Before/after comparison voi protected agent | `src/testing/testing.py` |
| 11 | SecurityTestPipeline run_all va calculate_metrics | `src/testing/testing.py` |
| 12 | ConfidenceRouter theo confidence va high-risk action | `src/hitl/hitl.py` |
| 13 | 3 HITL decision points cho banking | `src/hitl/hitl.py` |

## 4. Cac file moi

- `src/core/compat.py`: lightweight content/plugin types cho local Alibaba runner.
- `src/core/alibaba_client.py`: Alibaba/DashScope OpenAI-compatible HTTP client.
- `TODO_1_13_WORK_REPORT.md`: bao cao cong viec nay.

## 5. Cac lenh da kiem thu

Da chay thanh cong:

```powershell
python -m compileall src
python src\guardrails\input_guardrails.py
python src\guardrails\output_guardrails.py
python src\hitl\hitl.py
python src\main.py --part 1
python src\main.py --part 2
python src\main.py --part 3
python src\main.py --part 4
python src\testing\testing.py
```

Ket qua dang chu y:

- `main.py --part 2`: input guardrails va content filter PASS cac quick tests.
- `main.py --part 3`: protected agent block 5/5 manual attacks trong fallback comparison.
- `main.py --part 4`: confidence router route dung 5 sample cases va in 3 HITL decision points.
- NeMo duoc implement rule config, nhung local test bo qua vi may hien tai chua cai `nemoguardrails`.

## 6. Cach chay voi Alibaba API that

PowerShell:

```powershell
$env:DASHSCOPE_API_KEY="your_api_key"
$env:ALIBABA_MODEL="qwen-plus"
$env:DASHSCOPE_BASE_URL="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
python src\main.py
```

Neu API key thuoc region khac, doi `DASHSCOPE_BASE_URL` theo region Alibaba:

- Singapore: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- US Virginia: `https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- China Beijing: `https://dashscope.aliyuncs.com/compatible-mode/v1`

## 7. Luu y con lai

- Local verification da dung fallback vi moi truong hien tai khong co `DASHSCOPE_API_KEY`.
- Khi chay voi API that, ket qua model co the khac fallback; guardrails van duoc ap dung truoc/sau model.
- NeMo co the can cau hinh provider rieng tuy version package va region API.
