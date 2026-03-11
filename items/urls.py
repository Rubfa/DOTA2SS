from django.urls import path
from . import views

urlpatterns = [

    # 首页（显示英雄列表）
    path("", views.index, name="index"),

    # 获取某个英雄的饰品
    path("get_cosmetics/<int:hero_id>/", views.get_cosmetics, name="get_cosmetics"),

    # API：返回某个饰品的历史价格数据
    path("api/items/<int:item_id>/history/", views.item_history_api, name="item_history_api"),

    # 图表页面
    path("items/<int:item_id>/chart/", views.item_chart_page, name="item_chart_page"),

]