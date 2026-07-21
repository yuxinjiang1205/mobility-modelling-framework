import math

import pandas as pd

from .constraints import (
    apply_trip_purpose_constraint,
    apply_travel_mode_constraint,
)


PROFILE_COLUMNS = (
    "Age",
    "Gender",
    "Household Type",
    "Economic Activity Status",
    "Industry",
    "Ethnic Group",
    "Distance travelled to work",
    "Car Ownership",
)


NON_PROBABILITY_FIELDS = {
    "Year",
    "Purpose",
    "Trip purpose",
}


PROBABILITY_TOLERANCE = 1e-8


def _convert_profile_to_dict(profile):
    """
    Convert a demographic profile into a
    standard Python dictionary.

    The profile may be provided as either a
    dictionary or a pandas Series.
    """
    if isinstance(profile, dict):
        return profile.copy()

    if isinstance(profile, pd.Series):
        return profile.to_dict()

    raise TypeError(
        "Profile must be provided as either "
        "a dictionary or a pandas Series. "
        f"Received: {type(profile).__name__}."
    )


def _validate_probability_distribution(
    distribution,
    distribution_name,
):
    """
    Validate that a probability distribution
    is non-empty, contains no negative values,
    and sums to one within the permitted
    floating-point tolerance.
    """
    if not distribution:
        raise ValueError(
            f"{distribution_name} is empty."
        )

    negative_values = {
        category: probability
        for category, probability
        in distribution.items()
        if probability < 0
    }

    if negative_values:
        raise ValueError(
            f"{distribution_name} contains "
            "negative probabilities: "
            f"{negative_values}"
        )

    probability_sum = sum(
        distribution.values()
    )

    if not math.isclose(
        probability_sum,
        1.0,
        rel_tol=0.0,
        abs_tol=PROBABILITY_TOLERANCE,
    ):
        raise ValueError(
            f"{distribution_name} does not "
            "sum to one. Observed sum: "
            f"{probability_sum}"
        )


def construct_constrained_behaviour_profile(
    profile,
    behavioural_evidence,
):
    """
    Construct a constrained behavioural
    representation for one feasible
    representative demographic profile.

    The returned representation contains:

    - eight demographic attributes;
    - a constrained trip-purpose distribution;
    - one temporal distribution for each
      remaining trip purpose; and
    - one constrained travel-mode distribution
      for each remaining trip purpose.

    No trip purpose, start time, or travel mode
    is sampled by this function.
    """
    profile = _convert_profile_to_dict(
        profile
    )

    missing_attributes = [
        attribute
        for attribute in PROFILE_COLUMNS
        if attribute not in profile
    ]

    if missing_attributes:
        raise ValueError(
            "Profile is missing required "
            f"attributes: {missing_attributes}"
        )

    # ==========================================
    # 1. Retrieve Trip-Purpose Probabilities
    # ==========================================

    original_purpose_probabilities = {}

    for purpose, evidence in (
        behavioural_evidence.items()
    ):
        baseline_profiles = evidence.get(
            "baseline_profile",
            [],
        )

        matching_age_gender_profiles = [
            baseline_profile
            for baseline_profile
            in baseline_profiles
            if (
                baseline_profile["Age"]
                == profile["Age"]
            )
            and (
                baseline_profile["Gender"]
                == profile["Gender"]
            )
        ]

        if (
            len(matching_age_gender_profiles)
            != 1
        ):
            raise ValueError(
                "Expected one baseline profile "
                f"for purpose={purpose}, "
                f"age={profile['Age']}, "
                f"gender={profile['Gender']}; "
                "found "
                f"{len(matching_age_gender_profiles)}."
            )

        matching_age_gender_profile = (
            matching_age_gender_profiles[0]
        )

        original_purpose_probabilities[
            purpose
        ] = float(
            matching_age_gender_profile[
                "Trip Purpose Probability"
            ]
        )

    _validate_probability_distribution(
        distribution=(
            original_purpose_probabilities
        ),
        distribution_name=(
            "Original trip-purpose distribution"
        ),
    )

    # ==========================================
    # 2. Apply Trip-Purpose Constraints
    # ==========================================

    constrained_purpose_probabilities = (
        apply_trip_purpose_constraint(
            profile=profile,
            trip_purpose_probabilities=(
                original_purpose_probabilities
            ),
        )
    )

    _validate_probability_distribution(
        distribution=(
            constrained_purpose_probabilities
        ),
        distribution_name=(
            "Constrained trip-purpose distribution"
        ),
    )

    # ==========================================
    # 3. Construct Purpose-Conditioned Profiles
    # ==========================================

    purpose_conditioned_profiles = {}

    for purpose, purpose_probability in (
        constrained_purpose_probabilities.items()
    ):
        evidence = behavioural_evidence[
            purpose
        ]

        temporal_profiles = evidence.get(
            "temporal_pattern_profile",
            [],
        )

        travel_mode_profiles = evidence.get(
            "travel_mode_profile",
            [],
        )

        if len(temporal_profiles) != 1:
            raise ValueError(
                "Expected one temporal profile "
                f"for purpose={purpose}; "
                f"found {len(temporal_profiles)}."
            )

        if len(travel_mode_profiles) != 1:
            raise ValueError(
                "Expected one travel-mode profile "
                f"for purpose={purpose}; "
                f"found {len(travel_mode_profiles)}."
            )

        temporal_profile = (
            temporal_profiles[0]
        )

        travel_mode_profile = (
            travel_mode_profiles[0]
        )

        # Retain only time-interval
        # probability fields.
        temporal_distribution = {
            interval: float(probability)
            for interval, probability
            in temporal_profile.items()
            if interval
            not in NON_PROBABILITY_FIELDS
        }

        # Retain only travel-mode
        # probability fields.
        original_mode_distribution = {
            mode: float(probability)
            for mode, probability
            in travel_mode_profile.items()
            if mode
            not in NON_PROBABILITY_FIELDS
        }

        _validate_probability_distribution(
            distribution=(
                temporal_distribution
            ),
            distribution_name=(
                f"Temporal distribution "
                f"for {purpose}"
            ),
        )

        _validate_probability_distribution(
            distribution=(
                original_mode_distribution
            ),
            distribution_name=(
                f"Original travel-mode "
                f"distribution for {purpose}"
            ),
        )

        constrained_mode_distribution = (
            apply_travel_mode_constraint(
                age=profile["Age"],
                car_ownership=(
                    profile["Car Ownership"]
                ),
                travel_mode_probabilities=(
                    original_mode_distribution
                ),
            )
        )

        _validate_probability_distribution(
            distribution=(
                constrained_mode_distribution
            ),
            distribution_name=(
                f"Constrained travel-mode "
                f"distribution for {purpose}"
            ),
        )

        purpose_conditioned_profiles[
            purpose
        ] = {
            "trip_purpose_probability": (
                purpose_probability
            ),
            "temporal_distribution": (
                temporal_distribution
            ),
            "travel_mode_distribution": (
                constrained_mode_distribution
            ),
        }

    # ==========================================
    # 4. Return Integrated Representation
    # ==========================================

    return {
        "demographic_profile": {
            attribute: profile[attribute]
            for attribute in PROFILE_COLUMNS
        },
        "behavioural_representation": {
            "trip_purpose_distribution": (
                constrained_purpose_probabilities
            ),
            "purpose_conditioned_profiles": (
                purpose_conditioned_profiles
            ),
        },
    }