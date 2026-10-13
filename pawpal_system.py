from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity."""
    title: str
    duration_minutes: int
    priority: str = "medium"   # "low", "medium", or "high"
    category: str = "general"  # walk, feeding, meds, grooming, enrichment
    completed: bool = False

    def mark_complete(self) -> None:
        pass

    def is_high_priority(self) -> bool:
        pass


@dataclass
class Pet:
    """A pet and the care tasks assigned to it."""
    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass

    def get_pending_tasks(self) -> list[Task]:
        pass


class Owner:
    """A pet owner with a daily time budget and one or more pets."""

    def __init__(self, name: str, available_minutes: int, preferences: dict | None = None):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    """Builds a daily care plan for an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass

    def _sort_tasks(self, tasks: list[Task]) -> list[Task]:
        pass