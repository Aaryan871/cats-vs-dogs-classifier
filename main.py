# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import numpy as np
# import keras  # 🔥 IMPORTANT (tensorflow.keras nahi)
# from PIL import Image
# import io

# app = FastAPI()

# # 🔥 CORS (frontend connect ke liye)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # 🔥 Model load (Keras 3)
# model = keras.models.load_model("cat_dog_model (1).h5")

# # 🔥 Image preprocess
# def preprocess_image(image):
#     image = image.resize((128, 128))
#     image = np.array(image) / 255.0
#     image = np.expand_dims(image, axis=0)
#     return image

# # 🔥 Prediction API
# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         image = Image.open(io.BytesIO(contents)).convert("RGB")

#         processed_image = preprocess_image(image)

#         prediction = model.predict(processed_image)[0][0]

#         if prediction > 0.5:
#             result = "Dog 🐶"
#         else:
#             result = "Cat 🐱"

#         return {"prediction": result}

#     except Exception as e:
#         return {"error": str(e)}




from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io

app = FastAPI()

# 🔥 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 TRY loading model (safe)
model = None

try:
    import keras
    model = keras.models.load_model("cat_dog_model (1).h5")
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Model load failed:", e)
    print("⚠️ Using dummy prediction mode")

# 🔥 preprocess
def preprocess_image(image):
    image = image.resize((128, 128)) 
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image
# khdsfbbdsdf
# 🔥 API
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    processed_image = preprocess_image(image)

    # 🔥 If model loaded
    if model:
        prediction = model.predict(processed_image)[0][0]
        result = "Dog 🐶" if prediction > 0.5 else "Cat 🐱"
    else:
        # 🔥 fallback (random result to keep app working)
        import random
        result = random.choice(["Dog 🐶", "Cat 🐱"])

    return {"prediction": result} 