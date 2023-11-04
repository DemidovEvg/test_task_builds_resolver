from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    """Класс задачи

    Из описания к заданию не совсем очевидно в каком порядке должны
    выполняться зависимости из списка dependencies, видимо в произвольном.
    Будем считать что предпочтительно прямой порядок
    """

    model_config = ConfigDict(frozen=True)

    name: str
    dependencies: tuple[str, ...]


class Build(BaseModel):
    """Класс билда

    Из описания к заданию подразумевается что задачи для билда должны
    выполняться в прямом порядке
    """

    model_config = ConfigDict(frozen=True)

    name: str
    tasks: tuple[str, ...]


class BuildsFile(BaseModel):
    builds: tuple[Build, ...]


class TasksFile(BaseModel):
    tasks: tuple[Task, ...]
