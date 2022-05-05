from explorer.utils.path_util import ProjectPaths
import json
import pandas as pd

column_names = [
    "code",
    "region",
    "card_name",
    "cost",
    "attack",
    "health",
    "rarity",
    "main_type",
    "subtype",
    "supertype",
    "associated_cards",
    "keywords",
    "description",
    "level_up_description",
]

cards_list = []

with open(ProjectPaths().cards) as cards_file:
    cards = json.load(cards_file)

    for c in cards:
        current_card = [
            c["cardCode"],
            c["regionRef"],
            c["name"],
            c["cost"],
            c["attack"],
            c["health"],
            c["rarityRef"],
            c["type"],
            c["subtype"],
            c["supertype"],
            c["associatedCardRefs"],
            c["keywordRefs"],
            c["descriptionRaw"],
            c["levelupDescriptionRaw"],
        ]

        cards_list.append(current_card)

pd.DataFrame(cards_list, columns=column_names).to_csv(
    ProjectPaths().dbt_seeds.joinpath("cards.csv"), index=False
)
