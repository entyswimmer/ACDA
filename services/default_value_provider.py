from services.device_resolver import (
    DeviceResolver
)


class DefaultValueProvider:

    def __init__(
        self,
        registry,
        resolver=None
    ):

        self.registry = registry

        self.resolver = (
            resolver
            if resolver
            else DeviceResolver()
        )

    def get_defaults(
        self,
        formula_key: str,
        device,
        device_type: str
    ):

        meta = self.registry.get(
            formula_key
        )

        defaults = {}

        for item in meta["inputs"]:

            name = item["name"]

            source = item.get(
                "source"
            )

            if source:

                defaults[name] = (
                    self.resolver.get_value(
                        device,
                        device_type,
                        source
                    )
                )

            else:

                defaults[name] = None

        return defaults