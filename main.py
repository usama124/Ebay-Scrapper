import json
import ExcelWriter as excel
import Scrape_categories as scrapper


def read_cat_stored_urls():
    list_prod = []
    f = open("record/cat_urls_list.txt", "r")
    line = f.readline().split("\n")[0]
    while line != "" and line != None:
        list_prod.append(json.loads(line))
        line = f.readline().split("\n")[0]
    f.close()
    return list_prod


def read_scraped_products():
    list_prod = []
    f = open("record/scraped_products.txt", "r")
    line = f.readline().split("\n")[0]
    while line != "" and line != None:
        list_prod.append(line)
        line = f.readline().split("\n")[0]
    f.close()
    return list_prod


def write_scraped_products(url):
    f = open("record/scraped_products.txt", "a")
    f.write(url + "\n")
    f.close()


def write_not_scraped_products(url):
    f = open("record/skipped_products.txt", "a")
    f.write(url + "\n")
    f.close()


if __name__ == '__main__':
    excel.create_heading()

    print("\n\nScraping products...\n\n")

    main_url = "https://www.ebay.co.uk/sch/i.html?_dmd=2&iconV2Request=true&_ssn=2020foodie&store_cat=0&store_name=2020foodie&_oac=1&_pgn="
    counter = 1
    product_urls_list = []
    while True:
        if counter >= 11:
            break
        page_url = main_url + str(counter)
        page_obj = scrapper.get_page_obj(page_url)
        if page_obj is None:
            break
        products_grid = page_obj.find("ul", attrs={"class": "srp-results srp-grid clearfix"})
        pagination_div = products_grid.find("div", attrs={"class": "srp-river-answer srp-river-answer--BASIC_PAGINATION_V2"})
        pagination_div.decompose()
        products_grid_items = products_grid.findAll("li")
        for product in products_grid_items:
            prod_url = product.find("a", attrs={"class": "s-item__link"}).attrs["href"]
            product_urls_list.append(prod_url)
        counter = counter + 1
    product_urls_list = list(set(product_urls_list))

    counter = 1
    for product in product_urls_list:
        scrapper.scrape_product(product, counter)
        counter = counter + 1
    print("Finish...")

