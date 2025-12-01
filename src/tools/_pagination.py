class CursorPagination(object):
    
    def __init__(self, items=[], meta={}):
        default_meta = {
            "page": 1,
            "max_results": 25,
            "total": 0
        }
        self._items = items
        self._meta = meta if meta else default_meta

    @property
    def current_page(self):
        return self._meta.get("page", 1)

    @current_page.setter
    def current_page(self, value):
        self._meta["page"] = value
    
    @property
    def meta(self):
        return self._meta
    
    @meta.setter
    def meta(self, value):
        self._meta = value

    @property
    def items(self):
        return self._items
    
    @property
    def items_ids(self):
        return [item['_id'] for item in self._items]
    
    def attributes_to_patch(self, dest_query):
        return [item[dest_query] for item in self._items]

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def page_size(self):
        return self._meta.get("max_results", 25)

    @property
    def get_cursor_skip(self):
        return (self.current_page - 1) * self.page_size

    @property
    def get_next_page_params(self):
        params = {
            "limit": self.page_size,
            "offset": self.current_page * self.page_size,
        }
        self.current_page += 1
        return params

    def has_more_pages(self):
        return self.current_page * self.page_size < self._meta.get("total", 0)
