"""
Paymob payment gateway integration utilities.
"""

import requests
import hmac
import hashlib
from django.conf import settings


class PaymobAPI:
    """Paymob API integration class."""

    BASE_URL = "https://accept.paymob.com/api"

    def __init__(self):
        self.api_key = settings.PAYMOB_API_KEY
        self.integration_id = settings.PAYMOB_INTEGRATION_ID
        self.iframe_id = settings.PAYMOB_IFRAME_ID
        self.hmac_secret = settings.PAYMOB_HMAC_SECRET

    def authenticate(self):
        """Authenticate with Paymob and get token."""
        url = f"{self.BASE_URL}/auth/tokens"
        data = {"api_key": self.api_key}

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json().get('token')
        except requests.exceptions.RequestException as e:
            print(f"Paymob authentication error: {e}")
            return None

    def create_order(self, auth_token, amount_cents):
        """Create an order."""
        url = f"{self.BASE_URL}/ecommerce/orders"
        data = {
            "auth_token": auth_token,
            "delivery_needed": "false",
            "amount_cents": int(amount_cents * 100),  # Convert to cents
            "currency": "EGP",
            "items": []
        }

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Paymob order creation error: {e}")
            return None

    def generate_payment_key(self, auth_token, order_id, amount_cents, billing_data):
        """Generate payment key."""
        url = f"{self.BASE_URL}/acceptance/payment_keys"
        data = {
            "auth_token": auth_token,
            "amount_cents": int(amount_cents * 100),
            "expiration": 3600,
            "order_id": order_id,
            "billing_data": billing_data,
            "currency": "EGP",
            "integration_id": self.integration_id
        }

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json().get('token')
        except requests.exceptions.RequestException as e:
            print(f"Paymob payment key error: {e}")
            return None

    def verify_hmac(self, data):
        """Verify HMAC signature from webhook."""
        hmac_fields = [
            'amount_cents', 'created_at', 'currency', 'error_occured',
            'has_parent_transaction', 'id', 'integration_id', 'is_3d_secure',
            'is_auth', 'is_capture', 'is_refunded', 'is_standalone_payment',
            'is_voided', 'order', 'owner', 'pending', 'source_data_pan',
            'source_data_sub_type', 'source_data_type', 'success'
        ]

        concatenated = ''.join(str(data.get(field, '')) for field in hmac_fields)
        calculated_hmac = hmac.new(
            self.hmac_secret.encode(),
            concatenated.encode(),
            hashlib.sha512
        ).hexdigest()

        return calculated_hmac == data.get('hmac')

    def initiate_payment(self, amount, user, transaction_id):
        """
        Initiate payment process.

        Args:
            amount: Amount in EGP
            user: User object
            transaction_id: Transaction ID

        Returns:
            str: Payment iframe URL or None
        """
        # Authenticate
        auth_token = self.authenticate()
        if not auth_token:
            return None

        # Create order
        order = self.create_order(auth_token, amount)
        if not order:
            return None

        # Prepare billing data
        billing_data = {
            "apartment": "NA",
            "email": user.email,
            "floor": "NA",
            "first_name": user.first_name,
            "street": "NA",
            "building": "NA",
            "phone_number": user.phone_number or "NA",
            "shipping_method": "NA",
            "postal_code": "NA",
            "city": user.country,
            "country": user.country,
            "last_name": user.last_name,
            "state": "NA"
        }

        # Generate payment key
        payment_token = self.generate_payment_key(
            auth_token,
            order['id'],
            amount,
            billing_data
        )

        if not payment_token:
            return None

        # Return iframe URL
        return f"https://accept.paymobsolutions.com/api/acceptance/iframes/{self.iframe_id}?payment_token={payment_token}"


def process_paymob_callback(callback_data):
    """
    Process Paymob webhook callback.

    Args:
        callback_data: Callback data from Paymob

    Returns:
        dict: Processed payment information
    """
    paymob = PaymobAPI()

    # Verify HMAC
    if not paymob.verify_hmac(callback_data):
        return {'success': False, 'error': 'Invalid HMAC'}

    return {
        'success': callback_data.get('success', False),
        'transaction_id': callback_data.get('merchant_order_id'),
        'payment_id': callback_data.get('id'),
        'amount': callback_data.get('amount_cents', 0) / 100,
        'currency': callback_data.get('currency'),
        'status': 'completed' if callback_data.get('success') else 'failed'
    }
