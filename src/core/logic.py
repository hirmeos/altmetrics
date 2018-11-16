from enum import IntEnum


# TODO: NOT USED SO PROB GET RID OF IT.
# Create Enums from ORIGINS/PLUGINS
def create_enum(name, items_iterable):
    items = " ".join([item for item in items_iterable])
    return IntEnum(name, items, module=__name__)
