from app.utils.date_utils import (
    get_dataset_reference_date,
    get_date_range,
)


reference = get_dataset_reference_date()

start, end = get_date_range("this_week")


print("Dataset reference:")
print(reference)

print("\nThis week:")
print("Start:", start)
print("End:", end)