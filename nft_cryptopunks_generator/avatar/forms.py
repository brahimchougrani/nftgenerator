from django import forms
from django.db.models import fields
from .models import Arrpart, NftTemplate, Sections, Images
from .thumbnails import create_product_thumbnails
from django.utils.safestring import mark_safe

class NftTemplateFrom(forms.ModelForm):
    class Meta:
        model = NftTemplate
        fields = ("title", "width","height","file")
    def __init__(self, *args, **kwargs):
        super(NftTemplateFrom, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['width'].required = True
        self.fields['height'].required = True
        self.fields['file'].required = True


class SectionsFrom(forms.ModelForm):
    class Meta:
        model = Sections
        exclude = ("nft_template",)


class ImageFrom(forms.ModelForm):
    class Meta:
        model = Images
        exclude = ("section","raretiy","exclude")

    def save(self, commit=True):
        image = super().save(commit=commit)
        return image

class CustomChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return mark_safe("<img class='w-75' src='{}'/> <span>{}</span>".format(obj.image.url,obj.image.name))
        
class ImageFromUpdate(forms.ModelForm):
    class Meta:
        model = Images
        fields = ("sort_order","width","height","exclude")

    def __init__(self,images_qs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the query here
        print(images_qs)
        self.fields['exclude'] = CustomChoiceField(widget=forms.CheckboxSelectMultiple, queryset=images_qs,required=False,)

class ArrForm(forms.ModelForm):
    class Meta:
        model = Arrpart
        fields = ("arr",)

class OrderedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        qs = super().clean(value)
        keys = list(map(int, value))
        return sorted(qs, key=lambda v: keys.index(v.pk))


class ReorderProductImagesForm(forms.ModelForm):
    ordered_images = OrderedModelMultipleChoiceField(
        queryset=Images.objects.none()
    )

    class Meta:
        model = Sections
        fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["ordered_images"].queryset = self.instance.images.all()

    def save(self):
        for order, image in enumerate(self.cleaned_data["ordered_images"]):
            image.sort_order = order
            image.save()
        return self.instance
