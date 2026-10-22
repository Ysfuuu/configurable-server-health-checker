from server_health import check_status


def test_status_is_ok():
    assert check_status(50, 80, 90) == "OK"


def test_status_is_warning():
    assert check_status(85, 80, 90) == "WARNING"


def test_status_is_critical():
    assert check_status(95, 80, 90) == "CRITICAL"


def test_status_at_warning_threshold():
    assert check_status(80, 80, 90) == "WARNING"


def test_status_at_critical_threshold():
    assert check_status(90, 80, 90) == "CRITICAL"   