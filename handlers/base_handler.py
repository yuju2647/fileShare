#!usr/bin/env python
# coding=utf-8

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        self.user_ib_service = None
        self.user_omnibus_service = None
        self.report_service_sort_users = None
        self.report_service_group_invites = None

    def get_user_ib_service(self):
        if not self.user_ib_service:
            self.user_ib_service = UserIbService(self.application)
        return self.user_ib_service

    def get_user_omnibus_service(self):
        if not self.user_omnibus_service:
            self.user_omnibus_service = UserOmnibusService(self.application)
        return self.user_omnibus_service

    def get_report_service_sort_users(self, start_date, end_date):
        if not self.report_service_sort_users:
            self.report_service_sort_users = ReportServiceSortUsers(self.application, start_date, end_date)
        return self.report_service_sort_users

    def get_report_service_group_invites(self, start_date, end_date):
        if not self.report_service_group_invites:
            self.report_service_group_invites = ReportServiceGroupInvites(self.application, start_date, end_date)
        return self.report_service_group_invites
