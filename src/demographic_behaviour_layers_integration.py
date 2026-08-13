import math
from collections.abc import Mapping

from .constraints import apply_trip_purpose_constraint, apply_travel_mode_constraint


DEMOGRAPHIC_ATTRIBUTES = (
    "Age",
    "Sex",
    "Household Type",
    "Economic Activity Status",
    "Industry",
    "Ethnic Group",
    "Distance travelled to work",
    "Car Ownership",
)
NON_PROBABILITY_FIELDS = {"Year", "Purpose", "Trip purpose"}
NTS0611A_EVIDENCE_KEY = "nts0611a_trip_purpose_distribution"
NTS0502B_EVIDENCE_KEY = "nts0502b_temporal_distribution"
NTS0409A_EVIDENCE_KEY = "nts0409a_travel_mode_distribution"
PROBABILITY_TOLERANCE = 1e-8


def convert_representative_profile_to_dict(representative_profile):

    """Convert a mapping or pandas Series-like profile to a dictionary."""

    if isinstance(representative_profile, Mapping):
        return dict(representative_profile)
    if hasattr(representative_profile, "to_dict"):
        converted = representative_profile.to_dict()
        if isinstance(converted, Mapping):
            return dict(converted)
    raise TypeError(
        "Representative profile must be a mapping or have a to_dict() method; "
        f"received {type(representative_profile).__name__}."
    )


def convert_nts_evidence_distribution_to_list(evidence_records, evidence_name):

    """Convert JSON records or a DataFrame-like object to dictionaries."""

    records = evidence_records
    if not isinstance(records, list) and hasattr(records, "to_dict"):
        try:
            records = records.to_dict(orient="records")
        except TypeError:
            records = records.to_dict()
    if not isinstance(records, list):
        raise TypeError(f"{evidence_name} must be a list or DataFrame-like object.")
    invalid = [i for i, record in enumerate(records) if not isinstance(record, Mapping)]
    if invalid:
        raise TypeError(f"{evidence_name} has non-dictionary records at {invalid}.")
    return [dict(record) for record in records]


def validate_required_demographic_attributes(representative_profile):
    missing = [key for key in DEMOGRAPHIC_ATTRIBUTES if key not in representative_profile]
    if missing:
        raise ValueError(f"Demographic profile is missing: {missing}")


def validate_probability_distribution(distribution, distribution_name):

    """Require a non-empty, finite, non-negative distribution summing to one."""
    
    if not isinstance(distribution, Mapping):
        raise TypeError(f"{distribution_name} must be a dictionary.")
    if not distribution:
        raise ValueError(f"{distribution_name} is empty.")

    try:
        probabilities = [float(value) for value in distribution.values()]
    except (TypeError, ValueError) as error:
        raise TypeError(f"{distribution_name} contains a non-numeric probability.") from error
    if not all(math.isfinite(value) and value >= 0 for value in probabilities):
        raise ValueError(f"{distribution_name} contains a negative or non-finite probability.")
    if not math.isclose(sum(probabilities), 1.0, rel_tol=0, abs_tol=PROBABILITY_TOLERANCE):
        raise ValueError(f"{distribution_name} sums to {sum(probabilities)}, not one.")


def retrieve_evidence_records(evidence, evidence_key, shared_trip_purpose):
    if evidence_key not in evidence:
        raise KeyError(
            f"Missing evidence key '{evidence_key}' for purpose '{shared_trip_purpose}'."
        )
    return convert_nts_evidence_distribution_to_list(
        evidence[evidence_key], f"{evidence_key} for {shared_trip_purpose}"
    )


def extract_trip_purpose_distribution(
    representative_profile, assembled_behavioural_evidence
):
    distribution = {}
    for purpose, evidence in assembled_behavioural_evidence.items():
        records = retrieve_evidence_records(evidence, NTS0611A_EVIDENCE_KEY, purpose)
        matches = [
            record
            for record in records
            if record.get("Age") == representative_profile["Age"]
            and record.get("Sex") == representative_profile["Sex"]
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Expected one NTS0611a record for {purpose}, "
                f"age={representative_profile['Age']}, "
                f"Sex={representative_profile['Sex']}; found {len(matches)}."
            )
        try:
            distribution[purpose] = float(matches[0]["Trip Purpose Probability"])
        except KeyError as error:
            raise KeyError(
                f"Missing 'Trip Purpose Probability' for {purpose}."
            ) from error

    validate_probability_distribution(distribution, "Trip-purpose distribution")
    return distribution


def extract_probability_fields(behavioural_evidence):
    return {
        key: float(value)
        for key, value in behavioural_evidence.items()
        if key not in NON_PROBABILITY_FIELDS
    }


def extract_conditioned_trip_purpose_distribution(shared_trip_purpose, evidence):
    trip_purpose = shared_trip_purpose
    temporal = retrieve_evidence_records(evidence, NTS0502B_EVIDENCE_KEY, trip_purpose)
    travel_mode = retrieve_evidence_records(evidence, NTS0409A_EVIDENCE_KEY, trip_purpose)
    if len(temporal) != 1 or len(travel_mode) != 1:
        raise ValueError(
            f"Expected one temporal and one travel-mode record for {trip_purpose}; "
            f"found {len(temporal)} and {len(travel_mode)}."
        )

    temporal_distribution = extract_probability_fields(temporal[0])
    mode_distribution = extract_probability_fields(travel_mode[0])
    validate_probability_distribution(temporal_distribution, f"Temporal distribution for {trip_purpose}")
    validate_probability_distribution(mode_distribution, f"Travel-mode distribution for {trip_purpose}")
    return temporal_distribution, mode_distribution


def construct_constrained_behaviour_representation(
    representative_profile, assembled_behavioural_evidence
):
    """Combine one demographic profile with constrained NTS distributions."""
    profile = convert_representative_profile_to_dict(representative_profile)
    validate_required_demographic_attributes(profile)
    if not isinstance(assembled_behavioural_evidence, Mapping):
        raise TypeError("Assembled behavioural evidence must be a dictionary.")
    if not assembled_behavioural_evidence:
        raise ValueError("Assembled behavioural evidence is empty.")

    trip_purpose = extract_trip_purpose_distribution(
        profile, assembled_behavioural_evidence
    )
    trip_purpose = apply_trip_purpose_constraint(
        profile=profile, trip_purpose_distribution=trip_purpose
    )
    validate_probability_distribution(trip_purpose, "Constrained trip-purpose distribution")

    conditioned_purpose = {}
    for purpose, probability in trip_purpose.items():
        if purpose not in assembled_behavioural_evidence:
            raise KeyError(f"No assembled evidence for constrained purpose '{purpose}'.")
        temporal, travel_modes = extract_conditioned_trip_purpose_distribution(
            purpose, assembled_behavioural_evidence[purpose]
        )
        travel_modes = apply_travel_mode_constraint(
            age=profile["Age"],
            car_ownership=profile["Car Ownership"],
            travel_mode_distribution=travel_modes,
        )
        validate_probability_distribution(travel_modes, f"Constrained travel modes for {purpose}")
        conditioned_purpose[purpose] = {
            "trip_purpose_probability": float(probability),
            "temporal_distribution": temporal,
            "travel_mode_distribution": travel_modes,
        }

    return {
        "demographic_profile": {key: profile[key] for key in DEMOGRAPHIC_ATTRIBUTES},
        "behavioural_representation": {
            "trip_purpose_distribution": trip_purpose,
            "conditioned_trip_purpose_distribution": conditioned_purpose,
        },
    }