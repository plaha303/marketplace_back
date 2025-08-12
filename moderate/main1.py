from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
import torch
import numpy as np

# Перевірка доступності GPU
print("GPU доступний:", torch.cuda.is_available())
print("Назва GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")

# Завантаження датасету
dataset = load_dataset('json', data_files={
    'train': 'data1/train.jsonl',
    'validation': 'data1/validation.jsonl',
    'test': 'data1/test.jsonl'
})

# Очищення: видаляємо зразки без 'tags'
def clean_none_tags(example):
    return example['tags'] is not None

dataset = dataset.filter(clean_none_tags)

# Приведення міток до int
def convert_tags(example):
    if example['tags'] is not None:
        return {'tags': int(float(example['tags']))}  # Явне приведення до int через float
    return example

dataset = dataset.map(convert_tags)

# Друк розподілу класів
train_df = pd.DataFrame(dataset['train'])
print("Розподіл класів у train:")
print(train_df['tags'].value_counts())
print("Унікальні значення tags:")
print(train_df['tags'].unique())
print("Тип даних tags:")
print(train_df['tags'].dtype)

# Токенізатор
tokenizer = AutoTokenizer.from_pretrained('bert-base-multilingual-cased')

# Токенізація
def tokenize_function(examples):
    result = tokenizer(examples['text'], padding='max_length', truncation=True, max_length=128)
    if 'tags' in examples:
        result['labels'] = [int(float(tag)) for tag in examples['tags']]  # Перетворюємо мітки в int
    return result

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Видаляємо оригінальний стовпець 'tags', оскільки 'labels' уже створено
tokenized_dataset = tokenized_dataset.remove_columns(['tags'])

# Перетворення міток у torch.long
tokenized_dataset = tokenized_dataset.map(lambda x: {'labels': torch.tensor(x['labels'], dtype=torch.long)})

# Налаштування формату для PyTorch
tokenized_dataset.set_format('torch', columns=['input_ids', 'attention_mask', 'labels'])

# Перевірка типу міток
labels_sample = tokenized_dataset['train']['labels'][0]  # Беремо перший елемент
print("Тип міток у tokenized_dataset['train']:", type(labels_sample))
print("Значення першого мітки:", labels_sample)

# Модель
model = AutoModelForSequenceClassification.from_pretrained(
    'bert-base-multilingual-cased',
    num_labels=2  # класи 0 і 1
)

# Параметри навчання
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    eval_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True,
    metric_for_best_model='f1',
)

# Метрики
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='binary')
    return {'precision': precision, 'recall': recall, 'f1': f1}

# Тренер
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['validation'],
    compute_metrics=compute_metrics
)

# Навчання
trainer.train()

# Збереження моделі
model.save_pretrained('./moderation_model')
tokenizer.save_pretrained('./moderation_model')

# Тестування
results = trainer.evaluate(tokenized_dataset['test'])
print("Результати на тестовому наборі:", results)