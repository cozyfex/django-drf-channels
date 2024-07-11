import ulid


def generate_ulid():
    return ulid.new().uuid
