from config.celery_app import app
from .models import Images
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
import logging
logger = logging.getLogger(__name__)


def create_thumbnails(pk, model, size_set, image_attr=None):
    instance = model.objects.get(pk=pk)
    if not image_attr:
        image_attr = "image"
    image_instance = getattr(instance, image_attr)
    if image_instance.name == "":
        # There is no file, skip processing
        return
    warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance, rendition_key_set=size_set, image_attr=image_attr
    )
    logger.info("Creating thumbnails for  %s", pk)
    num_created, failed_to_create = warmer.warm()
    if num_created:
        logger.info("Created %d thumbnails", num_created)
    if failed_to_create:
        logger.error("Failed to generate thumbnails", extra={"paths": failed_to_create})



@app.task
def create_product_thumbnails(image_id):
    """Take a ProductImage model and create thumbnails for it."""
    create_thumbnails(pk=image_id, model=Images, size_set="images")
