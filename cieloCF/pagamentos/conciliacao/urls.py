from django.urls import path
from .views import conciliacao_pagamentos

urlpatterns = [
    path('conciliar/', conciliacao_pagamentos)
]