from datetime import datetime

from plone.app.layout.viewlets import ViewletBase
from plone import api
from zope.component import ComponentLookupError
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getMultiAdapter
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.api.exc import InvalidParameterError


class AnnouncementViewlet(ViewletBase):
    """ viewlet that displays announcements """

    def data(self):
        _data = {"show_here":False}
        prefix = "site_announcement"
        fields = ["site_announcement",
                  "show_on_all_pages",
                  "expire_on",
                  "show_announcement"]

        #import pdb; pdb.set_trace()
        try:
            announcements = self.get_registry_entry("%s.announcements" % prefix)
            if not announcements:
                return _data
            _data = announcements[0]
        except InvalidParameterError:
            return _data

        try:
            _data["show_here"] = datetime.now() <= _data["expire_on"]
        except TypeError:
            _data["show_here"] = True
        return _data

    def get_registry_entry(self,entry):
        _entry = None
        try:
            _entry = api.portal.get_registry_record(entry)
        except ComponentLookupError:
            pass
        return _entry

    def is_front_page(self):
        """
        Check if the viewlet is on a front page.
        Handle canonical paths correctly.
        based on docs: 
        http://docs.plone.org/develop/plone/serving/traversing.html#checking-if-an-item-is-the-site-front-page
        """
        # Get path with "Default content item" wrapping applied
        context_helper = getMultiAdapter((self.context, self.request), 
                                                 name="plone_context_state")
        canonical = context_helper.canonical_object()
        path = canonical.absolute_url_path()
        return INavigationRoot.providedBy(canonical)