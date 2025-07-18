def reading_schedule(total_pages, total_days):
    # Calculate base pages per day and remaining pages
    base_pages = total_pages // total_days
    remainder = total_pages % total_days

    schedule = []
    current_page = 1

    for day in range(1, total_days + 1):
        # Distribute the remainder pages to the first few days
        pages_today = base_pages + 1 if day <= remainder else base_pages
        start_page = current_page
        end_page = current_page + pages_today - 1

        schedule.append({
            'Day': day,
            'Start Page': start_page,
            'End Page': end_page
        })

        current_page = end_page + 1

    return schedule


# Example usage:
if __name__ == "__main__":
    total_pages = int(input("Enter total number of pages: "))
    total_days = int(input("Enter number of days to finish the book: "))

    plan = reading_schedule(total_pages, total_days)

    for day in plan:
        print(f"Day {day['Day']}: Read pages {day['Start Page']} to {day['End Page']}")