from django.urls import path
from .views import LeadsListView, LeadAPI, delete_testleads, lead_test_endpoint

app_name = "leads"
urlpatterns = [
    path('', LeadsListView.as_view(), name="leads_list"),
    path('api/leads', LeadAPI.as_view(), name="leads_api"),
    path('api/leads/<int:pk>', LeadAPI.as_view(), name="lead_api_update"),
    path('deleteleads/', delete_testleads, name="deleteleads"),
    path('testlead/', lead_test_endpoint, name="testlead"),
]
