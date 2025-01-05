import csv
import os
import re
import urllib
import urllib.request
from datetime import datetime
from urllib.error import HTTPError

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def transform_source(source):
    if "Salce" in source:
        return source + " @museocollezionesalce"
    if "Poster Auctions" in source:
        return source + " @posterauctions"
    if "gallica" in source:
        return source + " @gallicabnf"
    if "Musée Français de la Brasserie" in source:
        return source + " @museefrancaisbrasserie"
    if "Blanchet" in source:
        return source + " @blanchet.associes"
    if "Omnibus" in source:
        return source + " @omnibusgallery"
    if "Swann" in source:
        return source + " @swanngalleries"
    if "Musée des Beaux-Arts, Lyon" in source:
        return source + " @mba_lyon"
    if "Archives de Paris" in source:
        return source + " @archivesdeparis"
    if "Fitzroy" in source:
        return source + " @thegaleriefitzroy"
    if "Albertina" in source:
        return source + " @albertinamuseum"
    if "Bibliothèque de Genève" in source:
        return source + " @bgegeneve"
    if "Artcurial" in source:
        return source + " @artcurial__"
    if "Forney" in source:
        return source + " @bibforney"
    if "Musée des Arts Décoratifs" in source:
        return source + " @madparis"
    if "Carnavalet" in source:
        return source + " @museecarnavalet"
    if "Forney" in source:
        return source + " @bibforney"
    if "Victoria and Albert Museum" in source:
        return source + " @vamuseum"
    if "Musée des Beaux-Arts de Reims" in source:
        return source + " @musees.reims"

    return source  # Pas de changement si aucune règle ne s'applique


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
            source = row['source']
            dimensions_du_dessin_cm = row['dimensions_du_dessin_cm']
            nombre_de_les = row['nombre_de_les']
            remarques = row['Remarques']
            matieres = (re.sub(r'\s', '', row['matieres'])
                        .replace("_x000D_", " ")
                        .strip())

            support = row['support']
            dimensions_hors_tout_cm = row['dimensions_hors_tout_cm']
            reference_devambez = row['reference_devambez']

            # message = urlencode({
            #     'message': f"{text}\n\n{title} - {date}\n\n{url}\n\n\n\n\n{hashtags}"
            result.append({
                'UGS': ugs,
                'title': title,
                'text': text,
                'hashtags': hashtags,
                'url': url,
                'imageUrl': image_url,
                'date': date,
                'year': year,
                'publish_date': publish_date,
                'item_type': item_type,
                'published': published,
                'source': source,
                'dimensions_du_dessin_cm': dimensions_du_dessin_cm,
                'nombre_de_les': nombre_de_les,
                'remarques': remarques,
                'matieres': matieres,
                'support': support,
                'dimensions_hors_tout_cm': dimensions_hors_tout_cm,
                'reference_devambez': reference_devambez,
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
        # print("sans publish date", len(filtered_data))

        filtered_data = [item for item in filtered_data if
                         'publish_date' in item and isinstance(item['publish_date'], datetime)
                         and item['publish_date'].date() == date
                         ]

        # print("sans date au format string", len(filtered_data))

        filtered_data = [item for item in filtered_data if
                         isinstance(item['publish_date'], datetime)
                         ]
        # print("sans date au format pas datetime", len(filtered_data))

        filtered_data = [item for item in filtered_data if
                         isinstance(item['publish_date'], datetime)
                         ]
        # Exemple de dates :
        # 1er juin
        # 1er mercredi après le 1er janvier
        # 1 er vendredi d'octobre

        return filtered_data

    def download_image_url(self, line):
        image_url = line['imageUrl']
        if line['imageUrl'].find('|') != -1:
            image_url = line['imageUrl'].split('|')[0]

        ugs = (re.sub(r'\s', '', line['UGS'])
               .replace("_x000D_", " ")
               .strip())
        download_folder = os.getenv('DOWNLOAD_FOLDER')
        filename = ugs + '.jpg'
        try:
            response = urllib.request.urlretrieve(image_url, download_folder + filename)
        except HTTPError as e:
            print(filename, "Error, HTTP Code is {}".format(e.code))

        # print(response)
        return line['imageUrl']

    def get_hash_tags(self, hashtags):
        # Not found
        if hashtags.lower().find("#cappiello ") == -1:
            hashtags = "#Cappiello" + " " + hashtags

        if hashtags.lower().find("#leonettocappiello ") == -1:
            hashtags = "#LeonettoCappiello" + " " + hashtags

        if hashtags.lower().find("#vintageposter ") == -1:
            hashtags = hashtags + " " + "#VintagePoster"
        return hashtags

    def setsource(self, data):
        for row in data:
            if 'source' in row:
                row['source'] = transform_source(row['source'])
        return data
