from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead, Agent
from .forms import LeadModelForm, LeadForm, CustomUserCreationForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from agents.mixins import OrganizerAndLoginRequiredMixin

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(TemplateView):
    template_name = "landing.html"

def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user

        #filter for organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            #filter for agent
            queryset = queryset.filter(agent__user=user)
        return queryset

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
        }
    return render(request, "leads/lead_list.html", context)

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html"
    def get_queryset(self):
        user = self.request.user

        #filter for organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            #filter for agent
            queryset = queryset.filter(agent__user=user)
        return queryset
    context_object_name = "lead"

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        #todo send email
        send_mail(
            subject = "A lead has been created",
            message = "Go to the site to see the new lead",
            from_email = "test@test.com",
            recipient_list= ["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)
        
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
            "lead": lead,
            "form": form
        }
    return render(request, "leads/lead_update.html", context)

class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)
    template_name = "leads/lead_delete.html"
    
    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

