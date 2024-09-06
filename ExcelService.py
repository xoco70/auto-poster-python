import json
from datetime import datetime, timedelta

import pandas as pd
import math
import csv
from urllib.parse import urlencode


class ExcelService:
    def read_excel(self, file_path):
        # Lire le fichier Excel et retourner sous forme de tableau
        df = pd.read_excel(file_path, sheet_name=0)
        records = df.to_dict(orient='records')
        # Remplacer les NaT restants et autres valeurs similaires par des chaînes vides
        return self.clean_content(records)

    def clean_content(self, records):
        cleaned_records = []
        for record in records:
            cleaned_record = {key: ("" if pd.isna(value) else value) for key, value in record.items()}
            cleaned_records.append(cleaned_record)
        return cleaned_records

    def read_csv(self, file_path):
        data = []
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                data.append(row)
        return data

    def get_content(self):
        data = self.read_excel(r'./publications2.xlsx')
        result = []
        for i, row in enumerate(data):
            # recommend_pub_date = row[15]
            #
            # # Vérifier si la date est un nombre (entier ou flottant)
            # if not isinstance(recommend_pub_date, (int, float)):
            #     continue
            #
            # # Conversion de la date Excel en objet datetime
            # recommend_pub_date = pd.to_datetime('1899-12-30') + pd.to_timedelta(recommend_pub_date, unit='D')
            #
            # if not is_same_day_than_today(recommend_pub_date.day, recommend_pub_date.month):
            #     continue

            ugs = row['UGS']
            title = row['Title']
            date = row['Date']
            url = row['Permalink']
            image_url = row['Image URL']
            text = row['Commentaire Facebook']
            year = row['date2']
            hashtags = row['Hashtags']
            publish_date = row['Date de publication']
            item_type = row['Type']
            published = row['Date Pub']

            # message = urlencode({
            #     'message': f"{text}\n\n{title} - {date}\n\n{url}\n\n\n\n\n{hashtags}"
            result.append({
                # 'UGS': ugs,
                # 'title': title,
                'text': text,
                'hashtags': hashtags,
                # 'url': url,
                # 'imageUrl': image_url,
                # 'date': date,
                # 'year': year,
                'publish_date': publish_date,
                # 'item_type': item_type,
                'published': published,
            })
            # })

        return result

    def remove_void_text(self, content):
        filtered_data = [item for item in content if (item['text'])]
        return filtered_data

    def remove_void_hashtags(self, content):
        filtered_data = [item for item in content if (item['hashtags'])]
        return filtered_data

    def remove_published(self, content):
        filtered_data = [item for item in content if not (item['published'])]
        return filtered_data

    def remove_void_publish_date(self, content):
        filtered_data = [item for item in content if (item['publish_date'])]
        return filtered_data

    def select_item_type(self, content, item_type):
        filtered_data = [item for item in content if (item['item_type'] == item_type)]
        return filtered_data

    def select_ugs(self, content, ugs):
        filtered_data = [item for item in content if
                         'UGS' in item and isinstance(item['UGS'], str)
                         and ugs in item['UGS']]
        return filtered_data

    def get_by_date(self, content, date):
        filtered_data = self.remove_void_publish_date(content)
        print("sans publish date", len(filtered_data))

        filtered_data = [item for item in filtered_data if
                         'publish_date' in item and isinstance(item['publish_date'], datetime)
                         and item['publish_date'].date() == date
                         ]

        print("sans date au format string", len(filtered_data))

        filtered_data = [item for item in filtered_data if
                         isinstance(item['publish_date'], datetime)
                         ]
        print("sans date au format pas datetime", len(filtered_data))

        filtered_data = [item for item in filtered_data if
                         isinstance(item['publish_date'], datetime)
                         ]
        # Exemple de dates :
        # 1er juin
        # 1er mercredi après le 1er janvier
        # 1 er vendredi d'octobre

        return filtered_data
