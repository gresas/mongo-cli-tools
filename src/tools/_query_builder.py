from datetime import datetime, timezone
from pymongo import MongoClient
from tools._helpers import (
    is_instance_list,
    is_instance_dict,
    is_instance_datetime
)
from typing import List, Union, Dict, Any
from bson import ObjectId


class MongoQueryBuilder:
    
    def __init__(self, uri, db_name, collection):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.col = self.db[collection]

    def format_eve_date(self, dt: datetime) -> str:
        """Format type: 'Wed, 28 Oct 2025 00:00:00 GMT'"""
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

    def format_iso_date(self, dt: datetime) -> str:
        """Format Type: '2017-06-06T22:49:00.000+00:00'"""
        return dt.astimezone(timezone.utc).isoformat()

    def include_filters(self, query: dict) -> dict:
        mongo_filter = {}

        if not is_instance_dict(query):
            raise ValueError("Query must be a dict type")

        if "classification" in query:
            classification_source_query = query["classification"]
            mongo_filter["classification"] = {"$in":
                classification_source_query if is_instance_list(classification_source_query)
                else [classification_source_query]
            }
        
        if "tags" in query:
            tags_source_query = query["keyword_list"]
            mongo_filter["keyword_list"] = {"$in":
                tags_source_query if is_instance_list(tags_source_query)
                else [tags_source_query]
            }

        if "_created" in query and is_instance_datetime(query["_created"]):
            mongo_filter["_created"] = {"$gte": query["_created"]}

        # mongo_filter["_deleted"] = False
        return mongo_filter
    
    def patch_documents_by_ids(
        self,
        ids: List[Union[str, ObjectId]],
        patch_data: Dict[str, Any],
    ) -> Dict[str, int]:
        """
        Patch documents in a MongoDB collection using a list of _ids.
        
        Args:
            ids (List[Union[str, ObjectId]]): List of IDs to patch.
            patch_data (Dict[str, Any]): Fields to update (inside $set automatically).
        
        Returns:
            dict: Summary -> { matched, modified }
        """

        if not ids:
            return {"matched": 0, "modified": 0}

        converted_ids = []
        for value in ids:
            if isinstance(value, ObjectId):
                converted_ids.append(value)
            else:
                converted_ids.append(ObjectId(str(value)))

        result = self.col.update_many(
            {"_id": {"$in": converted_ids}},
            {"$set": patch_data},
        )

        return {
            "matched": result.matched_count,
            "modified": result.modified_count,
        }

    def patch_single_doc(self, id, patch_data):
        result = self.col.update_one(
            {"_id": id},
            {"$set": patch_data}
        )

        return {
            "matched": result.matched_count,
            "modified": result.modified_count,
        }

    def get_resources(self, pagination_handler, filters=None, projection=None, sort=None):
        """
        Retrieve paginated resources from the MongoDB collection.

        This method applies optional filters, projection, and sorting, then returns
        a paginated list of documents along with updated pagination metadata.

        Args:
            pagination_handler: An object responsible for tracking pagination state.
            filters (dict, optional): Raw filters provided externally.
            projection (dict, optional): Fields to include/exclude in the query.
            sort (tuple, optional): Tuple (field, direction) used to sort results.

        Returns:
            None. Updates `pagination_handler.items` and `pagination_handler.meta` in place.
        """
        filters = filters or {}
        mongo_query = self.include_filters(filters)

        skip = pagination_handler.get_cursor_skip
        limit = pagination_handler.page_size
        cursor = self.col.find(
            mongo_query,
            limit=limit,
            skip=skip,
            projection=projection
        )

        if sort:
            cursor = cursor.sort(sort[0], sort[1])

        total = cursor.count_documents() if hasattr(cursor, "count_documents") else self.col.count_documents(mongo_query)
        items = list(cursor.skip(skip).limit(limit))

        new_meta = {
            "page": pagination_handler.current_page,
            "next_page": pagination_handler.current_page + 1,
            "max_results": pagination_handler.page_size,
            "total": total
        }

        pagination_handler.items = items
        pagination_handler.meta = new_meta

    def get_resource_by_id(self, resource_id):
        if not isinstance(resource_id, ObjectId):
            resource_id = ObjectId(str(resource_id))

        result = self.col.find_one(
            {"_id": resource_id}
        )
        return result
