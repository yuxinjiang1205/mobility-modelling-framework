from copy import deepcopy


def apply_trip_purpose_constraint(
    profile,
    trip_purpose_probabilities,
):
    constrained = deepcopy(
        trip_purpose_probabilities
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


def apply_travel_mode_constraint(
    age,
    car_ownership,
    travel_mode_probabilities,
):
    constrained = deepcopy(travel_mode_probabilities)

    young_age_groups = {"0-4", "5-11"}
    no_household_car = (
        car_ownership == "No cars or vans in household"
    )

    modes_to_remove = set()

    # Young children cannot drive a car or motorcycle.
    if age in young_age_groups:
        modes_to_remove.update({
            "Car or van driver",
            "Motorcycle",
        })

    # A household without a car cannot support car-driver travel.
    if no_household_car:
        modes_to_remove.update({
            "Car or van driver",
            "Car or van passenger",
        })

    # Preserve unaffected distributions exactly as they are.
    if not modes_to_remove:
        return constrained

    for mode in modes_to_remove:
        constrained.pop(mode, None)

    total = sum(constrained.values())

    if total <= 0:
        raise ValueError(
            "No feasible travel-mode probability remains."
        )

    return {
        mode: probability / total
        for mode, probability in constrained.items()
    }