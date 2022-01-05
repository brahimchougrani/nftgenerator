from operator import truediv
from django.db import models
# Create your models here.
from django.db.models import F
from django.db.models.aggregates import Max
from django_validated_jsonfield import ValidatedJSONField as JSONField
from django.conf import settings
from django.urls import reverse

class NftTemplate(models.Model):
    title = models.CharField(max_length=225,blank=True, null=True)
    file = models.ImageField(blank=True, null=True,max_length=500)
    variants = models.IntegerField(blank=True, null=True)
    variants_used = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("collectibles:collectables_detail", kwargs={"pk": self.pk})
    def get_nft_generate(self):
        return Arrpart.objects.filter(nft_template__id=self.id).count()

class Arrpart(models.Model):
    nft_template = models.ForeignKey(NftTemplate, on_delete=models.CASCADE)
    arr = models.CharField(max_length=50000,unique=True)

class Sections(models.Model):
    nft_template = models.ForeignKey(NftTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    position_x = models.FloatField()
    position_y = models.FloatField()
    sort_order = models.IntegerField(default=0,)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('sort_order',)

    def get_absolute_url(self):
        return reverse("collectibles:collectables_detail", kwargs={"pk": self.nft_template.pk})
    

class Images(models.Model):
    image = models.ImageField()
    section = models.ForeignKey("Sections", on_delete=models.CASCADE)
    position_x = models.FloatField(null=True,blank=True)
    position_y = models.FloatField(null=True,blank=True)
    raretiy = models.IntegerField(default=0)
    width= models.FloatField(blank=True,null=True)
    height = models.FloatField(blank=True,null=True)
    sort_order = models.IntegerField(default=0,null=True,blank=True)
    exclude = models.ManyToManyField(
        "self", related_name="children"
    )    
    def __str__(self):
        return self.image.name
    
    class Meta:
        ordering = ('sort_order',)

class GeneratedArray(models.Model):
    _data_schema = {
        "type": "object",
        "properties": {
            "rarity": {
                "description": "generated set array",
                "type": "array",
                "items": {
                    "type": "string"
                },
            },
            "generatedSetArray": {
                "description": "generated set array",
                "type": "array",
                "items": {
                    "type": "string"
                },
            }
        },
        "default": {},  # note the top level default
        "additionalProperties": False,
    }
    data = JSONField(schema=_data_schema, editable=True)
