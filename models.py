#coding=utf-8

class Push(object):
    def __init__(self, template_id, push_id, title, news, deals, changes,
                 content, original_url, subject=''):
        self.template_id = template_id
        self.push_id = push_id
        self.title = title
        self.news = news
        self.deals = deals
        self.changes = changes
        self.content = content
        self.original_url = original_url
        self.subject = subject
