import firebase_admin
from firebase_admin import ml
from firebase_admin import credentials

cred = credentials.Certificate("realtime-discord-analysis-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)



model = ml.get_model("20020422")

# model.predict("hi")

print(model.as_dict())