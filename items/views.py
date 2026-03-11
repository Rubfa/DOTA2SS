from datetime import date, timedelta
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Item, PriceRecord, Hero, Cosmetic


# 首页（显示英雄列表）
def index(request):
    heroes = Hero.objects.all()
    return render(request, "index.html", {"heroes": heroes})


# 获取某个英雄的饰品
def get_cosmetics(request, hero_id):

    cosmetics = Cosmetic.objects.filter(hero_id=hero_id)

    data = []

    for c in cosmetics:
        data.append({
            "id": c.id,
            "name": c.name
        })

    return JsonResponse(data, safe=False)


# 线性回归趋势计算
def linear_trend(values):

    n = len(values)

    if n < 2:
        return values[:]

    xs = list(range(n))

    sum_x = sum(xs)
    sum_y = sum(values)
    sum_x2 = sum(x * x for x in xs)
    sum_xy = sum(x * y for x, y in zip(xs, values))

    denom = n * sum_x2 - sum_x * sum_x

    if denom == 0:
        return values[:]

    a = (n * sum_xy - sum_x * sum_y) / denom
    b = (sum_y - a * sum_x) / n

    return [a * x + b for x in xs]


# API：返回某个 cosmetic/item 的历史数据
def item_history_api(request, item_id):

    # 尝试从Cosmetic获取关联的Item
    try:
        cosmetic = Cosmetic.objects.get(id=item_id)
        if cosmetic.item:
            item = cosmetic.item
        else:
            item = get_object_or_404(Item, id=item_id)
    except Cosmetic.DoesNotExist:
        item = get_object_or_404(Item, id=item_id)

    qs = PriceRecord.objects.filter(item=item)

    # 时间范围
    r = request.GET.get("range", "30d")

    if r == "7d":
        qs = qs.filter(date__gte=date.today() - timedelta(days=7))
    elif r == "30d":
        qs = qs.filter(date__gte=date.today() - timedelta(days=30))
    elif r == "365d":
        qs = qs.filter(date__gte=date.today() - timedelta(days=365))

    # all 不筛选

    records = qs.order_by("date")

    labels = [x.date.isoformat() for x in records]
    prices = [float(x.price) for x in records]
    quantities = [x.quantity for x in records]

    trend_price = linear_trend(prices)
    trend_qty = linear_trend(quantities)

    return JsonResponse({
        "labels": labels,
        "prices": prices,
        "quantities": quantities,
        "trend_price": trend_price,
        "trend_qty": trend_qty,
    })


# 图表页面
def item_chart_page(request, item_id):
    return render(request, "items/item_chart.html", {
        "item_id": item_id
    })