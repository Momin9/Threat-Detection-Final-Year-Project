from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import SignupForm, LoginForm
from .models import RequestRecord
from .serializers import RequestRecordSerializer


class RequestListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = RequestRecord.objects.all()
        serializer = RequestRecordSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RequestRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@login_required(login_url='login')
def process_request(request):
    if request.method == 'POST':
        return render(request, 'dashboard.html', {'success': 'Request processed successfully!'})
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def explore(request):
    return render(request, 'explore.html')


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


class RequestListView(ListView):
    model = RequestRecord
    template_name = 'request_list.html'
    context_object_name = 'records'


class RequestCreateView(CreateView):
    model = RequestRecord
    template_name = 'request_form.html'
    fields = ['ip_address', 'device_name', 'browser', 'location', 'isp', 'threat_detected']
    success_url = reverse_lazy('request_list')


class RequestUpdateView(UpdateView):
    model = RequestRecord
    template_name = 'request_form.html'
    fields = ['ip_address', 'device_name', 'browser', 'location', 'isp', 'threat_detected']
    success_url = reverse_lazy('request_list')


class RequestDeleteView(DeleteView):
    model = RequestRecord
    template_name = 'request_confirm_delete.html'
    success_url = reverse_lazy('request_list')
