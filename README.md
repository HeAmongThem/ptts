# Simple FastAPI

## Installation avec uv

```bash
uv sync
```

## Lancement

```bash
uv run uvicorn app:app --reload --port 8778
```

L'API est disponible sur `http://127.0.0.1:8778`.

## Routes

Obtenir un token :

```bash
curl http://127.0.0.1:8778/api/get_token
```

Exécuter avec un JSON :

```bash
curl -X POST http://127.0.0.1:8778/api/run \
  -H "Content-Type: application/json" \
  -d '{"message":"bonjour","value":42}'
```
