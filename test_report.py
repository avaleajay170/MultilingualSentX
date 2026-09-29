from app import create_app

app = create_app()

with app.test_request_context():
    from app.routes.bulk import download_bulk_report
    response = download_bulk_report("6abb68935d349e5f4b4e2010")
    print("SUCCESS:", response)