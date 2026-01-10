import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import os

# ---------------- CONFIG ----------------
DATASET_PATH = "dataset/asl_alphabet"
MODEL_PATH = "models/asl_cnn_model.h5"
LABEL_PATH = "models/labels.json"
IMG_SIZE = 64
BATCH_SIZE = 32
EPOCHS = 10
# ---------------------------------------

os.makedirs("models", exist_ok=True)

datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

# ✅ Save label → index mapping
with open(LABEL_PATH, "w") as f:
    json.dump(train_data.class_indices, f, indent=4)

# ---------------- CNN MODEL ----------------
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation="relu",
                           input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(64, (3,3), activation="relu"),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(128, (3,3), activation="relu"),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation="relu"),
    tf.keras.layers.Dense(train_data.num_classes, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

model.save(MODEL_PATH)
print("✅ Model and labels saved successfully")
