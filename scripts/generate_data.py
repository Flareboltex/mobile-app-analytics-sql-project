import pandas as pd
import random
from faker import Faker

fake = Faker()

channels = ["Instagram", "Google", "TikTok", "Organic", "YouTube"]
countries = ["USA", "Canada", "UK", "Germany", "India"]

#(DAY 9: ADDED USER BEHAVIOR PROFILES)
channel_purchase_multiplier = {
    "Organic": 0.55,
    "Google": 0.40,
    "Instagram": 0.30,
    "YouTube": 0.25,
    "TikTok": 0.15
}

country_spend_multiplier = {
    "USA": 1.6,
    "Canada": 1.3,
    "UK": 1.2,
    "Germany": 1.1,
    "India": 0.6
}

country_session_multiplier = {
    "USA": 1.0,
    "Canada": 1.0,
    "UK": 1.1,
    "Germany": 1.1,
    "India": 1.5
}

users = []

for user_id in range(1, 10001):

    country = random.choice(countries)
    channel = random.choice(channels)

    users.append({
        "user_id": user_id,
        "signup_date": fake.date_between(start_date='-1y', end_date='today'),
        "country": country,
        "acquisition_channel": channel
    })
    
users_df = pd.DataFrame(users)

users_df.to_csv("../data/users.csv", index=False)

print("Generated users.csv")

sessions = []

session_id = 1

for user_id in range(1, 10001):

    user_country = users[user_id - 1]["country"]

    base_sessions = random.randint(1, 25)

    num_sessions = int(
        base_sessions *
        country_session_multiplier[user_country]
    )

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

    user_channel = users[user_id - 1]["acquisition_channel"]

    purchase_probability = channel_purchase_multiplier[user_channel]

    if random.random() < purchase_probability:

        num_purchases = random.randint(1, 5)

        for _ in range(num_purchases):

            user_country = users[user_id - 1]["country"]

            base_amount = random.uniform(4.99, 99.99)

            adjusted_amount = (
                base_amount *
                country_spend_multiplier[user_country]
            )

            purchases.append({
                "purchase_id": purchase_id,
                "user_id": user_id,
                "amount": round(adjusted_amount, 2),
                "purchase_date": fake.date_between(
                    start_date='-1y',
                    end_date='today'
                )
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