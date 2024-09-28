import os
import time

from celery import shared_task
from app.config import Config
from app.services.user_interaction_model import train_model as category_model_train
from app.services.plain_cat_model import train_model as interaction_model_train

@shared_task(name="train_category_model_task")
def train_category_model_task():
    return category_model_train()


@shared_task(name="train_interaction_model_task")
def train_interaction_model_task():
    return interaction_model_train()
