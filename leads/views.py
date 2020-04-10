import requests as r
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View, DetailView
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from .models import LeadModel
from .serializers import LeadSerializer
from django.views.generic.edit import FormView
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import LoginForm


TEMPLATE_DIRECTORY = "leads"


class LeadsListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    queryset = LeadModel.objects.order_by('-created_at')
    paginate_by = 5
    model = LeadModel
    template_name = f"{TEMPLATE_DIRECTORY}/index.html"

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = LeadModel.objects.order_by('-created_at')
        if q is not None:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(email__icontains=q) |
                Q(subject__icontains=q) |
                Q(message__icontains=q) |
                Q(referrer__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get("q")
        if q is not None:
            context['input'] = q
        return context


# API
# class LeadAPI(APIView):
#     def get(self, request, *args, **kwargs):
#         # The queryset we want to show
#         leads = LeadModel.objects.all()

#         #Serializing
#         leads_serialized = LeadSerializer(leads)

#         return Response({"leads": leads_serialized})

class LeadAPI(UpdateModelMixin, CreateModelMixin, ListModelMixin, GenericAPIView):
    queryset = LeadModel.objects.all()
    serializer_class = LeadSerializer

    def get(self, *args, **kwargs):
        return self.list(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# class LeadApiInstance(UpdateModelMixin ,GenericAPIView):

#     queryset = LeadModel.objects.all()
#     serializer_class = LeadSerializer


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = "login.html"

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(self.request, username=data.get(
            'username'), password=data.get('password'))
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Welcome {user.username} !')
        else:
            print('invalid')
            messages.warning(self.request, 'Please check your credentials')

        return super().form_valid(form)


def logout_view(request):
    logout(request)

    messages.success(request, 'Successfully Logged out')
    return HttpResponseRedirect('/login/')


@login_required
def delete_testleads(request):
    test_leads = LeadModel.objects.filter(isTestLead=True)
    if test_leads.exists():
        messages.success(
            request, f'{test_leads.count()} Test leads were deleted successfully')
        test_leads.delete()
    else:
        messages.success(request, 'No test leads to delete')

    return redirect('/')


@login_required
def lead_test_endpoint(request):
    if request.POST:
        # Hitting the API with requests to mimick a ajax post request
        url = f"{request.headers['Origin']}/api/leads"
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        referrer = "test"
        isAnswered = request.POST.get('isAnswered') == 'on'
        isTestLead = True

        print(request.POST)

        data = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "isAnswered": isAnswered,
            "referrer": referrer,
            "isTestLead": isTestLead
        }

        req = r.post(url=url, data=data)
        messages.success(request, 'Lead was sent successfully')
        return redirect('/')
    return render(request, f"{TEMPLATE_DIRECTORY}/test_endpoint.html")
