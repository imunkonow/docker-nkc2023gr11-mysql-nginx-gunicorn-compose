from django.urls import path

from . import views

urlpatterns = [
    path('', views.question_Main, name='question_Main'),
    path('question_Main', views.question_Main, name='question_Main'),
    path('mensetu_Main', views.mensetu_Main, name='mensetu_Main'),
    path('answer_List', views.answer_List, name='answer_List'),
    path('question', views.question, name='question'),
    path('question_List', views.question_List, name='question_List'),
    path('mensetu', views.mensetu, name='mensetu'),
    path('hensyu', views.hensyu, name='hensyu'),
    path('hensyu_tuika', views.hensyu_tuika, name='hensyu_tuika'),

    # # 6/27
    # path('login', views.login, name='login'),
    # path('login_Main', views.login_Main, name='login_Main'),
    # path('account_create', views.account_create, name='account_create'),

    # 6/29
    path('mensetu/<int:question_id>/', views.mensetu,
         name='mensetu/<int question_id>/'),

    # 7/1
    path('delete/<int:question_id>/', views.delete,
         name='delete/<int question_id>/'),
    path('update/<int:question_id>/', views.update,
         name='update/<int question_id>/'),

    # 7/12
    path('feedback_List', views.feedback_List, name='feedback_List'),
    path('feedback_yet', views.feedback_yet, name='feedback_yet'),
    path('question_yet', views.question_yet, name='feedback_yet'),
    path('feedback', views.feedback, name='feedback'),
    path('feedback_let/<int:question_id>/', views.feedback_let,
         name='feedback_let/<int question_id>/'),
    path('signup', views.AccountRegistration.as_view(), name='register'),

    path('login', views.Login, name='Login'),
    path("logout", views.Logout, name="Logout"),

    # 9/16
    path('profile', views.profile.as_view(), name='profile'),
    path('mail', views.mail.as_view(), name='mail'),

    # 11/1
    path("csvDLUP", views.csvDLUP, name="csvDLUP"),
    path("graph", views.utils.graph, name="graph"),




    # 11/2
    path("pdf_read", views.pdf_read_class.pdf_read, name="pdf_read"),

    # 11/4
    path("allinput", views.allinput, name="allinput"),
    path('answer_let/<int:question_id>/', views.answer_let,
         name='answer_let/<int question_id>/'),
    path('feedback_only/<int:question_id>/', views.feedback_only,
         name='feedback_only/<int question_id>/'),

    # 11/8
    path("attend", views.attend, name="attend"),
]
