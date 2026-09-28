import requests

response = requests.post(
    "http://127.0.0.1:5000/analyze/single",
    json={"text": "हा product मला खूप आवडला, quality आणि design दोन्ही उत्तम आहेत!"}
)
print(response.json())