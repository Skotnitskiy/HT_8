def get_pages_numbers(pages=2025, records_per_page=25):
    numbers = list(range(0, pages, records_per_page))
    return numbers
