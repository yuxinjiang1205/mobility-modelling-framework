import math
from collections.abc import Mapping

from .constraints import (
    apply_trip_purpose_constraint,
    apply_travel_mode_constraint,
)


# ==========================================
# Configuration
# ==========================================

DEMOGRAPHIC_ATTRIBUTES = (
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


NTS0611A_EVIDENCE_KEY = (
    "nts0611a_trip_purpose_profiles"
)

NTS0502B_EVIDENCE_KEY = (
    "nts0502b_temporal_profiles"
)

NTS0409A_EVIDENCE_KEY = (
    "nts0409a_travel_mode_profiles"
)


PROBABILITY_TOLERANCE = 1e-8


# ==========================================
# Input Conversion
# ==========================================

def _convert_demographic_profile_to_dict(
    demographic_profile,
):
    """
    Convert one demographic profile into a
    standard Python dictionary.

    The profile may be supplied as a dictionary,
    another mapping object, or an object such as
    a pandas Series that provides a to_dict()
    method.
    """
    if isinstance(
        demographic_profile,
        Mapping,
    ):
        return dict(demographic_profile)

    if hasattr(
        demographic_profile,
        "to_dict",
    ):
        converted_profile = (
            demographic_profile.to_dict()
        )

        if isinstance(
            converted_profile,
            Mapping,
        ):
            return dict(converted_profile)

    raise TypeError(
        "Demographic profile must be provided "
        "as a mapping or as an object with a "
        "to_dict() method. Received: "
        f"{type(demographic_profile).__name__}."
    )


def _convert_evidence_records_to_list(
    evidence_records,
    evidence_name,
):
    """
    Convert evidence records into a list of
    dictionaries.

    Evidence may be loaded from JSON as a list
    of dictionaries or supplied as a pandas
    DataFrame.
    """
    if isinstance(
        evidence_records,
        list,
    ):
        records = evidence_records

    elif hasattr(
        evidence_records,
        "to_dict",
    ):
        try:
            records = evidence_records.to_dict(
                orient="records"
            )
        except TypeError:
            records = evidence_records.to_dict()

    else:
        raise TypeError(
            f"{evidence_name} must be provided "
            "as a list of records or as a "
            "DataFrame-like object."
        )

    if not isinstance(records, list):
        raise TypeError(
            f"{evidence_name} could not be "
            "converted into a list of records."
        )

    invalid_record_positions = [
        index
        for index, record in enumerate(records)
        if not isinstance(record, Mapping)
    ]

    if invalid_record_positions:
        raise TypeError(
            f"{evidence_name} contains records "
            "that are not dictionaries at "
            f"positions: {invalid_record_positions}"
        )

    return [
        dict(record)
        for record in records
    ]


# ==========================================
# Validation
# ==========================================

def _validate_required_demographic_attributes(
    demographic_profile,
):
    """
    Confirm that all eight required demographic
    attributes are present.
    """
    missing_attributes = [
        attribute
        for attribute
        in DEMOGRAPHIC_ATTRIBUTES
        if attribute
        not in demographic_profile
    ]

    if missing_attributes:
        raise ValueError(
            "Demographic profile is missing "
            "required attributes: "
            f"{missing_attributes}"
        )


def _validate_probability_distribution(
    distribution,
    distribution_name,
):
    """
    Confirm that a probability distribution is
    non-empty, numeric, finite, non-negative,
    and sums to one within the permitted
    floating-point tolerance.
    """
    if not isinstance(
        distribution,
        Mapping,
    ):
        raise TypeError(
            f"{distribution_name} must be "
            "provided as a dictionary."
        )

    if not distribution:
        raise ValueError(
            f"{distribution_name} is empty."
        )

    validated_distribution = {}

    for category, probability in (
        distribution.items()
    ):
        try:
            numeric_probability = float(
                probability
            )
        except (TypeError, ValueError) as error:
            raise TypeError(
                f"{distribution_name} contains "
                "a non-numeric probability for "
                f"{category}: {probability}"
            ) from error

        if not math.isfinite(
            numeric_probability
        ):
            raise ValueError(
                f"{distribution_name} contains "
                "a non-finite probability for "
                f"{category}: {numeric_probability}"
            )

        if numeric_probability < 0:
            raise ValueError(
                f"{distribution_name} contains "
                "a negative probability for "
                f"{category}: {numeric_probability}"
            )

        validated_distribution[
            category
        ] = numeric_probability

    probability_sum = sum(
        validated_distribution.values()
    )

    if not math.isclose(
        probability_sum,
        1.0,
        rel_tol=0.0,
        abs_tol=PROBABILITY_TOLERANCE,
    ):
        raise ValueError(
            f"{distribution_name} does not sum "
            "to one. Observed sum: "
            f"{probability_sum}"
        )


def _retrieve_evidence_records(
    evidence,
    evidence_key,
    unified_purpose,
):
    """
    Retrieve and standardise one NTS evidence
    component for a unified trip purpose.
    """
    if evidence_key not in evidence:
        raise KeyError(
            f"Missing evidence key "
            f"'{evidence_key}' for unified "
            f"purpose '{unified_purpose}'."
        )

    return _convert_evidence_records_to_list(
        evidence_records=evidence[
            evidence_key
        ],
        evidence_name=(
            f"{evidence_key} for "
            f"{unified_purpose}"
        ),
    )


# ==========================================
# Distribution Extraction
# ==========================================

def _extract_trip_purpose_distribution(
    demographic_profile,
    assembled_nts_evidence,
):
    """
    Extract the NTS0611a trip-purpose
    distribution matching the individual's
    age and gender.
    """
    trip_purpose_distribution = {}

    for (
        unified_purpose,
        evidence,
    ) in assembled_nts_evidence.items():

        nts0611a_profiles = (
            _retrieve_evidence_records(
                evidence=evidence,
                evidence_key=(
                    NTS0611A_EVIDENCE_KEY
                ),
                unified_purpose=(
                    unified_purpose
                ),
            )
        )

        matching_profiles = [
            nts0611a_profile
            for nts0611a_profile
            in nts0611a_profiles
            if (
                nts0611a_profile.get("Age")
                == demographic_profile["Age"]
            )
            and (
                nts0611a_profile.get("Gender")
                == demographic_profile["Gender"]
            )
        ]

        if len(matching_profiles) != 1:
            raise ValueError(
                "Expected exactly one NTS0611a "
                "trip-purpose profile for "
                f"purpose={unified_purpose}, "
                f"age={demographic_profile['Age']}, "
                "and gender="
                f"{demographic_profile['Gender']}; "
                f"found {len(matching_profiles)}."
            )

        matching_profile = matching_profiles[0]

        if (
            "Trip Purpose Probability"
            not in matching_profile
        ):
            raise KeyError(
                "Missing 'Trip Purpose Probability' "
                "in the matching NTS0611a profile "
                f"for {unified_purpose}."
            )

        trip_purpose_distribution[
            unified_purpose
        ] = float(
            matching_profile[
                "Trip Purpose Probability"
            ]
        )

    _validate_probability_distribution(
        distribution=(
            trip_purpose_distribution
        ),
        distribution_name=(
            "Original NTS0611a trip-purpose "
            "distribution"
        ),
    )

    return trip_purpose_distribution


def _extract_probability_fields(
    evidence_profile,
):
    """
    Remove source-identification fields and
    retain only probability fields.
    """
    return {
        category: float(probability)
        for category, probability
        in evidence_profile.items()
        if category
        not in NON_PROBABILITY_FIELDS
    }


def _extract_purpose_conditioned_distributions(
    unified_purpose,
    evidence,
):
    """
    Extract the NTS0502b temporal distribution
    and NTS0409a travel-mode distribution for
    one unified trip purpose.
    """
    nts0502b_profiles = (
        _retrieve_evidence_records(
            evidence=evidence,
            evidence_key=(
                NTS0502B_EVIDENCE_KEY
            ),
            unified_purpose=unified_purpose,
        )
    )

    nts0409a_profiles = (
        _retrieve_evidence_records(
            evidence=evidence,
            evidence_key=(
                NTS0409A_EVIDENCE_KEY
            ),
            unified_purpose=unified_purpose,
        )
    )

    if len(nts0502b_profiles) != 1:
        raise ValueError(
            "Expected exactly one NTS0502b "
            "temporal profile for "
            f"purpose={unified_purpose}; "
            f"found {len(nts0502b_profiles)}."
        )

    if len(nts0409a_profiles) != 1:
        raise ValueError(
            "Expected exactly one NTS0409a "
            "travel-mode profile for "
            f"purpose={unified_purpose}; "
            f"found {len(nts0409a_profiles)}."
        )

    temporal_distribution = (
        _extract_probability_fields(
            nts0502b_profiles[0]
        )
    )

    travel_mode_distribution = (
        _extract_probability_fields(
            nts0409a_profiles[0]
        )
    )

    _validate_probability_distribution(
        distribution=temporal_distribution,
        distribution_name=(
            "Original NTS0502b temporal "
            f"distribution for {unified_purpose}"
        ),
    )

    _validate_probability_distribution(
        distribution=(
            travel_mode_distribution
        ),
        distribution_name=(
            "Original NTS0409a travel-mode "
            f"distribution for {unified_purpose}"
        ),
    )

    return (
        temporal_distribution,
        travel_mode_distribution,
    )


# ==========================================
# Demographic–Behavioural Integration
# ==========================================

def construct_constrained_behaviour_profile(
    demographic_profile,
    assembled_nts_evidence,
):
    """
    Construct the constrained behavioural
    representation for one feasible
    representative demographic profile.

    The returned representation contains:

    - the individual's eight demographic
      attributes;
    - a demographically constrained
      trip-purpose distribution;
    - an NTS0502b temporal distribution for
      every remaining trip purpose; and
    - a demographically constrained NTS0409a
      travel-mode distribution for every
      remaining trip purpose.

    This function does not sample a trip purpose,
    start time, or travel mode.
    """
    demographic_profile = (
        _convert_demographic_profile_to_dict(
            demographic_profile
        )
    )

    _validate_required_demographic_attributes(
        demographic_profile
    )

    if not isinstance(
        assembled_nts_evidence,
        Mapping,
    ):
        raise TypeError(
            "Assembled NTS evidence must be "
            "provided as a dictionary."
        )

    if not assembled_nts_evidence:
        raise ValueError(
            "Assembled NTS evidence is empty."
        )

    # ======================================
    # 1. Retrieve NTS0611a Distribution
    # ======================================

    original_trip_purpose_distribution = (
        _extract_trip_purpose_distribution(
            demographic_profile=(
                demographic_profile
            ),
            assembled_nts_evidence=(
                assembled_nts_evidence
            ),
        )
    )

    # ======================================
    # 2. Apply Trip-Purpose Constraints
    # ======================================

    constrained_trip_purpose_distribution = (
        apply_trip_purpose_constraint(
            profile=demographic_profile,
            trip_purpose_probabilities=(
                original_trip_purpose_distribution
            ),
        )
    )

    _validate_probability_distribution(
        distribution=(
            constrained_trip_purpose_distribution
        ),
        distribution_name=(
            "Constrained trip-purpose "
            "distribution"
        ),
    )

    # ======================================
    # 3. Construct Conditional Distributions
    # ======================================

    purpose_conditioned_distributions = {}

    for (
        unified_purpose,
        trip_purpose_probability,
    ) in (
        constrained_trip_purpose_distribution
        .items()
    ):
        if (
            unified_purpose
            not in assembled_nts_evidence
        ):
            raise KeyError(
                "No assembled NTS evidence was "
                "found for constrained purpose "
                f"'{unified_purpose}'."
            )

        evidence = assembled_nts_evidence[
            unified_purpose
        ]

        (
            temporal_distribution,
            original_travel_mode_distribution,
        ) = (
            _extract_purpose_conditioned_distributions(
                unified_purpose=(
                    unified_purpose
                ),
                evidence=evidence,
            )
        )

        constrained_travel_mode_distribution = (
            apply_travel_mode_constraint(
                age=demographic_profile["Age"],
                car_ownership=(
                    demographic_profile[
                        "Car Ownership"
                    ]
                ),
                travel_mode_probabilities=(
                    original_travel_mode_distribution
                ),
            )
        )

        _validate_probability_distribution(
            distribution=(
                constrained_travel_mode_distribution
            ),
            distribution_name=(
                "Constrained travel-mode "
                "distribution for "
                f"{unified_purpose}"
            ),
        )

        purpose_conditioned_distributions[
            unified_purpose
        ] = {
            "trip_purpose_probability": float(
                trip_purpose_probability
            ),
            "temporal_distribution": (
                temporal_distribution
            ),
            "travel_mode_distribution": (
                constrained_travel_mode_distribution
            ),
        }

    # ======================================
    # 4. Return Integrated Representation
    # ======================================

    return {
        "demographic_profile": {
            attribute: demographic_profile[
                attribute
            ]
            for attribute
            in DEMOGRAPHIC_ATTRIBUTES
        },
        "behavioural_representation": {
            "trip_purpose_distribution": (
                constrained_trip_purpose_distribution
            ),
            "purpose_conditioned_distributions": (
                purpose_conditioned_distributions
            ),
        },
    }