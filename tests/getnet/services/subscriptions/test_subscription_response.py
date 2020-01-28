import unittest

sample = {
    "seller_id": "eb523ac0-10e0-4acd-96b4-24436227e5b1",
    "order_id": "test-99243222",
    "create_date": "2019-11-14T14:14:06.596Z",
    "payment_date": 14,
    "next_scheduled_date": "2019-12-14T14:14:06.955Z",
    "subscription": {
        "subscription_id": "38a3c99d-b593-42e8-b47d-53b43f9786ab",
        "payment_type": {
            "credit": {
                "transaction_type": "FULL",
                "number_installments": 1,
                "card": {
                    "card_id": "1ddc2c8d-7a76-485e-8820-39f085c92ccf",
                    "bin": "401200",
                    "cardholder_name": "John Doe",
                    "expiration_month": "02",
                    "expiration_year": "25",
                    "brand": "Visa",
                },
            }
        },
    },
    "customer": {
        "customer_id": "d0964778-0efa-4574-a171-0197f6eee62d",
        "first_name": "João",
        "last_name": "da Silva",
        "document_type": "CPF",
        "document_number": "62599366862",
        "phone_number": "5551999887766",
        "celphone_number": "5551999887766",
        "birth_date": "1976-02-21",
        "observation": "O cliente tem interesse no plano x.",
        "address": {
            "street": "Av. Brasil",
            "number": "1000",
            "complement": "Sala 1",
            "district": "São Geraldo",
            "city": "Porto Alegre",
            "state": "RS",
            "country": "Brasil",
            "postal_code": "90230060",
        },
        "email": "customer@email.com.br",
    },
    "plan": {
        "plan_id": "d5aca135-a6a4-4363-96c0-387830c0a5f9",
        "name": "Plan Demo",
        "description": "Plan Demo",
        "amount": 1990,
        "currency": "BRL",
        "payment_types": ["credit_card"],
        "sales_tax": 0,
        "product_type": "service",
        "period": {"type": "monthly", "billing_cycle": 12},
        "status": "active",
    },
    "status": "success",
    "status_details": "Assinatura Plano flex criada com sucesso",
    "end_date": "2020-10-14T14:14:06.596Z",
    "payment": {
        "payment_id": "12f35188-f156-4809-b7ea-0fe184c36984",
        "seller_id": "eb523ac0-10e0-4acd-96b4-24436227e5b1",
        "amount": 1990,
        "currency": "BRL",
        "order_id": "test-99243222",
        "status": "approved",
        "payment_received_timestamp": "2019-11-14T15:14:06Z",
        "credit": {
            "delayed": False,
            "authorization_code": "4201496141293180",
            "authorization_timestamp": "2019-11-14T15:14:06Z",
            "reason_code": "00",
            "reason_message": "transaction approved",
            "acquirer": "GETNET",
            "soft_descriptor": "",
            "brand": "visa",
            "terminal_nsu": "006185",
            "acquirer_transaction_id": "000126287044",
            "transaction_id": "4201496141293180",
        },
    },
}

sample_error = sample.copy()
sample_error.update({
    "payment": {
        "error": {
            "message": "string",
            "name": "string",
            "status_code": 0,
            "details": [
                {
                    "acquirer_transaction_id": "string",
                    "description": "string",
                    "description_detail": "string",
                    "error_code": "string",
                    "payment_id": "string",
                    "status": "string",
                    "terminal_nsu": "string"
                }
            ]
        }
    }
})


class SubscriptionResponseTest(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
