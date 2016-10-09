from pyinstagram.module.printable import Printable


class Inbox(Printable):
    def __init__(self, unseen_count, has_older, unseen_count_ts, threads):
        self.unseen_count = unseen_count
        self.has_older = has_older
        self.unseen_count_ts = unseen_count_ts
        self.threads = threads


class V2InboxResponse(Printable):
    def __init__(self, pending_requests_total, seq_id, pending_requests_users,
                 inbox, subscription):
        self.pending_requests_total = pending_requests_total
        self.seq_id = seq_id
        self.pending_requests_users = pending_requests_users
        self.inbox = Inbox(**inbox)
        self.subscription = subscription
