from edadildo import parse_vers_0


def test_cheese():
    assert parse_vers_0("Сыр") == "Цена товара: 150 рублей"

def test_sausage():
    assert parse_vers_0("Сосиски") == "Цена товара: 100 рублей"

def test_tvorog():
    assert parse_vers_0("Творог") == "Цена товара: 44 рублей"

#Тесты релевантны только 07.12.2024 в Одинцово, так как работают относительно непостоянных данных
