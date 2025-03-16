import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from mongo_datatables import DataTables, DataField, Editor
from .models import MongoConnection


BOOKS_DATA_FIELDS = [
    DataField("Title", "string"),
    DataField("Author", "string"),
    DataField("PublisherInfo.Date", "date", alias="Published"),
    DataField("Themes", "array"),
    DataField("Pages", "number"),
    DataField("Rating", "number")
]


class IndexView(View):
    def get(self, request):
        return render(request, 'books/index.html')


@method_decorator(csrf_exempt, name='dispatch')
class BooksDataTablesView(View):
    def post(self, request):
        request_args = {}
        
        try:
            request_args = json.loads(request.body)
            mongo = MongoConnection()
            data = DataTables(mongo, 'books', request_args, data_fields=BOOKS_DATA_FIELDS).get_rows()
            return JsonResponse(data)
            
        except Exception as e:
            error_response = {
                'error': str(e),
                'data': [],
                'draw': request_args.get('draw', 1),
                'recordsTotal': 0,
                'recordsFiltered': 0
            }
            print("DataTables error:", str(e))
            return JsonResponse(error_response)



@method_decorator(csrf_exempt, name='dispatch')
class BooksEditorView(View):
    def post(self, request):
        request_args = {}
        
        try:
            request_args = json.loads(request.body)
            doc_id = request.GET.get('id', None)
            mongo = MongoConnection()
            collection = 'books'  # Hardcoded for books collection
            
            # Use data_fields directly with the new Editor implementation
            data = Editor(mongo, collection, request_args, doc_id, data_fields=BOOKS_DATA_FIELDS).process()
            return JsonResponse(data)
            
        except Exception as e:
            error_response = {
                'error': str(e),
                'data': [],
                'fieldErrors': []
            }
            print("Editor error:", str(e))
            return JsonResponse(error_response)
