class GrapheneMixin:
    @property
    def gid(self) -> str:
        try:
            from graphql_relay import to_global_id
        except ImportError:
            return None

        return to_global_id(f"{self.__class__.__name__}Node", self.id)

    @classmethod
    def retrieve_id(cls, gid) -> int:
        try:
            from graphql_relay import from_global_id

            object_type, object_id = from_global_id(gid)
            if object_type != f"{cls.__name__}Node":
                raise ValueError(
                    f"Passed ID [{object_type}] does not belong to class: {cls.__name__}Node"
                )
            return int(object_id)
        except ImportError:
            raise
