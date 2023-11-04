from dataclasses import dataclass

from models import Build, Task
from repo import Repo


@dataclass
class BuildDependencyResolver:
    """Сервис для получения списка всех задач билда"""

    target_build: Build
    repo: Repo
    exclude_task_repetitions: bool = True

    @property
    def all_tasks_names(self) -> list[str]:
        return [task.name for task in self.all_tasks]

    @property
    def all_tasks(self) -> list[Task]:
        def get_all_tasks(
            current_task: Task, tasks: list[Task] | None = None
        ) -> list[Task]:
            if not current_task.dependencies:
                return tasks

            tasks = [] if tasks is None else tasks

            for task_name in current_task.dependencies:
                task = self.repo.get_task_by_name(task_name)
                tasks = get_all_tasks(task, tasks)
                tasks.append(task)

            return tasks

        result_tasks = []
        for task_name in self.target_build.tasks:
            task = self.repo.get_task_by_name(task_name)
            result_tasks = get_all_tasks(task, result_tasks)
            result_tasks.append(task)

        if self.exclude_task_repetitions:
            result_tasks = self.get_tasks_without_repetitions(result_tasks)
        return result_tasks

    def get_tasks_without_repetitions(self, build_dependencies: list[Task]):
        unique_tasks = set()
        return [
            unique_tasks.add(task) or task
            for task in build_dependencies
            if task not in unique_tasks
        ]
