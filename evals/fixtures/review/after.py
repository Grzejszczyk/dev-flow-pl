def accepts(count, limit):
    return 0 <= count < limit


def caption(count):
    return str(count)


def serve(actor, owner, count, limit):
    if actor != owner:
        raise PermissionError("owner required")
    if not accepts(count, limit):
        raise ValueError("invalid count")
    return caption(count)
