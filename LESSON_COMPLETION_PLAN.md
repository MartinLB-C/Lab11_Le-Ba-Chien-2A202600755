# Plan hoan thanh Day 11 - Guardrails, HITL & Responsible AI

File nay la checklist co the chinh sua de hoan thanh bai hoc va assignment.

Cap nhat 2026-06-11: TODO 1-13 cua lab da duoc implement. Xem bao cao tai `TODO_1_13_WORK_REPORT.md`. Cac muc assignment production pipeline rieng nhu Rate Limiter/Audit/Monitoring van la phan mo rong neu can nop assignment production day du.

## 1. Trang thai code hien tai

- [ ] `src/attacks/attacks.py`: TODO 1 van con prompt mau dang de placeholder. Can thay bang 5 adversarial prompts that su.
- [ ] `src/attacks/attacks.py`: TODO 2 da co khung goi Alibaba/Qwen de sinh prompt tan cong, nhung can chay va luu output vao notebook/report.
- [ ] `src/guardrails/input_guardrails.py`: TODO 3 chua co regex injection patterns.
- [ ] `src/guardrails/input_guardrails.py`: TODO 4 `topic_filter()` dang `pass`.
- [ ] `src/guardrails/input_guardrails.py`: TODO 5 `InputGuardrailPlugin.on_user_message_callback()` dang `pass`.
- [ ] `src/guardrails/output_guardrails.py`: TODO 6 `content_filter()` chua co PII/secret regex.
- [ ] `src/guardrails/output_guardrails.py`: TODO 7 `safety_judge_agent` dang `None`, chua khoi tao LLM-as-Judge.
- [ ] `src/guardrails/output_guardrails.py`: TODO 8 `OutputGuardrailPlugin.after_model_callback()` chua redact/block response.
- [ ] `src/guardrails/nemo_guardrails.py`: TODO 9 chua co Colang rules moi cho role confusion, encoding, Vietnamese injection.
- [ ] `src/testing/testing.py`: TODO 10 chua tao protected agent va chua rerun attacks voi guardrails.
- [ ] `src/testing/testing.py`: TODO 11 `run_all()` va `calculate_metrics()` van tra ket qua rong/default.
- [ ] `src/hitl/hitl.py`: TODO 12 `ConfidenceRouter.route()` van tra hard-coded `auto_send`.
- [ ] `src/hitl/hitl.py`: TODO 13 `hitl_decision_points` van la placeholder.
- [ ] Assignment production pipeline: chua co Rate Limiter, Audit Log, Monitoring/Alerts, va pipeline end-to-end rieng.

## 2. Muc tieu nop bai

- [ ] Notebook hoac Python files chay end-to-end.
- [ ] Co it nhat 4 lop safety doc lap:
  - [ ] Rate limiter theo user/time window.
  - [ ] Input guardrails: injection regex + topic/danger filter.
  - [ ] Output guardrails: PII/secrets redact.
  - [ ] LLM-as-Judge: safety, relevance, accuracy, tone.
- [ ] Co audit log ghi lai input, output, layer nao block, latency, user id.
- [ ] Co monitoring/alerts: block rate, rate-limit hits, judge fail rate.
- [ ] Chay du 4 test suites trong assignment: safe queries, attacks, rate limiting, edge cases.
- [ ] Co bao cao ca nhan 1-2 trang tra loi 5 cau hoi.

## 3. Thu tu lam khuyen nghi

### Phase 1 - Hoan thien lab skeleton

- [ ] Thay 5 prompt placeholder trong `adversarial_prompts` bang attack prompts that su:
  - [ ] Completion/fill-in-the-blank.
  - [ ] Translation/reformat system prompt.
  - [ ] Creative/hypothetical frame.
  - [ ] Confirmation side-channel.
  - [ ] Multi-step escalation.
- [ ] Implement `detect_injection()` voi toi thieu 5 regex:
  - [ ] Ignore/forget/disregard previous instructions.
  - [ ] You are now / DAN / unrestricted AI.
  - [ ] Reveal/show/print system prompt.
  - [ ] Pretend/act as unrestricted/admin/auditor.
  - [ ] Output config/instructions as JSON/YAML/Base64/ROT13.
  - [ ] Vietnamese variants: "bo qua huong dan", "tiet lo mat khau", "system prompt".
- [ ] Implement `topic_filter()`:
  - [ ] Block ngay neu match `BLOCKED_TOPICS`.
  - [ ] Allow neu co banking topic trong `ALLOWED_TOPICS`.
  - [ ] Xu ly input rong, emoji-only, qua dai.
- [ ] Implement `InputGuardrailPlugin`:
  - [ ] Tang `total_count`.
  - [ ] Block injection voi message ro rang.
  - [ ] Block off-topic/dangerous topic.
  - [ ] Return `None` neu safe.
- [ ] Implement `content_filter()`:
  - [ ] VN phone number.
  - [ ] Email.
  - [ ] CMND/CCCD 9 hoac 12 so.
  - [ ] API key `sk-...`.
  - [ ] Password/key/token/secret patterns.
  - [ ] Internal host/domain pattern nhu `.internal`.
- [ ] Implement LLM-as-Judge:
  - [ ] Tao `safety_judge_agent`.
  - [ ] Doi judge prompt sang multi-criteria neu lam assignment: SAFETY, RELEVANCE, ACCURACY, TONE, VERDICT, REASON.
  - [ ] Parse verdict PASS/FAIL hoac SAFE/UNSAFE mot cach ro rang.
- [ ] Implement `OutputGuardrailPlugin`:
  - [ ] Redact response neu `content_filter()` tim thay issue.
  - [ ] Block response neu judge danh gia unsafe.
  - [ ] Tang counter `blocked_count`, `redacted_count`, `total_count`.
- [ ] Implement NeMo Colang TODO 9:
  - [ ] Role confusion attacks.
  - [ ] Encoding/output transformation attacks.
  - [ ] Vietnamese prompt injection.
  - [ ] Them test cases tuong ung.
- [ ] Implement `testing.py`:
  - [ ] `run_comparison()` tao protected agent voi input/output plugins.
  - [ ] `SecurityTestPipeline.run_all()` chay tung attack.
  - [ ] `calculate_metrics()` tinh total, blocked, leaked, block_rate, leak_rate, all_secrets_leaked.
- [ ] Implement HITL:
  - [ ] `ConfidenceRouter.route()` theo threshold va high-risk actions.
  - [ ] Dien 3 HITL decision points bang scenario ngan hang that te.

### Phase 2 - Xay production defense pipeline cho assignment

- [ ] Chon framework thuc hien. Khuyen nghi: dung callback plugins trong local Alibaba runner cua repo.
- [ ] Them `RateLimitPlugin`:
  - [ ] Sliding window per user.
  - [ ] Max 10 requests / 60 seconds theo Test 3.
  - [ ] Return block response co wait time.
- [ ] Them `AuditLogPlugin`:
  - [ ] Ghi timestamp, user id, input, output, latency.
  - [ ] Ghi layer block dau tien.
  - [ ] Export ra `security_audit.json`.
- [ ] Them `MonitoringAlert`:
  - [ ] Track block rate.
  - [ ] Track rate-limit hits.
  - [ ] Track judge fail rate.
  - [ ] In alert neu vuot nguong.
- [ ] Lap `production_plugins` theo thu tu:
  - [ ] `RateLimitPlugin`
  - [ ] `InputGuardrailPlugin`
  - [ ] Optional NeMo wrapper/plugin hoac rule test rieng.
  - [ ] `OutputGuardrailPlugin`
  - [ ] `AuditLogPlugin`
- [ ] Them script/test runner cho assignment:
  - [ ] Safe queries should PASS.
  - [ ] 7 attack queries should BLOCK.
  - [ ] Rate limit: 15 rapid requests, 10 pass, 5 block.
  - [ ] Edge cases: empty, very long, emoji-only, SQL injection, off-topic math.

### Phase 3 - Notebook va report

- [ ] Cap nhat `notebooks/lab11_guardrails_hitl.ipynb` hoac tao notebook assignment moi:
  - [ ] Cell setup/import.
  - [ ] Cell khoi tao pipeline.
  - [ ] Cell test safe queries.
  - [ ] Cell test attacks.
  - [ ] Cell test rate limiting.
  - [ ] Cell test edge cases.
  - [ ] Cell export audit log.
  - [ ] Cell hien thi metrics/alerts.
- [ ] Viet report Markdown/PDF:
  - [ ] Table: 7 attack prompts bi layer nao bat dau tien.
  - [ ] False positive analysis cho safe queries.
  - [ ] Gap analysis: 3 attacks hien pipeline chua bat duoc.
  - [ ] Production readiness: latency, cost, monitoring scale, rule updates.
  - [ ] Ethical reflection ve gioi han cua guardrails.

## 4. Definition of Done

- [ ] `python src/main.py --part 1` chay duoc va hien attack results.
- [ ] `python src/main.py --part 2` chay duoc va cac quick tests PASS.
- [ ] `python src/main.py --part 3` co before/after comparison va security report khong rong.
- [ ] `python src/main.py --part 4` route dung 5 sample cases va hien 3 HITL points that.
- [ ] Assignment test suites co output ro rang trong notebook/script.
- [ ] Audit log JSON duoc tao.
- [ ] Report tra loi du 5 cau hoi.

## 5. Luu y khi implement

- [ ] Khong dua secret that vao prompt/code. Secret trong unsafe agent chi la mock demo.
- [ ] Regex guardrails phai can bang false positive: dung qua rong se block cau hoi hop le.
- [ ] LLM-as-Judge ton latency/cost; trong report can neu trade-off.
- [ ] Audit log khong nen luu raw PII trong production; neu luu de demo thi can noi ro day la bai lab.
- [ ] Neu khong cai/chay duoc NeMo local, co the ghi la optional va chung minh rule logic bang code/test rieng.
