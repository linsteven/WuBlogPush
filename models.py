#coding=utf-8

class Push(object):
    def __init__(self, templateId, pushId, title, news, deals, content, originalUrl, subject=''):
        self.templateId = templateId
        self.pushId = pushId
        self.title = title
        self.news = news
        self.deals = deals 
        self.content = content
        self.originalUrl = originalUrl
        self.subject = subject
