from dataclasses import dataclass, field
from enum import IntEnum


class Priority(IntEnum):
    """Task priority. Higher value = more important, so sorting is reliable."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    """A single pet care activity."""
    title: str
    duration_minutes: int
    priority: Priority = Priority.MEDIUM
    category: str = "general"  # walk, feeding, meds, grooming, enrichment
    pet_name: str = ""         # set by Pet.add_task() so the plan can say which pet
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
        """Add a task and set task.pet_name to this pet's name."""
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
        self.plan: list[Task] = []
        self.skipped: list[tuple[Task, str]] = []  # (task, reason it was skipped)

    def generate_plan(self) -> list[Task]:
        """Fill self.plan and self.skipped using pending tasks and available time."""
        pass

    def explain_plan(self) -> str:
        """Explain why tasks were scheduled or skipped, using self.plan and self.skipped."""
        pass

    def _sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort by priority (high first), then shorter duration first."""
        pass