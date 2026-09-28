print("Step 1: importing...")
from src.predict_aspect import predict_aspect
print("Step 2: import successful, running prediction...")

result = predict_aspect("Camera quality bahot kharab hai is phone ki")
print("Step 3: prediction successful:", result)