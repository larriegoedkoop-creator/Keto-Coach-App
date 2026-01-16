from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
import json
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class Recipe:
    name: str
    net_carbs_g: int
    calories: int
    prep_minutes: int
    tags: tuple[str, ...]


@dataclass(frozen=True)
class TrainingDay:
    day: date
    start_time: time
    focus: str


@dataclass(frozen=True)
class CoachProfile:
    name: str
    timezone: str
    meal_times: tuple[time, ...]
    training_days: tuple[TrainingDay, ...]


@dataclass(frozen=True)
class DailyPlan:
    day: date
    recipes: tuple[Recipe, ...]
    notification_times: tuple[time, ...]
    training: Optional[TrainingDay]
    coach_note: str


def load_recipes(path: Path) -> list[Recipe]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    recipes = [
        Recipe(
            name=item["name"],
            net_carbs_g=item["net_carbs_g"],
            calories=item["calories"],
            prep_minutes=item["prep_minutes"],
            tags=tuple(item["tags"]),
        )
        for item in raw
    ]
    return recipes


def _select_recipes(recipes: Iterable[Recipe], day: date, count: int) -> tuple[Recipe, ...]:
    recipes_list = list(recipes)
    if not recipes_list:
        return tuple()
    seed = day.toordinal()
    selected = []
    for offset in range(count):
        index = (seed + offset) % len(recipes_list)
        selected.append(recipes_list[index])
    return tuple(selected)


def _training_for_day(training_days: Iterable[TrainingDay], day: date) -> Optional[TrainingDay]:
    for training_day in training_days:
        if training_day.day == day:
            return training_day
    return None


def build_daily_plan(
    profile: CoachProfile,
    recipes: Iterable[Recipe],
    day: date,
) -> DailyPlan:
    training = _training_for_day(profile.training_days, day)
    selected = _select_recipes(recipes, day, count=len(profile.meal_times))
    if training:
        coach_note = (
            f"Training vandaag om {training.start_time.strftime('%H:%M')} "
            f"({training.focus}). Hydrateer extra en voeg een eiwitrijke snack toe."
        )
    else:
        coach_note = "Rustdag: focus op consistente maaltijden en voldoende water."
    return DailyPlan(
        day=day,
        recipes=selected,
        notification_times=profile.meal_times,
        training=training,
        coach_note=coach_note,
    )


def _format_plan(plan: DailyPlan) -> str:
    lines = [f"Dagplanning voor {plan.day.isoformat()}", plan.coach_note, ""]
    for slot, recipe in zip(plan.notification_times, plan.recipes):
        lines.append(
            f"- {slot.strftime('%H:%M')} | {recipe.name} "
            f"({recipe.net_carbs_g}g carbs, {recipe.calories} kcal, "
            f"{recipe.prep_minutes} min)"
        )
    if plan.training:
        lines.append(
            f"Training: {plan.training.focus} om {plan.training.start_time.strftime('%H:%M')}"
        )
    return "\n".join(lines)


def _default_profile() -> CoachProfile:
    return CoachProfile(
        name="Alex",
        timezone="Europe/Amsterdam",
        meal_times=(time(8, 0), time(12, 30), time(18, 30)),
        training_days=(
            TrainingDay(day=date.today(), start_time=time(19, 0), focus="Kracht"),
        ),
    )


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    recipes = load_recipes(repo_root / "data" / "sample_recipes.json")
    profile = _default_profile()
    plan = build_daily_plan(profile, recipes, date.today())
    print(_format_plan(plan))


if __name__ == "__main__":
    main()
