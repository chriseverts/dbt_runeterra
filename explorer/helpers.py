from dataclasses import dataclass, field
from pathlib import Path

import git


def get_repository_root_path() -> Path:
    return Path(git.Repo(".", search_parent_directories=True).working_tree_dir)


def get_cards_path() -> Path:
    return get_repository_root_path().joinpath("data/cards/en_us/data/set1-en_us.json")


def get_global_path() -> Path:
    return get_repository_root_path().joinpath(
        "data/global/en_us/data/globals-en_us.json"
    )


def get_dbt_seeds_path() -> Path:
    return get_repository_root_path().joinpath("explorer/dbt/data")


@dataclass
class ProjectPaths:
    root: Path = field(default_factory=get_repository_root_path)
    cards: Path = field(default_factory=get_cards_path)
    globals: Path = field(default_factory=get_global_path)
    dbt_seeds: Path = field(default_factory=get_dbt_seeds_path)
