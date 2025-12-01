import logging
from copy import deepcopy
from ._generic_handler import QueryHandler, ArgsHandler
from factories.query_builder import QueryBuilder
from ._pagination import CursorPagination


logger = logging.getLogger(__name__)


class TransferQueryHandler(QueryHandler):
    
    def fetch_all(self, source_query, dest_query):
        for item in deepcopy(self.pagination_handler.items):
            item["classification"][item["classification"].index(source_query["classification"])] = dest_query["classification"]
            fetch_data = dict(classification=item["classification"])
            self.database_orm.patch_single_doc(item['_id'], fetch_data)


class TransferCommandHandler(ArgsHandler):

    def get_db_instance(self):
        return QueryBuilder()

    def command_handler(self, args):
        logger.info(f"Transferring data from {args.source} to {args.dest}...")

        source_query, dest_query = self.validate_incoming_args(args)

        articles_handler = TransferQueryHandler(
            database_orm=self.get_db_instance(),
            pagination_handler=CursorPagination(),
            dest_query=dest_query
        )
        articles_handler.fetch_all_source(
            source_query
        )
        logger.info(f"Transfer complete")

transfer_handler = TransferCommandHandler()
