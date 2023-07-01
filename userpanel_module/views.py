from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DeleteView
from account_module.models import User
from contacts_module.forms import ContactForm
from contacts_module.models import Contact
from django.contrib import messages
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .serializers import ContactSerializer
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

#-------------------------------------UserPanelDashboard--------------------------------------------------
class UserPanelDashboardAPIView(APIView):
    def get(self, request):
        contacts = Contact.objects.filter(user=request.user)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        selected_contacts = request.data.get('selected_contacts', [])
        Contact.objects.filter(id__in=selected_contacts).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPanelDashboardPage(View):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'
        
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        else:
            contacts = Contact.objects.filter(user=request.user).order_by('name')
            return render(request, self.template_name, {'contacts': contacts})
    
    @classmethod
    def user_panel_menu_component(cls, request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        else:
            contacts = Contact.objects.order_by('name')
            return render(request, 'contacts/contact_list.html', {'contacts': contacts})

class ContactListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login_page')
        else:
            contacts = Contact.objects.filter(user=request.user).order_by('name')
            return render(request, 'user_panel_module/components/user_panel_menu_component.html', {'contacts': contacts})

    def post(self, request):
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        Contact.objects.create(name=name, phone_number=phone_number, email=email, user=request.user)
        return redirect('user_panel_dashboard')

#---------------------------------adding contact with api-------------------------------------------------

class AddContactAPIView(APIView):
    
    def get(self, request):
        # Render the add contact form
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return render(request, 'contacts/add_contact.html')

    def post(self, request):
        # Handle the form submission when adding a new contact
        contact_form = ContactForm(request.data)
        if contact_form.is_valid():
            # Extract the form data
            name = contact_form.cleaned_data['name']
            phone_number = contact_form.cleaned_data['phone_number']
            email = contact_form.cleaned_data['email']
            try:
                user = request.user
                # Create a new contact object
                contact = Contact.objects.create(name=name, phone_number=phone_number, email=email, user=user)
                # Return a success response with serialized data
                serializer = ContactSerializer(contact)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                # Handle the case where the email is already used
                return Response({'error': 'The email is already used. Please provide a unique email.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return a validation error response
            return JsonResponse(contact_form.errors, status=status.HTTP_400_BAD_REQUEST)       
        
#------------------------------------------Delete-----------------------------------------------
class DeleteSelectedContactsView(APIView):
    def post(self, request):
        selected_contact_ids = request.data.get('selected_contact_ids', [])
        Contact.objects.filter(id__in=selected_contact_ids).delete()
        return Response({'message': 'Selected contacts deleted successfully'}, status=status.HTTP_200_OK)


class DeleteSelectedContactsView(View):
    def post(self, request):
        selected_contacts = request.POST.getlist('selected_contacts')
        # Perform the deletion logic based on the selected contacts
        try:
            Contact.objects.filter(id__in=selected_contacts).delete()
            messages.success(request, 'Selected contacts deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting selected contacts: {str(e)}')
        
        return redirect('user_panel_dashboard')

# class DeleteSelectedContacts(View):
#     def post(self, request):
#         selected_contacts = request.POST.getlist('contact_ids')
        
#         try:
#             Contact.objects.filter(id__in=selected_contacts).delete()
#             messages.success(request, 'Selected contacts deleted successfully.')
#         except Exception as e:
#             messages.error(request, f'Error deleting selected contacts: {str(e)}')
        
#         return redirect('user_panel_dashboard')
    
class DeleteContactAPIView(DeleteView):
    model = Contact
    template_name = 'contacts/delete_contact.html'
    success_url = reverse_lazy('user_panel_dashboard')
    
    def get_object(self, queryset=None):
        identifier = self.kwargs.get('identifier')  # Get the identifier from URL parameters
        return self.model.objects.get(identifier=identifier)
