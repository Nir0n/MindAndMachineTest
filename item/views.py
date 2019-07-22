from django.views import View
from item.models import Item,User
from django.http import HttpResponse

class SumByIdsView(View):
    def get(self,request, *args, **kwargs):
        data=request.GET.copy()["ids"]
        sum=0
        number_of_items=0
        for id in data:
            user=User.objects.get(pk=id)
            number_of_items+=user.bought_items.count()
            for item in user.bought_items.values():
                sum+=item["price"]
        params=["overall sum: ", sum, " number of items: ", number_of_items]
        return HttpResponse(params,status=200)



class FilterView(View):
    def get(self, request, *args, **kwargs):
        items = Item.objects.none()
        sex=None
        if "sex" in request.GET:
            sex=request.GET.copy()["sex"]
            users=User.objects.filter(sex=sex)
            for user in users:
                items = items|user.bought_items.all()

        if "price_low" and "price_high" in request.GET:
            price_low=request.GET.copy()["price_low"]
            price_high = request.GET.copy()["price_high"]
            items_corr_price = Item.objects.filter(price__range=[price_low, price_high])

            if items:
                items=items & items_corr_price
            else:
                items=items_corr_price
        filter=dict()
        if sex:
            filter.update({"sex":sex})
            params=buy_counter(items,filter)
        else:
            params=buy_counter(items,filter)

        return HttpResponse(params,status=200)

def buy_counter(items,filter):
    params = list(items.values())
    i = 0
    for item in items:
        filter.update({"bought_items":item,"date_joined__range":["2000-11-11", "2019-05-01"]})
        buy_amount = User.objects.filter(**filter).count()
        params[i]["buy_amount"] = buy_amount
        i += 1
    return params