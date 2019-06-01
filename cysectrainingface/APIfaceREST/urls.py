from django.conf.urls import url
from APIfaceREST import views
urlpatterns = [
    url(r'^trainings/$', views.traininglist),
    #url(r'^test/$', views.test),
    #url(r'^series/(?P<pk>[0-9]+)/$', views.serie_detail),
]


# curl -k -X POST https://localhost:8000/api/token/ -d username=admin -d password=pass
# curl -k -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTU5MjU0MDI3LCJqdGkiOiJmMzJiMDdkMzAzODM0Zjg3YjhmOWNmMDZkMjQ0OTdmZSIsInVzZXJfaWQiOjh9.DbAVCQsmCnvzSsaIv29dDlp7mWN4XlZ4j8druljKgSc" -X POST https://localhost:8000/trainings/ -d title="Advanced"