from lor_deckcodes import LoRDeck
from postgres import Postgres
import pandas as pd
import sys
from scipy.stats import hypergeom
import numpy as np

# Decoding
deck = LoRDeck.from_deckcode(sys.argv[1])

# list all cards with card format 3:01SI001
print(list(deck))


def sql_output_as_dataframe(output) -> list:
    return [
        pd.DataFrame(result[0], columns=[x[0] for x in result[1]]) for result in output
    ]


with Postgres("dev/guillaumelegoy") as conn:
    deck_info = []
    card_codes = []
    card_count = {}

    for card in list(deck):
        card_codes.append(card[-7:])
        card_count[card[-7:]] = card[:1]

    card_count = pd.DataFrame.from_dict(card_count, orient="index").reset_index()

    card_info = conn.execute_query(
        f"SELECT code, card_name, region, cost, attack, health, rarity, main_type, subtype, supertype, keywords "
        f"FROM legendofruneterra_explorer.cards WHERE code IN %(card_codes)s",
        parameters={"card_codes": tuple(card_codes)},
    )

    print(card_info)

    deck_info = pd.DataFrame(
        card_info,
        columns=[
            "card_code",
            "card_name",
            "region",
            "cost",
            "attack",
            "health",
            "rarity",
            "main_type",
            "subtype",
            "supertype",
            "keywords",
        ],
    )

    deck_info = (
        pd.merge(
            deck_info, card_count, how="left", left_on="card_code", right_on="index",
        )
        .drop("index", axis=1)
        .rename(columns={0: "card_count"})
    )

    deck_info["turn_one_prob_to_draw"] = hypergeom.cdf(
        deck_info["card_count"].astype(int), 40, deck_info["card_count"].astype(int), 9,
    ) - hypergeom(40, deck_info["card_count"].astype(int), 9).pmf(0)

    deck_info["cost_turn_prob_to_draw"] = 0.0

    mask = deck_info["main_type"] == "Unit"
    deck_info["cost_turn_prob_to_draw"] = np.where(
        mask,
        hypergeom.cdf(
            deck_info["card_count"].astype(int),
            40,
            deck_info["card_count"].astype(int),
            8 + deck_info["cost"],
        )
        - hypergeom(40, deck_info["card_count"].astype(int), 8 + deck_info["cost"]).pmf(
            0
        ),
        deck_info["cost_turn_prob_to_draw"],
    )

    deck_info["cost_turn_prob_to_draw"] = np.where(
        deck_info["cost"].astype(int) >= 6,
        hypergeom.cdf(
            deck_info["card_count"].astype(int),
            40,
            deck_info["card_count"].astype(int),
            8 + (deck_info["cost"] - 3),
        )
        - hypergeom(
            40, deck_info["card_count"].astype(int), 8 + (deck_info["cost"] - 3)
        ).pmf(0),
        deck_info["cost_turn_prob_to_draw"],
    )

    deck_info["cost_turn_prob_to_draw"] = np.where(
        np.logical_or(
            deck_info["cost"].astype(int) == 4, deck_info["cost"].astype(int) == 5
        ),
        hypergeom.cdf(
            deck_info["card_count"].astype(int),
            40,
            deck_info["card_count"].astype(int),
            11,
        )
        - hypergeom(40, deck_info["card_count"].astype(int), 11).pmf(0),
        deck_info["cost_turn_prob_to_draw"],
    )

    deck_info["cost_turn_prob_to_draw"] = np.where(
        np.logical_or(
            deck_info["cost"].astype(int) == 2, deck_info["cost"].astype(int) == 3
        ),
        hypergeom.cdf(
            deck_info["card_count"].astype(int),
            40,
            deck_info["card_count"].astype(int),
            10,
        )
        - hypergeom(40, deck_info["card_count"].astype(int), 10).pmf(0),
        deck_info["cost_turn_prob_to_draw"],
    )
    mask = deck_info["cost"].astype(int) == 1
    deck_info["cost_turn_prob_to_draw"] = np.where(
        mask,
        hypergeom.cdf(
            deck_info["card_count"].astype(int),
            40,
            deck_info["card_count"].astype(int),
            9,
        )
        - hypergeom(40, deck_info["card_count"].astype(int), 10).pmf(0),
        deck_info["cost_turn_prob_to_draw"],
    )

    print(deck_info)
