from unittest import mock

from superai import Client


def test_get_user():
    user_data = {
        "email": "test@example.com",
        "active": True,
        "id": "123",
        "created": "2023-03-23T13:02:47.285+00:00",
        "sysAdmin": False,
        "groups": [],
        "plan": "FREEMIUM",
        "username": "test_user",
        "backofficeAdmin": False,
        "trialDays": 30,
        "organizationMemberships": [],
    }
    with mock.patch.object(Client, "request", return_value=user_data):
        client = Client.from_credentials()
        user = client.get_user()
        assert user
        assert user.email == user_data["email"]
        assert user.active == user_data["active"]

    user_data["organizationMemberships"] = [
        {
            "id": 2222,
            "status": "ACTIVE",
            "role": "MEMBER",
            "invited": "2023-08-17T09:59:52.926000+00:00",
            "accepted": "2023-08-17T10:00:13.596000+00:00",
            "created": "2023-08-17T09:59:52.926000+00:00",
            "orgId": 1111,
            "orgUsername": "testorg",
            "userId": 123,
            "userEmail": "test@example.com",
        },
    ]
    with mock.patch.object(Client, "request", return_value=user_data):
        client = Client.from_credentials()
        user = client.get_user()
        assert user
        assert user.organizationMemberships
        assert len(user.organizationMemberships) == 1
        assert user.organizationMemberships[0].orgUsername == "testorg"
