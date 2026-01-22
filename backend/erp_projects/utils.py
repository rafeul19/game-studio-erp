ALLOWED_TRANSITIONS = {
    'TODO': ['IN_PROGRESS'],
    'IN_PROGRESS': ['REVIEW', 'TODO'],
    'REVIEW': ['DONE', 'IN_PROGRESS'],
    'DONE': ['REVIEW', 'IN_PROGRESS'],
}


def is_valid_status_transition(old_status, new_status):
    if old_status == new_status:
        return True
    return new_status in ALLOWED_TRANSITIONS.get(old_status, [])
