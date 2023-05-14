import csv
import json


def covert(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if "is_published" in row:
                if row["is_published"] == "TRUE":
                    row["is_published"] = True
                else:
                    row["is_published"] = False
            if "location_id" in row:
                row["locations"] = [row["location_id"]]
                del row["location_id"]

            result.append(row)
    with open(json_file, 'w', encoding="utf-8") as f:
        j = json.dumps(result, ensure_ascii=False)
        f.write(j)


if __name__ == '__main__':
    covert("ad.csv", "ad.json", "ads.ad")
    covert("category.csv", "category.json", "ads.category")
    covert("user.csv", "user.json", "users.user")
    covert("location.csv", "location.json", "users.location")