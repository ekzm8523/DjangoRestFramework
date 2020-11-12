from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from news.models import Article
from news.api.serializers import ArticleSerializer
# Create your views here.

@api_view(["GET", "POST"])
def article_list_create_api_view(request):
    if request.method == "GET":
        articles = Article.objects.filter(active=True)
        serializer = ArticleSerializer(articles, many=True)
        # many => queryset에 대응. many 없으면 instance 1개가 올 것으로 기대하고 있어 에러가 발생함.
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ArticleSerializer(data=request.data)
        if serializer.isvalid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT","DELETE"])
def article_detail_api_view(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({"error" : {
            "code" : 404,
            "message" : "Article not found"
        }}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
