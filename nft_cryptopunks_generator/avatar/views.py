import re
from django.contrib import messages
from django.db.models import fields
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.aggregates import ArrayAgg
import operator
from django.db.models import Q
from functools import reduce
import base64
from django.core.files.base import ContentFile

# Create your views here.
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, CreateView,UpdateView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import NftTemplate, Sections, Images, Arrpart
from . import forms
from django.urls import reverse
from rest_framework import serializers
from . import models
from django.core import serializers as myser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ("exclude","image","sort_order","position_x","position_y")


class TemplateList(ListView):
    template_name = "avatar_generator/index.html"
    model = NftTemplate
    paginate_by = 100
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@csrf_exempt
def savearr(request,pk):
    nft_template = get_object_or_404(NftTemplate,pk=pk)
    post_data =  request.POST
    print(post_data.get("data"))
    print("######################")
    if post_data:
        Arrpart.objects.create(arr=post_data.get("data"), nft_template=nft_template)
    return JsonResponse({"data": "uploaded"},status=200)

class Generatelist(ListView):
    model = Arrpart
    template_name = "avatar_generator/get.html"
    paginate_by = 1

    def get_queryset(self):
        print(self.kwargs.get("kwargs",None))
        qs = super().get_queryset()
        return qs

def generate_list(request,pk):
    query = request.GET.getlist('query',None)
    print(query)
    if query:
        query2 = reduce(operator.and_, (Q(arr__icontains = item) for item in query))
        user_list = Arrpart.objects.filter(query2,nft_template__pk=pk)
    else:
        user_list = Arrpart.objects.filter(nft_template__pk=pk)
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 50)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    uscount = user_list.count()
    return render(request,"avatar_generator/get.html", { 'object_list': users,"count":uscount })

class collectableCreateView(CreateView):
    model = NftTemplate
    template_name = "avatar_generator/form.html"
    form_class = forms.NftTemplateFrom
    
def createNft(request):
    if request.method == "POST":
        form = forms.NftTemplateFrom(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"data":obj.id},status=200)
        else:
            print(form.errors)
            return JsonResponse({"data":str(form.errors)},status=200)
    else:
        return render(request, "avatar_generator/form.html", {"form":forms.NftTemplateFrom})
    
class collectableDetail(CreateView):
    model = Sections
    template_name = "avatar_generator/upload_sections.html"
    form_class = forms.SectionsFrom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        context["object"] = NftTemplate.objects.get(id=pk)
        context["object_list"] = Sections.objects.filter(nft_template__id=pk)
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        pk = self.kwargs.get("pk")
        obj.nft_template =  NftTemplate.objects.get(id=pk)
        obj.save()
        return super().form_valid(form)


def update_settings(request,pk):
    obj = get_object_or_404(NftTemplate, pk=pk)
    form = forms.NftTemplateFrom(
        request.POST or None, request.FILES or None, instance=obj
    )
    if request.method == "POST":
        if form.is_valid():
            obj = form.save()
            msg = pgettext_lazy("Dashboard message", "Settings has been update  %s") % (
                obj.title,
            )
            messages.success(request, msg)
            return redirect( reverse("collectibles:collectables_detail", kwargs={"pk": pk}))
        else:
            msg = pgettext_lazy("Dashboard message", " %s") % (
                form.errors,
            )
            messages.success(request, msg)
            return redirect( reverse("collectibles:collectables_detail", kwargs={"pk":pk}))
    ctx = {"form": form, "form_url": reverse("collectibles:update_settings", kwargs={"pk":pk})}
    return TemplateResponse(request, "avatar_generator/form_modal.html", ctx)

def delete_section(request,pk):
    obj = get_object_or_404(Sections, pk=pk)
    nft_pk = obj.nft_template.pk
    if request.method == "POST":
        obj.delete()
        return redirect( reverse("collectibles:collectables_detail", kwargs={"pk":nft_pk}))
    ctx = {"form_url": reverse("collectibles:delete_section", kwargs={"pk":pk}), "object":obj}
    return TemplateResponse(request, "avatar_generator/delete_section.html", ctx)

def upload_image(request,pk):
    section = get_object_or_404(Sections, pk=pk)
    form = forms.ImageFrom(
        request.POST or None, request.FILES or None
    )
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.section = section
            obj.position_x = section.position_x
            obj.position_y = section.position_y
            obj.sort_order = section.sort_order
            obj.save()
            msg = pgettext_lazy("Dashboard message", "Image Has Benn Uploaded ")
            messages.success(request, msg)
            return JsonResponse({"data":reverse("collectibles:collectables_detail", kwargs={"pk":section.nft_template.pk})},status=200)
        else:
            msg = pgettext_lazy("Dashboard message", " %s") % (
                form.errors,
            )
            messages.success(request, msg)
            return redirect( reverse("collectibles:collectables_detail", kwargs={"pk":pk}))
    ctx = {"form": form, "form_url": reverse("collectibles:upload_image", kwargs={"pk":pk}), "object":section}
    return TemplateResponse(request, "avatar_generator/images/detail_list.html", ctx)

def generate_nft(request, pk):
    nft = get_object_or_404(NftTemplate, pk=pk)
    sections = Sections.objects.filter(nft_template_id=pk)
    arr = []
    for section in sections:
        image_list = list(section.images_set.all().annotate(exluded=ArrayAgg('exclude')).values("id","image","position_x","position_y","exluded").distinct())
        serialized_q = json.dumps(list(image_list), cls=DjangoJSONEncoder)
        arr.append(serialized_q)
    return TemplateResponse(request, "avatar_generator/generate.html", {"sections":arr,"pk":pk,})

def delete_image(request,pk):
    image = get_object_or_404(Images,pk=pk)
    section = image.section.id
    if request.method == "POST":
        image.delete()
        msg = pgettext_lazy("Dashboard message", "Image Has Benn Deleted ")
        messages.success(request, msg)
        return redirect( reverse("collectibles:upload_image", kwargs={"pk":section}))
    ctx = { "form_url": reverse("collectibles:delete_image", kwargs={"pk":pk}), "object":image}
    return TemplateResponse(request, "avatar_generator/images/delete_image.html", ctx)


def update_image(request,pk):
    image = get_object_or_404(Images,pk=pk)
    section = image.section
    sections_selected = Sections.objects.filter(nft_template=section.nft_template).exclude(id=section.id).values_list("id", flat=True)
    images = Images.objects.filter(section_id__in=list(sections_selected))
    form = forms.ImageFromUpdate(data=request.POST or None,files=request.FILES or None,images_qs=images, instance=image)
    print(form.errors)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            msg = pgettext_lazy("Dashboard message", "Image Has Benn updated ")
            messages.success(request, msg)
        else:
            msg = pgettext_lazy("Dashboard message", str(form.errors))
            messages.success(request, msg)
        return redirect( reverse("collectibles:upload_image", kwargs={"pk":image.section.id}))
    ctx = { "form_url": reverse("collectibles:update_image", kwargs={"pk":pk}), "form": form,"object":image}
    return TemplateResponse(request, "avatar_generator/images/update_images.html", ctx)

def reset_image(request,pk):
    section = get_object_or_404(Sections, pk=pk)
    imgs = Images.objects.filter(section_id=pk)
    print(imgs)
    for img in imgs:
        img.exclude.clear()
        img.save()
    return redirect( reverse("collectibles:upload_image", kwargs={"pk":pk}))

@require_POST
def ajax_upload_image(request, obj_pk):
    section = get_object_or_404(Sections, pk=obj_pk)
    form = forms.ImageFrom(
        request.POST or None, request.FILES or None, section=section
    )
    ctx = {}
    status = 200
    if form.is_valid():
        image = form.save()
        ctx = {"id": image.pk, "image": None, "order": image.sort_order}
    elif form.errors:
        status = 400
        ctx = {"error": form.errors}
    return JsonResponse(ctx, status=status)


def product_image_delete(request, obj_pk, img_pk):
    section = get_object_or_404(Sections, pk=obj_pk)
    image = get_object_or_404(Images, pk=img_pk)
    if request.method == "POST":
        image.delete()
        msg = pgettext_lazy("Dashboard message", "Removed image %s") % (
            image.image.name,
        )
        messages.success(request, msg)
        return redirect("dashboard:product-image-list", product_pk=section.pk)
    return TemplateResponse(
        request,
        "dashboard/product/product_image/modal/confirm_delete.html",
        {"product": section, "image": image},
    )


@require_POST
def ajax_reorder_product_images(request, obj_pk):
    images = get_object_or_404(Images, pk=obj_pk)
    form = forms.ReorderProductImagesForm(request.POST, instance=images)
    status = 200
    ctx = {}
    if form.is_valid():
        form.save()
    elif form.errors:
        status = 400
        ctx = {"error": form.errors}
    return JsonResponse(ctx, status=status)




def save_image_blob(request):
    if request.method == "POST":
        image_b64 = request.POST.get('image') # This is your base64 string image
        format, imgstr = image_b64.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        print(data)
    pass

def delete_partarr(request,pk):
    Arrpart.objects.filter(nft_template__pk=pk).delete()
    return redirect( reverse("collectibles:collectables_detail", kwargs={"pk": pk}))
