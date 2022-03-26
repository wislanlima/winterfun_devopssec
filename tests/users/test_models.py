import pytest


def test_user_str(base_user):
    """Test the custom user model string representation"""
    assert base_user.__str__() == f"{base_user.username}"


