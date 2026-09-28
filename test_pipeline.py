print("Step 1: importing...")
from src.predict_sentiment import predict_sentiment
from src.predict_aspect import predict_aspect
print("Step 2: imports successful")

text = "Ye phone khupach chan aahe, performance is really amazing."

print("Step 3: running sentiment...")
s = predict_sentiment(text)
print("Step 4: sentiment result:", s)

print("Step 5: running aspect...")
a = predict_aspect(text)
print("Step 6: aspect result:", a)

print("Step 7: both worked fine")