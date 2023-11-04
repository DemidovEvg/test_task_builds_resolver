from __future__ import annotations
from contextlib import asynccontextmanager

from functools import cached_property
from typing import Self
from fastapi import FastAPI

import yaml
from models import Build, BuildsFile, Task, TasksFile

from settings import settings


class Repo:
    """Репозиторий билдов и задач

    При старте приложения через метод reload билды и задачи подгружаются в репозиторий.
    """

    builds: tuple[Build, ...] = ()
    tasks: tuple[Task, ...] = ()

    def reload(self):
        with open(settings.path_to_builds, mode="r", encoding="utf-8") as fp:
            builds_raw = yaml.load(fp, Loader=yaml.Loader)
            self.builds = BuildsFile(**builds_raw).builds

        with open(settings.path_to_tasks, mode="r", encoding="utf-8") as fp:
            tasks_raw = yaml.load(fp, Loader=yaml.Loader)
            self.tasks = TasksFile(**tasks_raw).tasks

    def __call__(self) -> Self:
        if settings.reload_for_every_request:
            self.reload()
            if "builds_by_names" in self.__dict__:
                del self.__dict__["builds_by_names"]
            if "tasks_by_names" in self.__dict__:
                del self.__dict__["tasks_by_names"]
            if "builds_names" in self.__dict__:
                del self.__dict__["builds_names"]
        return self

    @cached_property
    def builds_by_names(self) -> dict[str, Build]:
        return {build.name: build for build in self.builds}

    @cached_property
    def tasks_by_names(self) -> dict[str, Build]:
        return {task.name: task for task in self.tasks}

    def get_build_by_name(self, name: str) -> Build | None:
        return self.builds_by_names.get(name)

    def get_task_by_name(self, name: str) -> Build | None:
        return self.tasks_by_names.get(name)

    @cached_property
    def builds_names(self) -> list[str]:
        return [build.name for build in self.builds]


repo = Repo()


@asynccontextmanager
async def lifespan_repo(app: FastAPI):
    repo.reload()
    yield
