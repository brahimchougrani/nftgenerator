from django.urls import include, path
from .views import TemplateList, collectableDetail, createNft, delete_image, update_settings, savearr, delete_section, upload_image, Generatelist, generate_list, generate_nft, update_image, reset_image, delete_image, delete_partarr
app_name = "collectibles"
urlpatterns = [
    path("", TemplateList.as_view(), name="home"),
    path("create/", createNft, name="collectables_create"),
    path("<int:pk>/", collectableDetail.as_view(), name="collectables_detail"),
    path("section/<int:pk>/", update_settings, name="update_settings"),
    path("section/delete/<int:pk>/", delete_section, name="delete_section"),
    path("section/image/<int:pk>/", upload_image, name="upload_image"),
    path("generate/<int:pk>/", generate_nft, name="generate_nft"),
    path("delete/imge/<int:pk>/", delete_image, name="delete_image"),
    path("update/imge/<int:pk>/", update_image, name="update_image"),
    path("reset/imge/<int:pk>/", reset_image, name="reset_image"),
    path("<int:id>/section/", TemplateList.as_view(), name="template_list"),
    path("<int:pk>/save_arr/", savearr, name="save_arr"),
    path("<int:pk>/generate_part/", generate_list, name="generate_part"),
    path("delete/<int:pk>/", delete_partarr, name="delete_partarr"),
]
