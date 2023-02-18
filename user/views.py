from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.models import User, AppUsage, Transactions
from django.db.models import Q
from django.shortcuts import get_object_or_404


class Home(APIView):
    # adding rest framework authentication permission
    permission_classes = (IsAuthenticated,)

    def get(self, request): 
        user = get_object_or_404(User, pk=request.user.id)
        transactions = Transactions.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).values('timestamp', 'transaction_type', 'amount', 'status')
        app_usage = AppUsage.objects.filter(
            user=user
        )

        session_hours = sum([
            (i.session_end - i.session_start).total_seconds() / 60.0 / 60.0
            for i in app_usage
        ])

        response = {
            "transactions": transactions,
            "mobile_usage": f"{session_hours:.0f}",
            "first_name": user.first_name
        }
    
        return Response(response)
