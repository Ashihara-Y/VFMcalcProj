import os
from dotenv import load_dotenv
import stripe
import flet as ft
from google.cloud import firestore
from fastapi import Request, HTTPException

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

db = firestore.Client()

class PaymentManager:
    @staticmethod
    def create_checkout_session(user_sub: str, user_email: str) -> str:
        # ユーザーをStripeの決済ページへ誘導するURLを発行
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': os.getenv("STRIPE_PRICE_ID"),
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=os.getenv("STRIPE_SUCCESS_URL"),
            cancel_url=os.getenv("STRIPE_CANCEL_URL"),
            client_reference_id=user_sub,
            customer_email=user_email
        )

        return session.url

    @staticmethod
    async def handle_webhook(request: Request):
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, ENDPOINT_SECRET
            )
            return event
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            # Invalid signature
            raise HTTPException(status_code=400, detail=str(e))

        # Handle the event
        #if event['type'] == 'checkout.session.completed':
        #    session = event['data']['object']
        #    user_sub = session.get('client_reference_id')
        #    
        #    if session.get('subscription'):
        #        stripe_sub_id = session['subscription']
        #        
        #        # usersコレクションの更新
        #        user_doc_ref = db.collection('users').document(user_sub)
        #        user_doc_ref.update({
        #            "stripe_subscription_id": stripe_sub_id,
        #            "stripe_subscription_status": "active",
        #            "is_premium": True,
        #            "updated_at": datetime.now(timezone.utc)
        #        })

        #        # サブスクリプション有効化のログ（必要であれば）
        #        print(f"✅ Subscription activated for user: {user_sub}, Stripe ID: {stripe_sub_id}")

        #return {"status": "success"}
                
