# Bug Fix Note

Context: switched translation direction to "any language -> Vietnamese" using the
Tencent Hy-MT2-1.8B GGUF model, then verified output quality on this Windows
machine. Three issues blocked the model from loading/running and were fixed.

## 1. huggingface_hub 1.x removed `configure_http_backend`

Symptom:
`ImportError: cannot import name ''configure_http_backend'' from ''huggingface_hub''`
during first-run model download.

Root cause:
huggingface_hub >= 1.0 (installed: 1.18.0) migrated its HTTP layer from
`requests` to `httpx`. The old `configure_http_backend(backend_factory=...)`
API was replaced by `huggingface_hub.utils.set_client_factory(...)`, which
expects a factory returning an `httpx.Client`.

Fix (translator.py):
Added `_configure_no_proxy_backend()` that tries the new httpx-based
`set_client_factory` first and falls back to the legacy
`configure_http_backend` for older versions. `_download_model` now calls this
helper instead of importing the removed symbol directly.

## 2. hf-mirror.com endpoint breaks downloads on huggingface_hub 1.x

Symptom:
`FileMetadataError` / `LocalEntryNotFoundError` even though the file (1.13 GB)
was reachable and HEAD returned HTTP 200.

Root cause:
translator.py hard-coded `HF_ENDPOINT=https://hf-mirror.com`. That mirror
returns a 308 redirect back to huggingface.co but drops the `x-repo-commit`
header. huggingface_hub 1.x requires `x-repo-commit` to validate file metadata,
so the download aborted. The official `huggingface.co` endpoint returns 302
with `x-repo-commit` present and works correctly from this network.

Fix (translator.py):
Default `HF_ENDPOINT` to `https://huggingface.co`, but still honor a
user-provided `HF_ENDPOINT` from the environment (so a mirror can be opted into
when needed). No-proxy env vars left in place.

## 3. test_llama_cpp.py: console encoding + stale wait condition

Symptoms:
- `UnicodeEncodeError: ''charmap'' codec can''t encode character ''\u1ea1''`
  (Vietnamese "a" with dot below) when printing translations on the default
  Windows cp1252 console.
- Potential infinite wait: the init loop checked for the Chinese substring
  "失败" in the status, but failure status messages are now English.

Fixes (test_llama_cpp.py):
- Force `sys.stdout`/`sys.stderr` to UTF-8 via `reconfigure(encoding="utf-8")`.
- Change the wait/abort condition to match the English token `"Failed"`.
- Updated `test_cases` to the "-> Vietnamese" direction and added Japanese and
  French source samples.

## Verification

`python test_llama_cpp.py` ran end to end (RC=0). Sample output:

```
Hello, how are you?              -> Xin chao, ban khoe khong?
今天天气真好                       -> Hom nay thoi tiet that tuyet.
This is a test sentence.         -> Day la mot cau thu nghiem.
我喜欢编程                         -> Toi thich lap trinh.
人工知能はとても面白いです。          -> Tri tue nhan tao that thu vi.
The quick brown fox ...          -> Con cao nau nhanh nhen nhay qua con cho luoi.
```

(Above transliterated without diacritics for ASCII safety; actual output is
fully accented Vietnamese.) Inference ~28 tokens/s on CPU, model load ~0.2s.

Environment: Windows, Python 3.13, llama-cpp-python 0.3.31,
huggingface_hub 1.18.0, httpx 0.28.1. Model:
tencent/Hy-MT2-1.8B-GGUF (Hy-MT2-1.8B-Q4_K_M.gguf, ~1.08 GB).
