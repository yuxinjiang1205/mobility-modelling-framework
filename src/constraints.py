from copy import deepcopy

def apply_trip_purpose_constraint(
    profile,
    trip_purpose_distribution,
):
    constrained = deepcopy(
        trip_purpose_distribution
    )

    if profile["Industry"] == "Does not apply":
        constrained.pop("Commuting", None)
        constrained.pop("Business", None)

    elif (
        profile["Distance travelled to work"]
        == "Works mainly from home"
    ):
        constrained.pop("Commuting", None)

    else:
        return constrained

    total = sum(constrained.values())

    if total <= 0:
        raise ValueError(
            "No feasible trip-purpose "
            "probability remains."
        )

    return {
        purpose: probability / total
        for purpose, probability
        in constrained.items()
    }

# AI Collaboration Record
# Tool: ChatGPT (OpenAI)
# Purpose: Add a study-area-based geographic travel-mode constraint.
# Prompt summary: Retain the original NTS0409a London-specific travel-mode
# categories, but modify the travel-mode constraint and demographic-behavioural
# integration functions so that “Bus in London” and “London Underground” are
# removed for non-London study areas. Renormalise the remaining mode
# probabilities to sum to one and validate their removal for Manchester.


LONDON_SPECIFIC_MODES = {
    "Bus in London",
    "London Underground",
}


def apply_travel_mode_constraint(
    age,
    car_ownership,
    travel_mode_distribution,
    study_area,
):
    constrained = deepcopy(
        travel_mode_distribution
    )

    young_age_groups = {
        "0-4",
        "5-11",
    }

    no_household_car = (
        car_ownership
        == "No cars or vans in household"
    )

    normalised_study_area = (
        study_area.strip().casefold()
    )

    modes_to_remove = set()

    # Remove London-specific modes
    # when the study area is not London.
    if normalised_study_area != "london":
        modes_to_remove.update(
            LONDON_SPECIFIC_MODES
        )

    # Young children cannot drive
    # a car or motorcycle.
    if age in young_age_groups:
        modes_to_remove.update({
            "Car or van driver",
            "Motorcycle",
        })

    # A household without a car cannot
    # support car-based travel.
    if no_household_car:
        modes_to_remove.update({
            "Car or van driver",
            "Car or van passenger",
        })

    # Preserve unaffected distributions.
    if not modes_to_remove:
        return constrained

    for mode in modes_to_remove:
        constrained.pop(mode, None)

    total = sum(constrained.values())

    if total <= 0:
        raise ValueError(
            "No feasible travel-mode "
            "probability remains."
        )

    return {
        mode: probability / total
        for mode, probability
        in constrained.items()
    }