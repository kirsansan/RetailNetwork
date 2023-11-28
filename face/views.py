from django.shortcuts import render


# HomePage View in FBV notation
def home_page_view(request):
    context = {
        'title': "Retail Selling service",
    }
    return render(request, 'face/index.html', context)
