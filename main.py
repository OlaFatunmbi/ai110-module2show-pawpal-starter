from pawpal_system import Owner, Pet, Task, Priority, Scheduler


def print_schedule(scheduler: Scheduler) -> None:
    """Print the plan as a readable table, plus anything that was skipped."""
    owner = scheduler.owner
    used = sum(t.duration_minutes for t in scheduler.plan)

    print("=" * 62)
    print(f"  TODAY'S SCHEDULE for {owner.name}")
    print(f"  Time used: {used} of {owner.available_minutes} minutes")
    print("=" * 62)
    print(f"  {'Time':<7}{'Pet':<9}{'Task':<20}{'Length':<9}{'Priority'}")
    print("  " + "-" * 58)
    for task in scheduler.plan:
        when = task.time or "flex"
        print(f"  {when:<7}{task.pet_name:<9}{task.title:<20}"
              f"{str(task.duration_minutes) + ' min':<9}{task.priority.name.title()}")

    if scheduler.skipped:
        print()
        print("  Skipped:")
        for task, reason in scheduler.skipped:
            print(f"    - {task.pet_name}: {task.title} ({reason})")
    print("=" * 62)


def main() -> None:
    owner = Owner("Jordan", available_minutes=75)

    biscuit = Pet("Biscuit", "dog", age=3)
    mochi = Pet("Mochi", "cat", age=5)
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # Tasks are added out of time order on purpose, so you can see the sorting work.
    biscuit.add_task(Task("Morning walk", 30, Priority.HIGH, "walk", time="08:00", frequency="daily"))
    biscuit.add_task(Task("Evening walk", 30, Priority.MEDIUM, "walk", time="18:00", frequency="daily"))
    biscuit.add_task(Task("Brush coat", 20, Priority.LOW, "grooming", time="19:30"))
    mochi.add_task(Task("Breakfast", 10, Priority.HIGH, "feeding", time="07:30", frequency="daily"))
    mochi.add_task(Task("Give medication", 5, Priority.HIGH, "meds", time="09:00", frequency="daily"))
    mochi.add_task(Task("Play session", 25, Priority.MEDIUM, "enrichment", time="17:00"))

    scheduler = Scheduler(owner)
    scheduler.generate_plan()
    print_schedule(scheduler)


if __name__ == "__main__":
    main()