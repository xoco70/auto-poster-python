from ExcelService import ExcelService
from datetime import date, datetime

item_type = {
    "E": "Esquisse",
    "M": "Maquette",
    "L": "Lithographie",
    "PP": "Photo peinte",
    "PE": "Photo d'esquisse",
    "V": "Vignette",

}


class PublicationService:
    def __init__(self, excel_service):
        self.excel_service = excel_service


if __name__ == "__main__":
    excel_service = ExcelService()
    data = excel_service.get_content()
    print(len(data))
    data = excel_service.remove_void_text(data)
    print(len(data))
    data = excel_service.remove_void_hashtags(data)
    print(len(data))
    data = excel_service.remove_published(data)
    # for line in data:
    #     print(line)
    print("sans published", len(data))

    # Get data by type
    # data = excel_service.select_item_type(data, item_type['L'])
    # print(len(data))

    # Get data by UGS
    # data = excel_service.select_ugs(data, "1925027AO")
    # print(len(data))

    # Get data by date
    # data = excel_service.select_ugs(data, "1925027AO")
    my_date = datetime.today().date()
    data = excel_service.get_by_date(data, my_date)
    print("date", len(data))