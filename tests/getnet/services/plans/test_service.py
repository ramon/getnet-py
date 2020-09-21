from getnet.services.plans import Service, Plan
from getnet.services.plans.plan_response import PlanResponse
from getnet.services.service import ResponseList


def test_create(client_mock, plan_sample, plan_response_sample):
    client_mock.post.return_value = plan_response_sample

    service = Service(client_mock)
    plan = service.create(Plan(**plan_sample))

    assert isinstance(plan, Plan)
    assert plan_response_sample.get("plan_id") == str(plan.plan_id)


def test_all(client_mock, plan_response_sample):
    client_mock.get.return_value = {
        "plans": [plan_response_sample, plan_response_sample, plan_response_sample],
        "page": 1,
        "limit": 100,
        "total": 3,
    }

    service = Service(client_mock)
    plans = service.all()

    assert isinstance(plans, ResponseList)
    assert 1 == plans.page
    assert 3 == plans.total
    assert plan_response_sample.get("plan_id") == str(plans[0].plan_id)


def test_get(client_mock, plan_response_sample):
    client_mock.get.return_value = plan_response_sample

    service = Service(client_mock)
    plan = service.get(plan_response_sample.get("plan_id"))

    assert isinstance(plan, PlanResponse)
    assert plan_response_sample.get("plan_id") == str(plan.plan_id)
    client_mock.get.assert_called_once_with(
        "/v1/plans/{}".format(plan_response_sample.get("plan_id"))
    )


def test_update(client_mock, plan_response_sample):
    client_mock.patch.return_value = plan_response_sample

    service = Service(client_mock)
    _ = service.update(plan_response_sample.get("plan_id"), "Demo", "Demo Desc")

    client_mock.patch.assert_called_once_with(
        "/v1/plans/{}".format(plan_response_sample.get("plan_id")),
        json={"name": "Demo", "description": "Demo Desc"},
    )


def test_update_status(client_mock, plan_response_sample):
    client_mock.patch.return_value = plan_response_sample

    service = Service(client_mock)
    _ = service.update_status(plan_response_sample.get("plan_id"), False)

    client_mock.patch.assert_called_once_with(
        "/v1/plans/{}/status/inactive".format(plan_response_sample.get("plan_id")),
    )
