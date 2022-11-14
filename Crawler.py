import os
import shutil
import subprocess

import requests
from bs4 import BeautifulSoup
import wget
import datetime

# top_URL = ["https://wire3.com", "https://help.wire3.com/hc/en-us"]
URLs = []
src_list = []
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/74.0.3729.169 Safari/537.36"
}
base_URL = "https://wire3.com"
PATH = os.getcwd()
Downloads = os.path.join(PATH, "Downloads")
Downloads_dir = {"Images": os.path.join(Downloads, "Images"),
                 "Links": os.path.join(Downloads, "Links"),
                 "Scripts": os.path.join(Downloads, "Scripts")
                 }
Reports = os.path.join(PATH, "Reports")
Today = datetime.datetime.today()
Date = Today.date().__str__()
Time = Today.time().strftime("%H-%M-%S")
Today = Today.date().__str__() + " " + Today.time().strftime("%H:%M:%S")

Todays_Reports = os.path.join(Reports, Date)
Latest_Report = Todays_Reports

Report_Intro = "For Wire3 Eyes Only \n \n" \
               "This is an automatically generated report. \n" \
               "Script used to generate report: Metadata_crawler.py \n" \
               "The script was created by: Vimal Seshadri Raguraman \n" \
               "Generated on: {}".format(Today)


def main():
    file_manager()
    scrape(base_URL)
    metadata_extractor(Downloads)
    print("Latest Report: ", Latest_Report)
    print("Total URLs: ", len(URLs))
    print("Total Images: ", len(os.listdir(Downloads_dir["Images"])))
    print("Total Scripts: ", len(os.listdir(Downloads_dir["Scripts"])))


def file_manager():
    if not os.path.exists(Downloads):
        os.mkdir(Downloads)
        for key in Downloads_dir.keys():
            os.mkdir(Downloads_dir[key])
    else:
        shutil.rmtree(Downloads)
        os.mkdir(Downloads)
        for key in Downloads_dir.keys():
            os.mkdir(Downloads_dir[key])

    if not os.path.exists(Reports):
        os.mkdir(Reports)
    else:
        if not os.path.exists(os.path.join(Reports, Date)):
            os.mkdir(os.path.join(Reports, Date))


def extractor(bs_object):
    links = bs_object.find_all("link")
    images = bs_object.find_all("img")
    scripts = bs_object.find_all("script")

    for i in links:
        if "src" in i.attrs.keys():
            src = i.attrs["src"]
            if src.startswith("/"):
                sub_src = base_URL + src
                if not sub_src.endswith("/"):
                    sub_src += "/"
                src = sub_src
            if src not in src_list and "facebook" not in src:
                src_list.append(src)
                try:
                    wget.download(src, Downloads_dir["Scripts"])
                except:
                    continue

    for i in images:
        if "src" in i.attrs.keys():
            src = i.attrs["src"]
            if src.startswith("/"):
                sub_src = base_URL + src
                if not sub_src.endswith("/"):
                    sub_src += "/"
                src = sub_src
            if src not in src_list and "facebook" not in src:
                src_list.append(src)
                try:
                    wget.download(src, Downloads_dir["Images"])
                except:
                    continue

    for i in scripts:
        if "src" in i.attrs.keys():
            src = i.attrs["src"]
            if src.startswith("/"):
                sub_src = base_URL + src
                if not sub_src.endswith("/"):
                    sub_src += "/"
                src = sub_src
            if src not in src_list and "facebook" not in src:
                src_list.append(src)
                try:
                    wget.download(src, Downloads_dir["Scripts"])
                except:
                    continue


def scrape(site):
    r = requests.get(site, headers=header)
    soup = BeautifulSoup(r.content, "html.parser")
    extractor(soup)
    links = soup.find_all("a")

    for i in links:
        s = None
        if "href" not in i.attrs.keys():
            continue

        if i.attrs["href"].startswith("/"):
            sub_site = site + i.attrs["href"]
            if not sub_site.endswith("/"):
                sub_site += "/"
            s = sub_site

        elif not i.attrs["href"].startswith("https"):
            continue

        else:
            sub_site = i.attrs["href"]
            if not sub_site.endswith("/"):
                sub_site += "/"
            s = sub_site

        if s is not None and s not in URLs:
            URLs.append(s)
            scrape(site)


def metadata_extractor(dir):
    report_name = "Metadata Report {}.txt".format(Today)
    report_path = os.path.join(Todays_Reports, report_name)
    f = open(report_path, "a+")
    f.write("{} \n \n \n \n".format(Report_Intro))
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        output = subprocess.run(["exiftool", file_path], stdout=subprocess.PIPE)
        f.write(output.stdout.decode("utf-8"))
        f.write("\n\n")
    f.close()


main()
