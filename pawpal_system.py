from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum

VALID_FREQUENCIES = ("once", "daily", "weekly")


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
    category: str = "general"       # walk, feeding, meds, grooming, enrichment
    time: str | None = None         # optional preferred start time, "HH:MM" (24-hour)
    frequency: str = "once"         # "once", "daily", or "weekly"
    pet_name: str = ""              # set by Pet.add_task()
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate that duration is positive and frequency is a known value."""
        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        if self.frequency not in VALID_FREQUENCIES:
            raise ValueError(f"frequency must be one of {VALID_FREQUENCIES}")

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def reset(self) -> None:
        """Mark this task as not done (used for recurring tasks on a new day)."""
        self.completed = False

    def is_high_priority(self) -> bool:
        """Return True if this task has high priority."""
        return self.priority == Priority.HIGH

    def __str__(self) -> str:
        """Return a readable one-line description of the task."""
        who = f"{self.pet_name}: " if self.pet_name else ""
        at = f" at {self.time}" if self.time else ""
        return (f"{who}{self.title} ({self.duration_minutes} min, "
                f"{self.priority.name.lower()} priority{at})")


@dataclass
class Pet:
    """A pet and the care tasks assigned to it."""
    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, title: str) -> bool:
        """Remove the first task with this title; return True if one was removed."""
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                return True
        return False

    def get_pending_tasks(self) -> list[Task]:
        """Return this pet's tasks that are not completed yet."""
        return [t for t in self.tasks if not t.completed]


class Owner:
    """A pet owner with a daily time budget and one or more pets."""

    def __init__(self, name: str, available_minutes: int, preferences: dict | None = None):
        """Create an owner with a name, daily time budget, and optional preferences."""
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences or {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Pet | None:
        """Return the pet with this name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all pets, done or not."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_pending_tasks(self) -> list[Task]:
        """Return every task across all pets that isn't completed yet."""
        return [task for pet in self.pets for task in pet.get_pending_tasks()]


class Scheduler:
    """The 'brain': collects tasks across pets and builds a daily care plan."""

    def __init__(self, owner: Owner):
        """Create a scheduler for the given owner with an empty plan."""
        self.owner = owner
        self.plan: list[Task] = []
        self.skipped: list[tuple[Task, str]] = []  # (task, reason it was skipped)

    def generate_plan(self) -> list[Task]:
        """Pick pending tasks by priority until time runs out, then order them by time."""
        self.plan = []
        self.skipped = []
        remaining = self.owner.available_minutes

        for task in self._sort_tasks(self.owner.get_pending_tasks()):
            if task.duration_minutes <= remaining:
                self.plan.append(task)
                remaining -= task.duration_minutes
            else:
                self.skipped.append(
                    (task, f"needs {task.duration_minutes} min but only {remaining} min left")
                )

        # Stable sort: timed tasks first (by time), untimed keep their priority order.
        self.plan.sort(key=lambda t: (t.time is None, t.time or ""))
        return self.plan

    def explain_plan(self) -> str:
        """Return a plain-English explanation of what was scheduled and skipped."""
        if not self.plan and not self.skipped:
            return "No pending tasks to schedule."

        total = sum(t.duration_minutes for t in self.plan)
        lines = [
            f"Plan for {self.owner.name}: {total} of "
            f"{self.owner.available_minutes} available minutes used.",
            "",
            "Scheduled:",
        ]
        for task in self.plan:
            lines.append(f"  - {task}")
        if not self.plan:
            lines.append("  (nothing fit in the available time)")

        if self.skipped:
            lines += ["", "Skipped:"]
            for task, reason in self.skipped:
                lines.append(f"  - {task}: {reason}")

        lines += ["", "Tasks are chosen by priority (high first), then shorter tasks first."]
        return "\n".join(lines)

    def start_new_day(self) -> None:
        """Reset completed daily tasks so they show up in today's plan again."""
        for task in self.owner.get_all_tasks():
            if task.frequency == "daily":
                task.reset()

    def _sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort by priority (high first), breaking ties with shorter duration."""
        return sorted(tasks, key=lambda t: (-t.priority, t.duration_minutes))