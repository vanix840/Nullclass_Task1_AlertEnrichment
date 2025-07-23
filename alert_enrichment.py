import csv
import requests

def enrich_ip(ip):
    try:
        # Using ip-api.com for free IP enrichment
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return data['country'], data['regionName'], data['city'], data['isp']
        else:
            return "Unknown", "Unknown", "Unknown", "Unknown"
    except Exception as e:
        return "Error", "Error", "Error", "Error"

input_file = "alerts.csv"
output_file = "enriched_alerts.csv"

with open(input_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    enriched_data = []

    for row in reader:
        country, region, city, isp = enrich_ip(row["ip"])
        row["country"] = country
        row["region"] = region
        row["city"] = city
        row["isp"] = isp
        enriched_data.append(row)

with open(output_file, "w", newline="") as csvfile:
    fieldnames = ["ip", "user", "country", "region", "city", "isp"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in enriched_data:
        writer.writerow(row)

print(f"[✅] Enriched {len(enriched_data)} alerts and saved to {output_file}")
