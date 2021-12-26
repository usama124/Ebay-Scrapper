import openpyxl


def create_heading():

    headers = ["Main Category", "Sub Category 1", "Sub Category 2", "Sub Category 3", "Sub Category 5", "Sub Category 6", "Tags", "Title", "Price", "Weight", "Product Details", "Image 1", "Image 2", "Image 3"]
    workbook_name = "Data/ebay_products.xlsx"

    wb_obj = openpyxl.Workbook()
    sheet = wb_obj.active
    sheet.append(headers)
    wb_obj.save(filename=workbook_name)


def write_excel_file(categories_list, tags, prod_title, price, weight, prod_desc, img_name_list):
    workbook_name = "Data/ebay_products.xlsx"
    wb = openpyxl.load_workbook(workbook_name)
    page = wb.active

    data = [categories_list[0], categories_list[1], categories_list[2], categories_list[3], categories_list[4], categories_list[5], tags, prod_title, price, weight, prod_desc, img_name_list[0], img_name_list[1], img_name_list[2]]

    page.append(data)
    wb.save(filename=workbook_name)