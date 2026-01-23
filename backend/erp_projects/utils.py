ALLOWED_TRANSITIONS = {
    'TODO': ['IN_PROGRESS'],
    'IN_PROGRESS': ['DONE'],
    'DONE': [],
}


def is_valid_status_transition(old_status, new_status):
    return new_status in ALLOWED_TRANSITIONS.get(old_status, [])
