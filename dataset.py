import json
from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from typing import Any

from dataclasses import dataclass
from fastapi import Body, FastAPI, Request, status
from fastapi.responses import JSONResponse
import repo


print("APIDATASET")
app = FastAPI(title="Simple API")

REPO_NAME = {
    "BusinessUnits"     : "repoBusinessUnits",
    "Categories"        : "repoCategories",
    "Users"             : "repoUsers",
    "Indicators"        : "repoIndicators",
    "Campaigns"         : "repoCampaigns",
    "CampaignIndicators": "repoCampaignIndicators",
    "IndicatorAudits"   : "repoIndicatorAudits",
    "Settings"          : "repoSettings",
    "All"               : "all"
}



def _response_content(response: JSONResponse) -> Any:
    return json.loads(response.body) # type: ignore

def _fetch_repos():
    result: dict[str, Any]           = {}
    result["repoBusinessUnits"]      = repo.repoBusinessUnits
    result["repoCategories"]         = repo.repoCategories
    result["repoUsers"]              = repo.repoUsers
    result["repoIndicators"]         = repo.repoIndicators
    result["repoCampaigns"]          = repo.repoCampaigns
    result["repoCampaignIndicators"] = repo.repoCampaignIndicators
    result["repoIndicatorAudits"]    = repo.repoIndicatorAudits
    result["repoSettings"]           = repo.repoSettings
    return result

def _select_repo(repoName: str) -> JSONResponse:
    content = {}
    match repoName:
        case "repoBusinessUnits":
            content = repo.repoBusinessUnits
        case "repoCategories":
            content = repo.repoCategories
        case "repoUsers":
            content = repo.repoUsers
        case "repoIndicators":
            content = repo.repoIndicators
        case "repoCampaigns":
            content = repo.repoCampaigns
        case "repoCampaignIndicators":
            content = repo.repoCampaignIndicators
        case "repoIndicatorAudits":
            content = repo.repoIndicatorAudits
        case "repoSettings":
            content = repo.repoSettings
        case "all":
            content = _fetch_repos()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = content        
    )


### fetch 1 repos
#{
#    "repo_name" : "name one of repo"
#}
### fetch all repos
#{
#    "repo_name" : "all"
#}
###
@app.get("/dataset/run")
@app.post("/dataset/run")
def run(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    content = {}
    if "repo_name" not in payload:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { "message" : "repo_name is required" }
        )
    if str(payload['repo_name']).lower() not in [ str(n).lower() for n in REPO_NAME.values()]:        
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content = { "message" : f'{payload['repo_name']} not found' }
        )
    
    if str(payload['repo_name']).lower() == "all":
        return _select_repo(payload['repo_name'])

    repo =  _select_repo(payload['repo_name'])
    repo_content = json.loads(repo.body)
    return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = repo_content
        )

@dataclass
class EntityBase():
    id : int 




def _create(repo: list[dict[str, Any]], item: Any) -> dict[str, Any]:
    new_id = max((entity["id"] for entity in repo), default=0) + 1
    entity = {**item, "id": new_id}
    repo.append(entity)
    return entity


def _item_id_key(item: dict[str, Any]) -> str | None:
    if "id" in item:
        return "id"
    if "item_id" in item:
        return "item_id"
    candidates = [k for k in item if k.endswith("_id")]
    return candidates[0] if len(candidates) == 1 else None


def _item_id(item: dict[str, Any]) -> Any:
    key = _item_id_key(item)
    return item[key] if key is not None else None


def _update(repo: list[dict[str, Any]], item: Any) -> dict[str, Any]:
    key = _item_id_key(item)
    item_id = _item_id(item)
    changes = {k: v for k, v in item.items() if k != key}
    changes["id"] = item_id
    for index, entity in enumerate(repo):
        if entity["id"] == item_id:
            repo[index] = {**entity, **changes}
            return repo[index]
    raise KeyError(f"id {item_id} not found")


def _delete(repo: list[dict[str, Any]], id: int | dict[str, Any]) -> dict[str, Any]:
    item_id = _item_id(id) if isinstance(id, dict) else id
    for index, entity in enumerate(repo):
        if entity["id"] == item_id:
            return repo.pop(index)
    raise KeyError(f"id {item_id} not found")


WRITABLE_REPOS = [name for name in REPO_NAME.values() if name != "all"]


def _get_writable_repo(repo_name: str) -> list[dict[str, Any]] | None:
    if repo_name not in WRITABLE_REPOS:
        return None
    return getattr(repo, repo_name)


def _not_found_response(repo_name: str) -> JSONResponse:
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = { "message" : f'{repo_name} not found' }
    )


@app.post("/dataset/{repo_name}", status_code = status.HTTP_201_CREATED)
def create_item(repo_name: str, payload: dict[str, Any] = Body(...)) -> JSONResponse:
    target = _get_writable_repo(repo_name)
    if target is None:
        return _not_found_response(repo_name)
    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = _create(target, payload)
    )


@app.put("/dataset/{repo_name}")
def update_item(repo_name: str, payload: dict[str, Any] = Body(...)) -> JSONResponse:
    target = _get_writable_repo(repo_name)
    if target is None:
        return _not_found_response(repo_name)
    if _item_id(payload) is None:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = { "message" : "id is required" }
        )
    try:
        updated = _update(target, payload)
    except KeyError as e:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content = { "message" : str(e.args[0]) }
        )
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = updated
    )


@app.delete("/dataset/delete/{item_id}")
def delete_item(item_id: int, repo_name: str) -> JSONResponse:
    target = _get_writable_repo(repo_name)
    if target is None:
        return _not_found_response(repo_name)
    try:
        deleted = _delete(target, item_id)
    except KeyError as e:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content = { "message" : str(e.args[0]) }
        )
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = deleted
    )


@app.exception_handler(Exception)
def unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
    print(f"unhandled error on {request.url}: {exc!r}")
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = { "message" : "internal server error" }
    )


