# Learning Path 05 – Model Optimisation

_Last Updated: November 30, 2025_

**Difficulty:** Advanced  
**Estimated time:** 8–12 hours

Model optimisation is about improving performance (accuracy, speed, size) without sacrificing quality. This path covers techniques for production models.

## Hyperparameter Tuning

### What Are Hyperparameters?

Parameters set **before** training that control how the model learns:
- Learning rate: how big each gradient step is (0.001, 0.01, 0.1)
- Batch size: how many samples per gradient update
- Number of layers: architecture choice
- Regularisation strength: dropout rate, L2 penalty

**Problem:** Choosing optimal hyperparameters manually is tedious and suboptimal.

### Grid Search

Try all combinations in a defined grid.

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    n_jobs=-1  # Use all CPU cores
)
grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
```

**Pros:** Simple, guarantees finding the best in the grid  
**Cons:** Exponential growth (3 × 3 × 3 = 27 combinations; add another dimension → 81)

### Random Search

Randomly sample hyperparameters.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

param_dist = {
    'n_estimators': randint(50, 500),
    'max_depth': randint(5, 30),
    'min_samples_split': randint(2, 20)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(),
    param_dist,
    n_iter=50,  # Try 50 random combinations
    cv=5,
    n_jobs=-1
)
random_search.fit(X_train, y_train)
```

**Pros:** Scales better than grid search; often finds good solutions faster  
**Cons:** May miss optimal combination

### Bayesian Optimisation (Vertex AI Vizier)

**Smart search:** Use machine learning to predict which hyperparameters will work best, then focus search there.

```bash
gcloud ai hp-tuning-jobs create \
  --display-name="churn-tuning" \
  --config=hparams.yaml \
  --region=us-central1
```

**Config (hparams.yaml):**

```yaml
displayDisplayName: "Churn Model Hyperparameter Tuning"
studySpec:
  metrics:
    - id: "accuracy"
      goal: MAXIMIZE
  parameters:
    - id: "learning_rate"
      doubleValueSpec:
        minValue: 0.0001
        maxValue: 0.1
    - id: "batch_size"
      integerValueSpec:
        minValue: 16
        maxValue: 512
trialCount: 50
```

**Result:** After 50 trials, Bayesian optimisation recommends best hyperparameters (often better than random or grid).

**Cost:** ~£100–300 depending on trials and compute.

## Feature Importance and Selection

### Why It Matters

- Fewer features → faster model, easier interpretation
- Irrelevant features add noise → lower accuracy
- Removing features can improve generalisation

### Permutation Importance

Measure accuracy drop when you shuffle a feature.

```python
from sklearn.inspection import permutation_importance

importances = permutation_importance(
    model, X_test, y_test, n_repeats=10
)

for feature, importance in sorted(zip(X_test.columns, importances.importances_mean),
                                   key=lambda x: x[1], reverse=True):
    print(f"{feature}: {importance:.4f}")
```

**Output:**
```
customer_lifetime_value: 0.0450
account_age_months: 0.0320
monthly_spend: 0.0180
region: 0.0020  # Low importance; consider removing
```

### Tree-Based Feature Importance

Random Forests compute importance during training.

```python
model = RandomForestClassifier()
model.fit(X_train, y_train)

importances = model.feature_importances_
for feature, importance in sorted(zip(X_train.columns, importances), 
                                   key=lambda x: x[1], reverse=True):
    print(f"{feature}: {importance:.4f}")
```

### Recursive Feature Elimination

Iteratively remove least important features.

```python
from sklearn.feature_selection import RFE

selector = RFE(estimator=RandomForestClassifier(), n_features_to_select=5)
X_selected = selector.fit_transform(X_train, y_train)
print(f"Selected features: {X_train.columns[selector.support_]}")
```

## Quantisation

**Goal:** Reduce model size and inference latency by using lower precision.

### INT8 Quantisation

Replace float32 with int8 (8-bit integers).

**Trade-off:**
- **Pros:** Model 4× smaller, 2–4× faster inference
- **Cons:** Slight accuracy loss (usually <1%)

### TensorFlow Quantisation

```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
quantized_model = converter.convert()

# Save quantized model
with open('model.tflite', 'wb') as f:
    f.write(quantized_model)

# Size comparison
print(f"Original: {os.path.getsize('model.h5') / 1024 / 1024:.1f} MB")
print(f"Quantized: {os.path.getsize('model.tflite') / 1024 / 1024:.1f} MB")
```

**Result:**
- Original: 150 MB
- Quantized: 40 MB (73% reduction)

## Pruning

Remove redundant neurons/connections to reduce model size.

```python
import tensorflow_model_optimization as tfmot

pruning_params = {
    'pruning_schedule': tfmot.sparsity.keras.PolynomialDecay(
        initial_sparsity=0.36,
        final_sparsity=0.80,
        begin_step=0,
        end_step=end_step
    )
}

pruned_model = tfmot.sparsity.keras.prune_low_magnitude(
    model,
    **pruning_params
)

pruned_model.compile(optimizer='adam', loss='categorical_crossentropy')
pruned_model.fit(X_train, y_train, epochs=12)

# Export for deployment
final_model = tfmot.sparsity.keras.strip_pruning(pruned_model)
final_model.save('pruned_model')
```

**Result:** Model 30–40% smaller with minimal accuracy loss.

## Distributed Training Optimisation

### Gradient Accumulation

Simulate larger batch sizes on smaller GPUs by accumulating gradients.

```python
accumulation_steps = 4
batch_size = 32  # Effective batch size = 32 × 4 = 128

optimizer = tf.keras.optimizers.Adam()
accumulated_grads = [tf.Variable(tf.zeros_like(w), trainable=False) 
                     for w in model.trainable_weights]

@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        logits = model(x, training=True)
        loss = loss_fn(y, logits)
    grads = tape.gradient(loss, model.trainable_weights)
    return grads

for step, (x_batch, y_batch) in enumerate(train_dataset):
    grads = train_step(x_batch, y_batch)
    
    # Accumulate
    for acc_grad, grad in zip(accumulated_grads, grads):
        acc_grad.assign_add(grad)
    
    # Apply after accumulation_steps
    if (step + 1) % accumulation_steps == 0:
        optimizer.apply_gradients(zip(accumulated_grads, model.trainable_weights))
        for acc_grad in accumulated_grads:
            acc_grad.assign(tf.zeros_like(acc_grad))
```

### Mixed Precision

Use lower precision (float16) for forward pass; higher precision (float32) for backward pass.

```python
policy = tf.keras.mixed_precision.Policy('mixed_float16')
tf.keras.mixed_precision.set_global_policy(policy)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax',
                         dtype='float32')  # Last layer stays float32
])

model.fit(X_train, y_train)
```

**Result:** ~2× faster training on modern GPUs; minimal accuracy loss.

## Latency Optimisation

### Batch Prediction vs Online

- **Batch prediction:** Process many samples together (higher throughput, higher latency) → background jobs
- **Online prediction:** Process individual requests (lower latency, lower throughput) → API endpoints

**Example trade-offs:**
- Batch: 1M predictions in 1 hour (avg latency: 3.6ms per prediction)
- Online: 100 predictions/second (avg latency: 50ms per prediction)

### Caching

Cache predictions for frequent queries.

```python
import redis

def get_prediction_with_cache(user_id, features):
    cache_key = f"prediction:{user_id}"
    
    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Compute prediction
    prediction = model.predict(features)
    
    # Store in cache (expire after 1 hour)
    redis_client.setex(cache_key, 3600, json.dumps(prediction))
    
    return prediction
```

## Cost Optimisation

### Compute Instance Sizing

Choose instance based on model size and traffic:

| Instance Type | Cost/Hour (GBP) | Throughput | Best For |
|---------------|-----------------|-----------|----------|
| n1-standard-1 (0.5 CPU) | £0.05 | 10 req/s | Low-traffic APIs |
| n1-standard-4 (4 CPU, GPU) | £0.25 | 100 req/s | Production APIs |
| TPU v3 | £0.35 | 1000 req/s | High-volume batch |

### Experiment Cost Tracking

Track total cost of hyperparameter tuning:

```python
cost_per_trial_hour = 0.35  # GPU instance
total_trials = 50
hours_per_trial = 2
total_cost_gbp = cost_per_trial_hour * total_trials * hours_per_trial

print(f"Hyperparameter tuning cost: £{total_cost_gbp:.2f}")
```

## Exam Focus

**PMLE will test:**
- [ ] Hyperparameter tuning strategies (grid, random, Bayesian)
- [ ] Feature selection and importance
- [ ] Quantisation and pruning trade-offs
- [ ] Distributed training optimisation
- [ ] Latency vs throughput trade-offs
- [ ] Cost estimation for optimisation workflows

## Cross-References

- See `02-vertex-ai.md` for Vizier hyperparameter tuning
- See `03-tensorflow-keras.md` for model architecture choices
