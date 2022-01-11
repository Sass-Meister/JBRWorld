# This is a file to store utility functions that could see use in any section of the code.


def isnum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


# There is no good way to determine if a dict with a lot of nested dicts has the fields you're looking for. Mainly used
# for testing jsons. This function takes in a dict and the fields in order and tests if they exist. Fields can be either
# strings or array indexes and returns a bool if those fields in that order could be accessed.
def dictverify(data:dict, *fields) -> bool:
    for field in fields:
        if data is None:
            return False

        elif field in data:
            data = data[field]

        elif isnum(field) and len(data) > field:
            data = data[field]

        else:
            return False

    return True