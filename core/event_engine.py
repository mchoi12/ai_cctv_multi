def detect_event(person_count):

    if person_count >= 4:
        return "crowd", "critical"

    elif person_count >= 2:
        return "loitering", "warning"

    return "normal", "info"