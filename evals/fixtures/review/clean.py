def accepts(count, limit):
    return count >= 0 and count <= limit


def caption(count):
    return str(count)


def serve(actor, owner, count, limit):
    if actor != owner:
        raise PermissionError("owner required")
    if not accepts(count, limit):
        raise ValueError("invalid count")
    return caption(count)
