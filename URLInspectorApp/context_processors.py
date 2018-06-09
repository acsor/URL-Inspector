def global_app_context(request):
    return {
        "global": {
            "length_url_max": 50,
            "length_url_min": 30,
            # Seconds to wait before an incomplete inspection's page is
            # refreshed
            "inspection_refresh": 7,
        }
    }
