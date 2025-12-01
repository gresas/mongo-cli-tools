
from abc import ABC, abstractmethod


class QueryHandler(ABC):

    def __init__(
        self,
        database_orm,
        dest_query,
        pagination_handler=None
    ):
        self.database_orm = database_orm
        self.dest_query = dest_query
        self.pagination_handler = pagination_handler

    def fetch_all_source(self, source_query, projection=None, sort=None):
        while True:
            self.database_orm.get_resources(
                self.pagination_handler,
                filters=source_query,
                projection=projection,
                sort=sort
            )

            # Need store (redis) pagination and 'already transfered' information to deal with reprocessing
            self.fetch_all(source_query, self.dest_query)

            if not self.pagination_handler.has_more_pages() and not self.pagination_handler.items:
                break

    @abstractmethod
    def fetch_all(self, source_query, dest_query):
        ...


class ArgsHandler(ABC):

    def build_query(self, filter_str: str) -> dict:
        """
        Converts a string like:
            'classification:[1234124,teste],keyword_list:geral,metadata:{a:1,b:2}'
        
        Into:
            {
                'classification': ['1234124', 'teste'],
                'keyword_list': 'geral',
                'metadata': {'a': '1', 'b': '2'}
            }
        """

        if not filter_str or ":" not in filter_str:
            raise ValueError("Filter string must contain at least one key:value pair")

        query = {}
        parts = [p.strip() for p in filter_str.split(",") if p.strip()]

        for part in parts:
            if ":" not in part:
                raise ValueError(f"Invalid filter segment: '{part}'")

            key, raw_value = part.split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()

            if raw_value.startswith("[") and raw_value.endswith("]"):
                inner = raw_value[1:-1].strip()

                if inner == "":
                    values = []
                else:
                    values = [v.strip() for v in inner.split(",")]

                query[key] = values
                continue

            if raw_value.startswith("{") and raw_value.endswith("}"):
                inner = raw_value[1:-1].strip()

                if inner == "":
                    obj = {}
                else:
                    obj = {}
                    # split a:1,b:2
                    fields = [x.strip() for x in inner.split(",") if x.strip()]
                    for f in fields:
                        if ":" not in f:
                            raise ValueError(f"Invalid dict item: '{f}'")
                        k, v = f.split(":", 1)
                        obj[k.strip()] = v.strip()

                query[key] = obj
                continue

            query[key] = raw_value

        return query

    def validate_incoming_args(self, args):
        try:
            return self.build_query(args.source), self.build_query(args.dest)
        except AttributeError as e:
            raise ValueError("Missing required arguments: source and dest") from e
        except Exception as e:
            raise ValueError("Invalid arguments provided") from e
    
    @abstractmethod
    def command_handler(self, args):
        pass
