from store.models import CartItem
from django.db.models import Sum

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).aggregate(total=Sum('quantity'))['total'] or 0
    else:
        session_key = request.session.session_key
        if session_key:
            count = CartItem.objects.filter(session_key=session_key).aggregate(total=Sum('quantity'))['total'] or 0
    return {'cart_count': count}
