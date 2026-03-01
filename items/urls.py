from django.urls import path
from .views import item_history_api,item_chart_page

urlpatterns = [
    path("api/items/<int:item_id>/history/", item_history_api, name="item_history_api"),
 path("items/<int:item_id>/chart/", item_chart_page, name="item_chart_page"),

]