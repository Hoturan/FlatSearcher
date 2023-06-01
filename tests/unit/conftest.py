import pytest


@pytest.fixture(scope="package")
def happy_idealista_url():
    return "https://www.idealista.com/venta-viviendas/barcelona/sant-marti/el-poblenou/"


@pytest.fixture(scope="package")
def malformed_idealista_url():
    return "https://www.idealostu.com"
