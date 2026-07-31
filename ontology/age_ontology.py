def AGE_GROUP(age):
    if age <= 4:
        return "0-4"
    elif age <= 11:
        return "5-11"
    elif age <= 17:
        return "12-17"
    elif age <= 22:
        return "18-22"
    elif age <= 34:
        return "23-34"
    elif age <= 49:
        return "35-49"
    elif age <= 64:
        return "50-64"
    elif age <= 74:
        return "65-74"
    else:
        return "75+"
    
AGE_ORDER = [ "0-4",
             "5-11",
             "12-17",
             "18-22",
             "23-34",
             "35-49",
             "50-64",
             "65-74",
             "75+"]