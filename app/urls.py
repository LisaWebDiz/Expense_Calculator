from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers

from app.forms.auth import LoginForm
from app.views.all_time import AllTimeExpensesView
from app.views.analysis import AnalysisView
from app.views.auth import RegistrationView
from app.views.budget import MonthlyBudgetViewSet, MonthlyBudgetUpdateView
from app.views.category import CategoryViewSet, add_category
from app.views.current_year import CurrentYearExpensesView
from app.views.expense import AddExpenseView, ExpenseUpdateView, ExpenseDeleteView, ExpenseViewSet
from app.views.index import IndexView
from app.views.info import InfoView
from app.views.month_alimony import MonthAlimonyView
from app.views.previous_month import PreviousMonthExpensesView
from app.views.previous_year import PreviousYearExpensesView

router = routers.DefaultRouter()
router.register('expense', ExpenseViewSet, basename='expenses')
router.register('category', CategoryViewSet, basename='category')
router.register('budget', MonthlyBudgetViewSet, basename='budget')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view(), name='index'),

    path('add-category/', add_category, name='add-category'),
    path('add-expense/', AddExpenseView.as_view(), name='add-expense'),

    path('budget/update/<int:pk>/', MonthlyBudgetUpdateView.as_view(), name='edit-budget'),

    path('app_html/analysis/', AnalysisView.as_view(), name='analysis'),

    path('app_html/month-alimony/', MonthAlimonyView.as_view(), name='month-alimony'),

    path('expense/update/<int:pk>/', ExpenseUpdateView.as_view(), name='edit-expense'),
    path('expense/delete/<int:pk>/', ExpenseDeleteView.as_view(), name='delete-expense'),
    path('app_html/info/<int:category_id>/', InfoView.as_view(), name='info'),

    path('app_html/previous-month-expenses/', PreviousMonthExpensesView.as_view(), name='previous-month'),
    path('app_html/current-year-expenses/', CurrentYearExpensesView.as_view(), name='current-year'),
    path('app_html/previous-year-expenses/', PreviousYearExpensesView.as_view(), name='previous-year'),
    path('app_html/all-time-expenses/', AllTimeExpensesView.as_view(), name='all-time'),

    path('api/v1/', include(router.urls)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(
        template_name='auth/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
