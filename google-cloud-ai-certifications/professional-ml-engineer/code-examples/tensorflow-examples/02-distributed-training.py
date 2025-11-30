"""Skeleton example: Distributed training with MirroredStrategy."""

import tensorflow as tf


def create_strategy_model() -> tf.keras.Model:
    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Dense(64, activation="relu", input_shape=(32,)),
                tf.keras.layers.Dense(1),
            ]
        )
        model.compile(optimizer="adam", loss="mse")
    return model


if __name__ == "__main__":
    model = create_strategy_model()
    print(model.summary())
