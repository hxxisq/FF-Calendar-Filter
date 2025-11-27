import requests
import subprocess
from icalendar import Calendar

ff_ics_url = "https://nfs.faireconomy.media/ff_calendar_thisweek.ics?version=25f50249a94f7acf98c77d0ea83a6fe4"

try:
    response = requests.get(ff_ics_url) # download the calendar file
    response.raise_for_status() # check for error
    ics_data = response.text
except requests.exceptions.RequestException as e: # handle download error
    print(f"Error downloading calendar: {e}")
    exit(1)

# parsing the ics data
try:
    cal = Calendar.from_ical(ics_data)
except Exception as e:
    print(f"Error parsing calendar: {e}")
    exit(1)

filtered_cal = Calendar() # new calendar for filtered events
count_event = 0

for component in cal.walk(): # walking through the calendar events
    if component.name == "VEVENT":
        summary = component.get("summary")
        description = component.get("description")

        if (summary and "⁂" in summary and "US" in summary
                and description and "Impact: High" in description): # filtering for high impact usd news events
            filtered_cal.add_component(component)
            count_event += 1

        if summary and "US Bank Holiday" in summary: # filtering for us bank holidays news events
            filtered_cal.add_component(component)
            count_event += 1

# exit code if no events wee found
if count_event == 0:
    print("No USD high impact events found this week")
    exit(0)

output_path = "usd_high_impact.ics"

# saving the new filtered calendar file
try:
    with open(output_path, "wb") as f:
        f.write(filtered_cal.to_ical())
    print(f"\n {count_event} USD high impact events to {output_path}")
except IOError as e:
    print(f"Error saving to file: {e}")
    exit(1)

subprocess.run(["open", output_path]) # automatically open the file