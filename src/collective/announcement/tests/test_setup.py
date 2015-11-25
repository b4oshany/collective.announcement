# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.announcement.testing import COLLECTIVE_ANNOUNCEMENT_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.announcement is properly installed."""

    layer = COLLECTIVE_ANNOUNCEMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.announcement is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.announcement'))

    def test_browserlayer(self):
        """Test that ICollectiveAnnouncementLayer is registered."""
        from collective.announcement.interfaces import (
            ICollectiveAnnouncementLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveAnnouncementLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_ANNOUNCEMENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.announcement'])

    def test_product_uninstalled(self):
        """Test if collective.announcement is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.announcement'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveAnnouncementLayer is removed."""
        from collective.announcement.interfaces import ICollectiveAnnouncementLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveAnnouncementLayer, utils.registered_layers())
