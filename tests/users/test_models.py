def test_user_str(base_user):
    """Test the custom user model string representation"""
    assert base_user.__str__() == f"{base_user.username}"

def test_get_short_name(base_user):
    """Test the custom user model string representation"""
    assert base_user.get_short_name() == base_user.username


