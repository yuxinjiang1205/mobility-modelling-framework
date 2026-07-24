import pandas as pd

TRIP_PURPOSE_TO_POI_MAPPING = pd.DataFrame(

    [

        # Representative Mapping
        ["Commuting", "Representative Mapping", ["Employment"]],
        ["Business", "Representative Mapping", ["Employment"]],
        ["Visiting Friends Elsewhere", "Representative Mapping", ["Food and Beverage"]],
        ["Entertainment or Public Activity", "Representative Mapping", ["Recreation"]],
        ["Day Trip", "Representative Mapping", ["Recreation"]],
        ["Just Walk", "Representative Mapping", ["Recreation"]],

        # Direct Mapping
        ["Education", "Direct Mapping", ["Education"]],
        ["Escort Education", "Direct Mapping", ["Education"]],
        ["Shopping", "Direct Mapping", ["Retail"]],
        ["Sport: Participate", "Direct Mapping", ["Recreation"]],
        ["Holiday: Base", "Direct Mapping", ["Accommodation"]],

        # Context-dependent Mapping
        [
            "Personal Business",
            "Context-dependent Mapping",
            [
                "Healthcare",
                "Public Services",
                "Personal Services",
                "Food and Beverage",
                "Employment",
                "Recreation"
            ]
        ],

        [
            "Other Escort",
            "Context-dependent Mapping",
            [
                "Employment",
                "Retail",
                "Healthcare",
                "Personal Services",
                "Public Services",
                "Food and Beverage",
                "Recreation",
                "Accommodation"
            ]
        ],

        # Excluded Mapping
        [
            "Visiting Friends at Private Home",
            "Excluded Mapping",
            []
        ]

    ],

    columns=[
        "Unified Trip Purpose",
        "Mapping Strategy",
        "POI Categories"
    ]

)