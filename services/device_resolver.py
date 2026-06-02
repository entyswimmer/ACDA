class DeviceResolver:

    def get_value(
        self,
        device,
        device_type: str,
        parameter: str
    ):

        if not hasattr(device, device_type):
            raise ValueError(
                f"Unknown device type: {device_type}"
            )

        target = getattr(
            device,
            device_type
        )

        if not hasattr(target, parameter):
            raise ValueError(
                f"Unknown parameter: {parameter}"
            )

        return getattr(
            target,
            parameter
        )