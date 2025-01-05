from ExcelService import ExcelService

item_type = {
    "E": "Esquisse",
    "M": "Maquette",
    "L": "Lithographie",
    "PP": "Photo peinte",
    "PE": "Photo d'esquisse",
    "V": "Vignette",

}


class PublicationService:
    def __init__(self, excel):
        self.excel_service = excel


if __name__ == "__main__":
    excel_service = ExcelService()
    data = excel_service.get_content()
    # print(len(data))
    data = excel_service.remove_void_text(data)
    # print(len(data))
    data = excel_service.remove_void_hashtags(data)
    # print(len(data))
    data = excel_service.remove_published(data)
    data = excel_service.setsource(data)
    # for line in data:
    #     print(line)
    # print("sans published", len(data))

    # Get data by type
    # data = excel_service.select_item_type(data, item_type['L'])
    # print(len(data))

    # Get data by UGS

    data = excel_service.select_ugs(data, "1899001Z0")

    # print(len(data))

    # Get data by date

    # my_date = datetime.today().date()
    # data = excel_service.get_by_date(data, my_date)
    # print("Nombre d'oeuvres filtrées:", len(data))
    for line in data:
        print(line['title'], "(", line['year'][:4], ")")
        print(line['text'])
        print(line['url'])
        image_url = excel_service.download_image_url(line)
        if line['source'] and line['source'] != "Collection particulière" : print("Source: " + line['source'])
        if line['dimensions_du_dessin_cm']: print("Dimensions du dessin en cm: " + line['dimensions_du_dessin_cm'])
        if line['nombre_de_les']: print("Nombre de lés: " + str(int(line['nombre_de_les'])))
        if line['remarques']: print("Remarques: " + line['remarques'])
        if line['matieres']: print("Matières: " + line['matieres'])
        if line['support']: print("Support: " + line['support'])
        if line['dimensions_hors_tout_cm']: print("Dimensions hors tout en cm: " + line['dimensions_hors_tout_cm'])
        # if line['reference_devambez']: print("Reference Devambez: " + line['reference_devambez'])
        hashtags = excel_service.get_hash_tags(line['hashtags'])
        print(hashtags)
        print("\n")

# dimensions_hors_tout_cm
# reference_devambez
