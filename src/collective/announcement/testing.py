# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.announcement


class CollectiveAnnouncementLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.announcement)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.announcement:default')


COLLECTIVE_ANNOUNCEMENT_FIXTURE = CollectiveAnnouncementLayer()


COLLECTIVE_ANNOUNCEMENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_ANNOUNCEMENT_FIXTURE,),
    name='CollectiveAnnouncementLayer:IntegrationTesting'
)


COLLECTIVE_ANNOUNCEMENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_ANNOUNCEMENT_FIXTURE,),
    name='CollectiveAnnouncementLayer:FunctionalTesting'
)


COLLECTIVE_ANNOUNCEMENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_ANNOUNCEMENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveAnnouncementLayer:AcceptanceTesting'
)
