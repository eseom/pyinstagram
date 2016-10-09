from pyinstagram.module.printable import Printable


class UserTagsResponse(Printable):
    def __init__(self, more_available, auto_load_more_enabled, total_count,
                 items, requires_review, new_photos, num_results):
        self.more_available = more_available
        self.auto_load_more_enabled = auto_load_more_enabled
        self.total_count = total_count
        self.items = items
        self.requires_review = requires_review
        self.new_photos = new_photos
        self.num_results = num_results
