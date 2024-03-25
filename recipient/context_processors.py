

def my_context_processor(request):
    # Здесь вы можете определить любые данные, которые вы хотите добавить в контекст шаблона
    return {
        'site_name': 'Мой сайт',
        'current_year': 2024,
    }