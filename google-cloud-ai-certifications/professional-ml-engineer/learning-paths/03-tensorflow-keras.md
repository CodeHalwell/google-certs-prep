# Learning Path 03 – TensorFlow & Keras

_Last Updated: November 30, 2025_

**Difficulty:** Advanced  
**Estimated time:** 12–16 hours

TensorFlow and Keras are the frameworks you'll use to build and train neural networks on Vertex AI. This path focuses on practical, production-ready patterns.

## Keras Fundamentals

### Sequential Model (Simple)

**What it is:** Simplest way to stack layers in order.

```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

**Use case:** Image classification, sentiment analysis, regression.

**Limitation:** Linear; can't represent branching inputs or multiple outputs.

### Functional API (Flexible)

**What it is:** Define models with branches, merges, and multiple inputs/outputs.

```python
inputs = keras.Input(shape=(784,))
x = keras.layers.Dense(128, activation='relu')(inputs)
x = keras.layers.Dropout(0.2)(x)
outputs = keras.layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs=inputs, outputs=outputs)
```

**Use case:** Multi-input models (e.g., tabular + image), multi-task learning, complex architectures.

### Subclassing API (Full Control)

**What it is:** Define custom layers and models by inheriting from `keras.Model`.

```python
class CustomModel(keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = keras.layers.Dense(128, activation='relu')
        self.dropout = keras.layers.Dropout(0.2)
        self.dense2 = keras.layers.Dense(10, activation='softmax')
    
    def call(self, inputs, training=False):
        x = self.dense1(inputs)
        x = self.dropout(x, training=training)
        return self.dense2(x)

model = CustomModel()
```

**Use case:** Implementing research papers, custom training loops, advanced architectures.

## Common Layers

| Layer | Purpose | Example |
|-------|---------|---------|
| Dense | Fully connected (every input to every output) | `Dense(64, activation='relu')` |
| Conv2D | 2D convolution (detect features in images) | `Conv2D(32, kernel_size=3)` |
| LSTM | Recurrent (process sequences) | `LSTM(64)` |
| Embedding | Convert integers to dense vectors | `Embedding(vocab_size, 128)` |
| Dropout | Randomly zero activations (prevent overfitting) | `Dropout(0.2)` |
| BatchNormalization | Normalize layer inputs (stable training) | `BatchNormalization()` |

## Training a Model

### Basic Training Loop

```python
model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)
```

**Key parameters:**
- `epochs`: Number of passes through the entire dataset
- `batch_size`: Number of samples per gradient update (smaller = more updates, noisier gradients; larger = fewer updates, smoother)
- `validation_split`: Fraction of training data to use for validation (not trained on)

### Custom Training Loop

For production or research:

```python
optimizer = keras.optimizers.Adam(learning_rate=0.001)
loss_fn = keras.losses.SparseCategoricalCrossentropy()

@tf.function  # Compile to graph for speed
def train_step(x, y):
    with tf.GradientTape() as tape:
        logits = model(x, training=True)
        loss_value = loss_fn(y, logits)
    grads = tape.gradient(loss_value, model.trainable_weights)
    optimizer.apply_gradients(zip(grads, model.trainable_weights))
    return loss_value

for epoch in range(10):
    for x_batch, y_batch in train_dataset:
        loss = train_step(x_batch, y_batch)
    print(f"Epoch {epoch}, loss: {loss}")
```

**Why custom loops?**
- Fine-grained control over training
- Custom loss functions or metrics
- Advanced techniques (gradient accumulation, mixed precision)

## Distributed Training

### Data Parallelism (MirroredStrategy)

Run training on multiple GPUs, each processing a different batch, then average gradients.

```python
strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    model = keras.Sequential([...])
    model.compile(...)

model.fit(x_train, y_train, epochs=10)
```

**Result:** ~2–4× speedup on 2–4 GPUs (not perfectly linear due to communication overhead).

**Cost:** Using 2 GPUs costs ~2× more, but training time is ~1.5× faster (not worth it unless you're doing many experiments).

### TPU Strategy

Google Cloud TPUs (tensor processing units) are optimised for matrix multiplication.

```python
strategy = tf.distribute.TPUStrategy()
# Same pattern as MirroredStrategy
```

**Trade-off:** TPUs are cheaper per compute hour than GPUs for large-scale training; good for batch training, not ideal for interactive work.

## Transfer Learning

**Problem:** Training a model from scratch on small datasets is slow and often overfits.

**Solution:** Start with a pre-trained model (e.g., trained on ImageNet), freeze early layers, fine-tune later layers on your data.

```python
base_model = keras.applications.EfficientNetB0(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False  # Freeze early layers

model = keras.Sequential([
    base_model,
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(num_classes, activation='softmax')
])

model.fit(x_train, y_train, epochs=5)
```

**Result:** Often better accuracy with less training data and time.

## Regularisation Techniques

### Dropout

Randomly zero a fraction of activations during training; disabled during inference.

```python
keras.layers.Dropout(0.3)  # Zero 30% of activations
```

**Effect:** Prevents co-adaptation of neurons; improves generalisation.

### L1/L2 Regularisation

Add penalty to loss if weights become large.

```python
keras.layers.Dense(64, kernel_regularizer=keras.regularizers.l2(0.001))
```

**Effect:** Encourages simpler models; reduces overfitting.

### Early Stopping

Stop training if validation loss doesn't improve.

```python
callbacks = [
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,  # Stop if no improvement for 5 epochs
        restore_best_weights=True
    )
]
model.fit(x_train, y_train, validation_split=0.2, callbacks=callbacks)
```

## Saving and Loading Models

### SavedModel Format (Recommended)

```python
model.save('my_model')  # Saves to directory with metadata, weights, assets
loaded_model = keras.models.load_model('my_model')
```

**Why:** Portable across frameworks, includes training and inference signatures.

### Keras Format (Legacy)

```python
model.save('my_model.h5')  # Single file
```

## Production Considerations

### Batch Normalization

If your model uses BatchNormalization, ensure it's switched to inference mode during serving (Keras handles this if you use `model.predict()`).

### Model Size

Large models take longer to serve and consume more memory. Trade-off accuracy vs latency:
- Mobile/edge: SqueezeNet, MobileNet (1–5 MB)
- Server: ResNet, EfficientNet (50–200 MB)
- Research: Large transformers (500 MB–2 GB)

### Quantisation

Reduce model size and latency by using lower precision (e.g., int8 instead of float32).

```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
```

## Exam Focus

**PMLE will test:**
- [ ] When to use Sequential vs Functional vs Subclassing API
- [ ] Custom training loops and loss functions
- [ ] Distributed training strategies (MirroredStrategy, TPU)
- [ ] Transfer learning and pre-trained models
- [ ] Regularisation (dropout, L1/L2, early stopping)
- [ ] Model serialisation and deployment
- [ ] Trade-offs: accuracy vs speed vs model size

## Cross-References

- See `02-vertex-ai.md` for training on Vertex AI
- See `04-mlops-deployment.md` for production pipelines
- See `code-examples/tensorflow-examples/` for working code
