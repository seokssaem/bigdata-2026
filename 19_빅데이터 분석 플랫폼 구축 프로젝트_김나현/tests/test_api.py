def create_product(client, stock=20):
    response = client.post(
        "/products",
        json={
            "sku": "P-001",
            "name": "산업용 센서",
            "unit_price": 15000,
            "reorder_point": 5,
            "initial_stock": stock,
        },
    )
    assert response.status_code == 201
    return response.json()


def create_customer(client):
    response = client.post(
        "/customers",
        json={
            "company_name": "테스트 제조",
            "business_number": "123-45-67890",
            "contact_name": "김담당",
            "contact_email": "manager@example.com",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_product_and_duplicate_sku(client):
    product = create_product(client)
    assert product["stock_quantity"] == 20

    duplicate = client.post(
        "/products",
        json={"sku": "P-001", "name": "중복", "unit_price": 1000},
    )
    assert duplicate.status_code == 409


def test_create_order_decreases_stock(client):
    product = create_product(client, stock=20)
    customer = create_customer(client)

    response = client.post(
        "/orders",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": product["id"], "quantity": 3}],
        },
    )
    assert response.status_code == 201
    assert response.json()["total_amount"] == "45000.00"

    inventory = client.get("/inventory").json()
    assert inventory[0]["quantity"] == 17


def test_order_fails_when_stock_is_insufficient(client):
    product = create_product(client, stock=2)
    customer = create_customer(client)

    response = client.post(
        "/orders",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": product["id"], "quantity": 3}],
        },
    )
    assert response.status_code == 409
    assert "재고가 부족" in response.json()["detail"]


def test_dashboard_summary(client):
    product = create_product(client, stock=4)
    customer = create_customer(client)
    client.post(
        "/orders",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": product["id"], "quantity": 1}],
        },
    )

    response = client.get("/dashboard/summary")
    assert response.status_code == 200
    assert response.json() == {
        "product_count": 1,
        "customer_count": 1,
        "order_count": 1,
        "total_sales": "15000.00",
        "low_stock_count": 1,
    }

