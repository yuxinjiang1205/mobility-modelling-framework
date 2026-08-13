# AI Collaboration Record
# Tool: ChatGPT (OpenAI)
# Purpose: Integrate all framework layers into a complete mobility representation.
# Prompt summary: Develop a reusable function that combines one representative
# demographic profile with the constrained Behavioural Evidence Layer and
# Opportunity Layer. Apply general trip-purpose-to-POI mappings, refine retained
# Commuting purposes using the profile’s industry mapping, preserve excluded
# mapping outcomes, and return both the complete nested representation and
# presentation-ready DataFrames for every framework layer.

import pandas as pd
from IPython.display import Markdown, display
from src.demographic_behaviour_layers_integration import (
    construct_constrained_behaviour_representation
)

def construct_complete_framework(
    representative_profile,
    assembled_behavioural_evidence,
    opportunity_layer,
    industry_component,
):
    # ==========================================================
    # 1. Construct Demographic and Behavioural Evidence Layers
    # ==========================================================

    complete_framework_representation = (
        construct_constrained_behaviour_representation(
            representative_profile=(
                representative_profile
            ),
            assembled_behavioural_evidence=(
                assembled_behavioural_evidence
            ),
        )
    )

    representative_profile = complete_framework_representation[
        "representative_profile"
    ]

    trip_purpose_distribution = complete_framework_representation[
        "behavioural_representation"
    ]["conditioned_trip_purpose_distribution"]

    # ==========================================================
    # 2. Add General Opportunity Mapping
    # ==========================================================

    for trip_purpose, distributions in (
        trip_purpose_distribution.items()
    ):

        if trip_purpose not in opportunity_layer:
            raise KeyError(
                f"No Opportunity mapping found for: "
                f"{trip_purpose}"
            )

        opportunity_details = opportunity_layer[
            trip_purpose
        ]

        distributions["mapping_strategy"] = (
            opportunity_details["mapping_strategy"]
        )

        distributions["poi_distribution"] = (
            opportunity_details[
                "poi_distribution"
            ].copy()
        )
        if (
            opportunity_details["mapping_strategy"]
            == "Excluded Mapping"
        ):
            distributions["allocation_outcome"] = (
                opportunity_details["allocation_outcome"]
            )

        distributions[
            "industry_refinement_applied"
        ] = False

    # ==========================================================
    # 3. Refine Commuting Using Industry
    # ==========================================================

    if "Commuting" in trip_purpose_distribution:

        industry = representative_profile["Industry"]

        if industry not in industry_component:
            raise KeyError(
                f"No Industry mapping found for: "
                f"{industry}"
            )

        commuting_distributions = (
            trip_purpose_distribution["Commuting"]
        )

        # Preserve the original general POI distribution
        commuting_distributions[
            "general_poi_distribution"
        ] = commuting_distributions[
            "poi_distribution"
        ].copy()

        commuting_distributions["industry"] = industry

        # Replace with the industry-refined POI distribution
        commuting_distributions[
            "poi_distribution"
        ] = industry_component[industry].copy()

        commuting_distributions[
            "industry_refinement_applied"
        ] = True

    # ==========================================================
    # 4. Prepare Demographic Layer DataFrame
    # ==========================================================

    demographic_dataframe = pd.DataFrame(
        [representative_profile]
    )

    # ==========================================================
    # 5. Prepare Trip-purpose Probability DataFrame
    # ==========================================================

    trip_purpose_probability_dataframe = pd.DataFrame(
        [
            {
                "Trip Purpose": trip_purpose,
                "Probability": distributions[
                    "trip_purpose_probability"
                ],
            }
            for trip_purpose, distributions
            in trip_purpose_distribution.items()
        ]
    )

    trip_purpose_probability_dataframe[
        "Probability"
    ] = trip_purpose_probability_dataframe[
        "Probability"
    ].round(4)

    # ==========================================================
    # 6. Prepare Temporal Distribution DataFrame
    # ==========================================================

    temporal_distribution_dataframe = (
        pd.DataFrame.from_dict(
            {
                trip_purpose: distributions[
                    "temporal_distribution"
                ]
                for trip_purpose, distributions
                in trip_purpose_distribution.items()
            },
            orient="index",
        )
        .rename_axis("Trip Purpose")
        .reset_index()
        .round(4)
    )

    # ==========================================================
    # 7. Prepare Travel-mode Distribution DataFrame
    # ==========================================================

    travel_mode_distribution_dataframe = (
        pd.DataFrame.from_dict(
            {
                trip_purpose: distributions[
                    "travel_mode_distribution"
                ]
                for trip_purpose, distributions
                in trip_purpose_distribution.items()
            },
            orient="index",
        )
        .rename_axis("Trip Purpose")
        .reset_index()
        .round(4)
    )

    # ==========================================================
    # 8. Prepare Opportunity Layer DataFrame
    # ==========================================================

    opportunity_rows = []

    for trip_purpose, distributions in (
        trip_purpose_distribution.items()
    ):

        if (
            distributions["mapping_strategy"]
            == "Excluded Mapping"
        ):

            opportunity_rows.append(
                {
                    "Trip Purpose": trip_purpose,
                    "POI Category": distributions[
                        "allocation_outcome"
                    ],
                    "Weight": None,
                }
            )

            continue

        final_poi_distribution = distributions[
            "poi_distribution"
        ]

        for poi_category, weight in (
            final_poi_distribution.items()
        ):

            opportunity_rows.append(
                {
                    "Trip Purpose": trip_purpose,
                    "POI Category": poi_category,
                    "Weight": round(weight, 4),
                }
            )

    # ==========================================================
    # 9. Store Presentation DataFrames
    # ==========================================================

    framework_dataframes = {
        "demographic_layer": (
            demographic_dataframe
        ),
        "trip_purpose_probabilities": (
            trip_purpose_probability_dataframe
        ),
        "temporal_distributions": (
            temporal_distribution_dataframe
        ),
        "travel_mode_distributions": (
            travel_mode_distribution_dataframe
        ),
        "opportunity_layer": (
            pd.DataFrame(opportunity_rows)
        ),
    }

    # ==========================================================
    # 10. Return Complete Results
    # ==========================================================

    return (
        complete_framework_representation,
        framework_dataframes,
    )


# AI Collaboration Record
# Tool: ChatGPT (OpenAI)
# Purpose: Improve the presentation of excluded opportunity mappings.
# Prompt summary: Preserve the underlying None/NaN weight for trip purposes
# outside the POI scope, but display it as “N/A”. Format valid opportunity
# weights to four decimal places without modifying the original DataFrame
# or affecting framework validation.


### Framework Display Functions ###
def display_complete_framework(
    framework_dataframes,
):
    """
    Display each framework component
    as a separate DataFrame.
    """

    display(
        Markdown(
            "## Demographic Layer"
        )
    )

    display(
        framework_dataframes[
            "demographic_layer"
        ]
    )

    display(
        Markdown(
            "## Behavioural Evidence Layer"
            "\n### Trip-purpose Probabilities"
        )
    )

    display(
        framework_dataframes[
            "trip_purpose_probabilities"
        ]
    )

    display(
        Markdown(
            "### Temporal Distributions"
        )
    )

    display(
        framework_dataframes[
            "temporal_distributions"
        ]
    )

    display(
        Markdown(
            "### Travel-mode Distributions"
        )
    )

    display(
        framework_dataframes[
            "travel_mode_distributions"
        ]
    )

    display(
        Markdown(
            "## Opportunity Layer"
            "\n### Final POI Mapping"
        )
    )

    # Create a presentation-only copy so that
    # the original framework DataFrame remains
    # unchanged for subsequent validation.
    opportunity_display = (
        framework_dataframes[
            "opportunity_layer"
        ].copy()
    )

    # Display excluded mappings as N/A while
    # formatting valid weights to four decimals.
    opportunity_display["Weight"] = (
        opportunity_display["Weight"]
        .apply(
            lambda value: (
                "N/A"
                if pd.isna(value)
                else f"{value:.4f}"
            )
        )
    )

    display(
        opportunity_display
    )