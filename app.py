import json
import httpx
from datetime import datetime, timedelta, timezone
from secrets import compare_digest, token_urlsafe
from typing import Any

from fastapi import Body, FastAPI, Request, status
from fastapi.responses import JSONResponse


app = FastAPI(title="Simple API")
"""
{ "command" : "fetch", "repo_name" : "repoCampaigns" }
{ "command" : "fetch", "repo_name" : "all" }
{ "command" : "create", "repo_name" : "repoCampaigns", "item" : { ... } }
{ "command" : "update", "repo_name" : "repoCampaigns", "item" : { "id" : 1, ... } }
{ "command" : "delete", "repo_name" : "repoCampaigns", "item" : { "item_id" : 1 } }
"""
CLIENT_SECRET="un_client_secret"

@app.post("/api/get_token")
def get_token(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    """Return an access token when the submitted client secret is valid."""
    submitted = str(payload.get("secret", ""))
    if not compare_digest(submitted.encode(), CLIENT_SECRET.encode()):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "invalid client secret"}
        )
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=600)
    response = {
        "token": token_urlsafe(32),
        "expires_at": expires_at.isoformat(),    
    }
    return JSONResponse (
        status_code = status.HTTP_200_OK,
        content=response
    )
    

@app.get("/api/get_token/error")
def get_token_error() -> JSONResponse:
    """Return an unauthorized error response."""
    return JSONResponse(
        status_code=401,
        content={"error": "Unauthorized"},
    )

DATASET_URL = "http://localhost:7887/dataset"


def _json_content(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return {"message": response.text or response.reason_phrase}


@app.post("/api/run")
def run(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    """Dispatch a dataset command (fetch | create | update | delete) to the dataset API."""
    command   = str(payload.get("command", "")).lower()
    repo_name = payload.get("repo_name")
    item      = payload.get("item")
    try:
        if command == "fetch":
            response = httpx.request("GET", f"{DATASET_URL}/run", json={"repo_name": repo_name})
        elif command == "create":
            response = httpx.post(f"{DATASET_URL}/{repo_name}", json=item)
        elif command == "update":
            response = httpx.put(f"{DATASET_URL}/{repo_name}", json=item)
        elif command == "delete":
            item_id = (item or {}).get("item_id")
            if item_id is None:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": "item.item_id is required for delete"}
                )
            response = httpx.delete(f"{DATASET_URL}/delete/{item_id}", params={"repo_name": repo_name})
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": f"command {command} not supported"}
            )

        return JSONResponse(
            status_code=response.status_code,
            content=_json_content(response)
        )
    except httpx.HTTPStatusError as exc:
        return JSONResponse(
            status_code=exc.response.status_code,
            content=_json_content(exc.response)
        )
    except httpx.HTTPError as exc:
        message = f"HTTP Exception - {exc}"
        print(message)
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"message": message}
        )


@app.exception_handler(Exception)
def unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
    print(f"unhandled error on {request.url}: {exc!r}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "internal server error"}
    )

