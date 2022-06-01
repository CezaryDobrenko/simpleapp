def get_current_user(context):
    user = context.user
    if not user.is_authenticated:
        raise Exception("Authentication credentials were not provided")
    return user


def reformat_duration(duration):
    duration_string = str(duration)
    for days_reformat in [" days, ", " day, "]:
        duration_string = duration_string.replace(days_reformat, ":")
    for hours_reformat in range(0, 10):
        duration_string = duration_string.replace(
            f":{hours_reformat}:", f":0{hours_reformat}:"
        )
    return duration_string
