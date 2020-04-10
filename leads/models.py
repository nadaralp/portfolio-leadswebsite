from django.db import models
from background_task import background

class LeadModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    referrer = models.CharField(max_length=40)
    isAnswered = models.BooleanField()
    isTestLead = models.BooleanField(default=False) # Thread runs and deletes every 20minutes

    def __str__(self):
        return self.email
    

    class Meta:
        verbose_name = ("Lead")
        verbose_name_plural = ("Leads")


# Thread
# import threading

# def remove_testleads():
#     try:
#         threading.Timer(60.0, remove_testleads).start() # called every x time
#         print('Test leads deleted')
#         LeadModel.objects.filter(isTestLead=True).delete()
#     except:
#         pass


# remove_testleads()