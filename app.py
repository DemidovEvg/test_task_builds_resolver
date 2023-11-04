from fastapi import FastAPI, Depends, Body, HTTPException
from pydantic import ConfigDict, Field
from models import Build
from repo import repo, Repo, lifespan_repo
from services import BuildDependencyResolver
from typing import Annotated

app = FastAPI(lifespan=lifespan_repo)


@app.get("/get-builds")
async def get_builds(
    repo: Annotated[Repo, Depends(repo)],
) -> list[Build]:
    return repo.builds


@app.get("/get-builds-names")
async def get_builds_names(
    repo: Annotated[Repo, Depends(repo)],
) -> list[str]:
    return repo.builds_names


class BuildResponse(Build):
    model_config = ConfigDict(frozen=False)

    tasks_len: int = Field(default=0, init_var=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tasks_len = len(self.tasks)


@app.post("/get-tasks")
async def get_tasks(
    *,
    build: Annotated[str, Body(embed=True)],
    repo: Annotated[Repo, Depends(repo)],
) -> BuildResponse:
    target_build = repo.get_build_by_name(build)
    if not target_build:
        raise HTTPException(status_code=404, detail="Build not found")
    try:
        tasks_names = BuildDependencyResolver(
            target_build=target_build,
            repo=repo,
        ).all_tasks_names
    except RecursionError:
        raise HTTPException(status_code=400, detail="Build has recursion dependencies")
    return dict(name=target_build.name, tasks=tasks_names)
