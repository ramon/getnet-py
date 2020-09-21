import pytest

from getnet.errors import NotFound
from getnet.services.plans import Service, Plan
from getnet.services.service import ResponseList


@pytest.mark.vcr
def test_create(client, plan_sample):
    plan = Service(client).create(Plan(**plan_sample))
    assert isinstance(plan, Plan)
    assert plan.plan_id is not None


@pytest.mark.vcr
def test_get(client, plan_sample):
    created_plan = Service(client).create(Plan(**plan_sample))

    plan = Service(client).get(created_plan.plan_id)

    assert isinstance(plan, Plan)
    assert created_plan == plan
    assert created_plan.plan_id == plan.plan_id


@pytest.mark.vcr
def test_invalid_get(client):
    with pytest.raises(NotFound) as excinfo:
        Service(client).get("14a2ce5d-ebc3-49dc-a516-cb5239b02285")

    assert excinfo.value.error_code == "404"


@pytest.mark.vcr
def test_all(client):
    plans = Service(client).all()

    assert isinstance(plans, ResponseList)
    assert plans.page == 1
    assert plans.limit == 100
    assert plans.total is not None


@pytest.mark.vcr
def test_all_not_found(client):
    plans = Service(client).all(name="foobarTest123")
    assert plans.total == 0


@pytest.mark.vcr
def test_update(client, plan_sample):
    created_plan = Service(client).create(Plan(**plan_sample))

    plan1 = Service(client).update(
        created_plan.plan_id, "FooBar #1", created_plan.description
    )
    assert plan1.name == "FooBar #1"

    plan2 = Service(client).update(created_plan, "FooBar #2")
    assert plan2.name == "FooBar #2"

    created_plan.name = "FooBar #3"
    plan3 = Service(client).update(created_plan)
    assert plan3.name == "FooBar #3"


@pytest.mark.vcr
def test_update_status(client, plan_sample):
    created_plan = Service(client).create(Plan(**plan_sample))
    assert created_plan.is_active is True

    plan = Service(client).update_status(created_plan.plan_id, False)
    assert plan.is_active is False
