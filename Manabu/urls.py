from django.urls import include, path

urlpatterns = [ 
    path('api/v1/', include('app.urls'))
]


    #path('books/<int:id>/', BookView.as_view(allowed_methods=['GET', 'PUT', 'DELETE']), name='book_detail'),
    #path('books/', BookView.as_view(allowed_methods=['GET']), name='book_list'),