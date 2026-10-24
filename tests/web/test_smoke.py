"""Connectivity smoke test; replace/extend after the authorized UI is surveyed."""

import pytest


@pytest.mark.smoke
@pytest.mark.web
def test_authorized_application_opens(browser):
    # This only checks that the configured page opens and has a title.
    # It is not evidence that the application's business workflows are correct.
    assert browser.title.strip(), "The page opened without a document title"
