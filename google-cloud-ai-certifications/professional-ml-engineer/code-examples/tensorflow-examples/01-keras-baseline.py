"""Baseline Keras model example for PMLE practice.

Trains a simple dense network on MNIST using TensorFlow Datasets.
"""

import tensorflow as tf
import tensorflow_datasets as tfds


def build_model() -> tf.keras.Model:
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def load_dataset(batch_size: int = 128):
    ds_train, ds_test = tfds.load(
        "mnist",
        split=["train", "test"],
        as_supervised=True,
    )

    def _prep(image, label):
        image = tf.cast(image, tf.float32) / 255.0
        return image, label

    ds_train = ds_train.map(_prep).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    ds_test = ds_test.map(_prep).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return ds_train, ds_test


if __name__ == "__main__":
    train_ds, test_ds = load_dataset()
    model = build_model()
    model.fit(train_ds, epochs=3, validation_data=test_ds)
    test_loss, test_acc = model.evaluate(test_ds)
    print(f"Test accuracy: {test_acc:.3f}")
