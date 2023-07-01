from django.urls import path
from .views import (
    AddContactAPIView,
    DeleteContactAPIView,
    DeleteSelectedContactsView,
    UserPanelDashboardAPIView,
    UserPanelDashboardPage,
    ContactListView,
)

urlpatterns = [
    path('', UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    path('add-contact/', AddContactAPIView.as_view(), name='add_contact'),
    path('delete-contact/<uuid:identifier>/', DeleteContactAPIView.as_view(), name='delete_contact'),
    path('contact_list/', ContactListView.as_view(), name='contact_list'),
    path('api/user-panel/', UserPanelDashboardAPIView.as_view(), name='user_panel_dashboard_api'),
    path('delete-selected/', DeleteSelectedContactsView.as_view(), name='delete_selected_contacts'),
    path('api/user-panel/<int:contact_id>/', UserPanelDashboardAPIView.as_view(), name='delete_contact_api'),
]

# from django.urls import path
# from .views import (
#     DeleteContactAPIView,
#     DeleteSelectedContactsView,
#     UserPanelDashboardAPIView,
#     UserPanelDashboardPage,
#     contact_list,
#     AddContactAPIView,
# )

# urlpatterns = [
#     path('', UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
#     path('add-contact/', AddContactAPIView.as_view(), name='add_contact'),
#     path('delete-contact/<uuid:identifier>/', DeleteContactAPIView.as_view(), name='delete_contact'),
#     path('contact_list/', contact_list.as_view(), name='contact_list'),
#     path('api/user-panel/', UserPanelDashboardAPIView.as_view(), name='user_panel_dashboard_api'),
#     path('delete-selected/', DeleteSelectedContactsView.as_view(), name='delete_selected_contacts'),
#     path('api/user-panel/<int:contact_id>/', UserPanelDashboardAPIView.as_view(), name='delete_contact_api'),
# ]

# # urlpatterns = [
# #     path('', UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    
# #     path('add-contact/', AddContactAPIView.as_view(), name='add_contact'),
# #     path('delete-contact/<uuid:identifier>/', DeleteContactAPIView.as_view(), name='delete_contact'),
    
# #     path('contact_list/', contact_list.as_view(), name='contact_list'),
# #     # path('api/contacts/', AddContactView.as_view(), name='add_contact_api'),
# #     path('api/user-panel/', UserPanelDashboardAPIView.as_view(), name='user_panel_dashboard_api'),
# #     path('delete-selected/', DeleteSelectedContactsView.as_view(), name='delete_selected_contacts'),
# #     path('api/user-panel/<int:contact_id>/', UserPanelDashboardAPIView.as_view(), name='delete_contact_api'),
# # ]
