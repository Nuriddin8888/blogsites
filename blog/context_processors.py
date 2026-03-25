def home_page(request):
    return {"person": request.user}