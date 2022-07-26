from pathlib import Path
from typing import Tuple
import tensorflow as tf
from functools import partial


def process_path(file_path: str, image_shape: Tuple[int]):
    image = tf.io.read_file(file_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, image_shape)
    image = image / 255.0
    return image, file_path


def get_image_generator(imgs_path: Path, batch_size: int) -> tf.data.Dataset:
    imgs_path = [str(i) for i in imgs_path]
    ds = tf.data.Dataset.list_files(imgs_path, shuffle=False)
    process = partial(process_path, image_shape=(224, 224))
    return ds.map(process).batch(batch_size)
