import uuid, requests
import re
from bs4 import BeautifulSoup
import DownloadImage as downloader
import ExcelWriter as excel


def get_page_obj(url):
    error_count = 0
    error = True
    page_obj = None
    while error and error_count < 3:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
            r.encoding = "utf-8"
            page = r.text
            page_obj = BeautifulSoup(page, "lxml")
            error = False
        except:
            error = True
            error_count = error_count + 1
            print("%s URL not accessible " % (url))

    return page_obj


def get_categories_tags(page_obj):
    tags_list = []
    tags_ul = page_obj.find("ul", attrs={"aria-label": "Listed in category:"}).findAll("li")
    for tag in tags_ul:
        try:
            tag_text = tag.find("a").text.replace("\n", "").replace(",", "").strip()
            tags_list.append(tag_text)
        except:
            pass
    while "" in tags_list: tags_list.remove("")
    tags = "|".join(tags_list)
    while len(tags_list) < 6:
        tags_list.append("")

    return (tags_list, tags)


def get_alphabets_unit(value):
    only_alpha = ""
    for char in value:
        if char.isalpha():
            only_alpha += char
    return only_alpha

def convert_weight_to_kg(weight : str):
    if weight is None or weight == "":
        return None
    non_decimal = re.compile(r'[^\d.-]+')
    unit = get_alphabets_unit(weight).strip()
    try:
        if unit.lower() == "kg":
            return weight
        elif unit.lower() == "l":
            return weight
        elif unit.lower() == "g":
            weight = non_decimal.sub('', weight).strip()
            if "." in weight:
                weight = str(float(weight) / 1000) + "Kg"
            else:
                weight = str(int(weight) / 1000) + "Kg"
        elif unit.lower() == "ml":
            weight = non_decimal.sub('', weight).strip()
            if "." in weight:
                weight = str(float(weight) / 1000) + "L"
            else:
                weight = str(int(weight) / 1000) + "L"
        else:
            weight = None
    except Exception as e:
        weight = None
        pass
    return weight


def download_all_images(images_list):
    img_name_lst = []
    tag = uuid.uuid4().__str__()
    counter = 1
    for img in images_list:
        try:
            img_link = img.find("img").attrs["src"]
            img_link_temp = img_link.split("/")[-1].split(".")[0]
            img_link_temp = "/" + img_link_temp + "."
            img_link = img_link.replace(img_link_temp, "/s-l500.")
        except:
            img_link = img
        image_name = downloader.download_image(img_link, tag + "_" + str(counter))
        img_name_lst.append(image_name)
        counter = counter + 1

    while len(img_name_lst) < 3:
        img_name_lst.append("")

    return img_name_lst


def find_weight_from_title(title : str):
    weight = ""
    splitted_title = title.split(" ")
    for sp_t in splitted_title:
        sp_t = sp_t.split("x")[-1]
        if "g" in sp_t.lower() or "kg" in sp_t.lower() or "ml" in sp_t.lower() or "l" in sp_t.lower():
            weight = convert_weight_to_kg(sp_t)
            if weight is not None:
                break
    if weight is None:
        weight = ""
    return weight


def scrape_product(link, counterr):
    page_obj = get_page_obj(link)
    if page_obj is None:
        return
    try:
        prod_title = page_obj.find("h1", attrs={"id": "itemTitle"}) #.text.strip()
        prod_title.find("span").decompose()
        prod_title = prod_title.text.strip()
        categories_list, tags = get_categories_tags(page_obj)
        try:
            img_div_list = page_obj.find("div", attrs={"id": "vi_main_img_fs"}).findAll("li")
        except:
            img_div_list = [page_obj.find("img", attrs={"id": "icImg"}).attrs["src"]]
        img_name_list = download_all_images(img_div_list)
        prod_desc_box = str(page_obj.find("div", attrs={"id": "viTabs_0_is"}))
        prod_desc_text = str(page_obj.find("div", attrs={"id": "desc_wrapper_ctr"}))
        prod_desc = prod_desc_box + prod_desc_text
        try:
            weight = find_weight_from_title(prod_title)
        except:
            weight = ""
            pass
        try:
            cost_div = page_obj.find("span", attrs={"id": "prcIsum"})
            price = cost_div.text.strip().split(" ")[0]
        except:
            price = ""
            pass
        excel.write_excel_file(categories_list, tags, prod_title, price, weight, prod_desc, img_name_list)
        print(str(counterr) + " => Product scraped...")
    except Exception as e:
        print(str(counterr) + " => Product failed to scrape...")
        pass
