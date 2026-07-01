# LLM Inference Platform

A production-grade LLM inference platform running on self-hosted hardware — converting a retired laptop into an always-on inference server accessible from anywhere.

## Architecture

Omen (Dev Machine)

│

│  Tailscale VPN

│

nitro-server (Acer Nitro 5)

├── Ollama → phi3:mini (local LLM inference)

├── RAG API → FastAPI (wired to Ollama)

├── Prometheus (metrics) [coming soon]

└── Grafana (dashboard) [coming soon]

## Stack

- **OS**: Ubuntu Server 26.04 LTS
- **Networking**: Tailscale (MagicDNS + private VPN)
- **LLM Serving**: Ollama (`phi3:mini`)
- **RAG API**: FastAPI (from `rag-document-qa`, rewired to local Ollama)
- **Observability**: Prometheus + Grafana (Phase 3)
- **CI/CD**: GitHub Actions (Phase 4)

## Hardware

- **Server**: Acer Nitro 5 (Intel Core i5, 4GB NVIDIA GPU, 8GB RAM)
- **Dev Machine**: HP Omen (Intel Core Ultra 7 255H, RTX 5060 8GB, 24GB DDR5)

## Phases

- [x] Phase 1 — Base server setup (Ubuntu, SSH, Tailscale, Ollama)
- [x] Phase 2 — Dockerize services, RAG API deployment
- [ ] Phase 3 — Prometheus + Grafana observability
- [ ] Phase 4 — GitHub Actions CI/CD

## Accessing the Server

The server is accessible from any device on the same Tailscale network:

```bash
ssh om@nitro-server
```

Ollama API endpoint: http://nitro-server:11434

## Services

### Ollama (LLM Serving)
- Model: `phi3:mini` (3.8B parameters, 4-bit quantized)
- Endpoint: `http://nitro-server:11434`
- No API costs — fully local inference

### RAG API (FastAPI)
- Endpoint: `http://nitro-server:8000`
- `GET /health` — health check
- `POST /query` — ask a question, get answer + sources
- `GET /docs` — interactive Swagger UI
- Backed by ChromaDB (236 chunks from 2 research papers)
- LLM: Ollama primary, Groq fallback (circuit breaker pattern)

## Related Projects

- [rag-document-qa](https://github.com/OmUniyal/rag-document-qa) — RAG system wired to this inference server