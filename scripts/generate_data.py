import pandas as pd
import random
from faker import Faker

fake = Faker()

users = []

channels = ["Instagram", "Google", "TikTok", "Organic", "YouTube"]
countries = ["USA", "Canada", "UK", "Germany", "India"]

for user_id in range(1, 10001):
    users.append({
        "user_id": user_id,
        "signup_date": fake.date_between(start_date='-1y', end_date='today'),
        "country": random.choice(countries),
        "acquisition_channel": random.choice(channels)
    })

users_df = pd.DataFrame(users)

users_df.to_csv("../data/users.csv", index=False)

print("Generated users.csv")

sessions = []

session_id = 1

for user_id in range(1, 10001):

    num_sessions = random.randint(1, 25)

    for _ in range(num_sessions):

        sessions.append({
            "session_id": session_id,
            "user_id": user_id,
            "session_date": fake.date_between(start_date='-1y', end_date='today'),
            "duration_minutes": random.randint(1, 120)
        })

        session_id += 1

sessions_df = pd.DataFrame(sessions)

sessions_df.to_csv("../data/sessions.csv", index=False)

print("Generated sessions.csv")

purchases = []

purchase_id = 1

for user_id in range(1, 10001):

    # Only some users make purchases
    if random.random() < 0.35:

        num_purchases = random.randint(1, 5)

        for _ in range(num_purchases):

            purchases.append({
                "purchase_id": purchase_id,
                "user_id": user_id,
                "amount": round(random.uniform(4.99, 99.99), 2),
                "purchase_date": fake.date_between(start_date='-1y', end_date='today')
            })

            purchase_id += 1

purchases_df = pd.DataFrame(purchases)

purchases_df.to_csv("../data/purchases.csv", index=False)

print("Generated purchases.csv")

subscriptions = []

sub_id = 1

plans = ["Basic", "Premium", "Pro"]

for user_id in range(1, 10001):

    # Only some users subscribe
    if random.random() < 0.20:

        start_date = fake.date_between(start_date='-1y', end_date='today')

        canceled = random.random() < 0.30

        canceled_date = (
            fake.date_between(start_date=start_date, end_date='today')
            if canceled else None
        )

        subscriptions.append({
            "sub_id": sub_id,
            "user_id": user_id,
            "plan_type": random.choice(plans),
            "start_date": start_date,
            "canceled_date": canceled_date
        })

        sub_id += 1

subscriptions_df = pd.DataFrame(subscriptions)

subscriptions_df.to_csv("../data/subscriptions.csv", index=False)

print("Generated subscriptions.csv")