# encoding: UTF-8
import requests
import re


def download_file(url, filename):
    # NOTE the stream=True parameter
    # response = requests.head(url)

    # if "Content-Length" in response.headers:
    #     print("length---" + response.headers["Content-Length"])
    # if "Content-Length" in response.headers and int(response.headers["Content-Length"]) > 100000:
    #     r = requests.get(url, stream=True)
    #     with open(filename, 'wb') as f:
    #         for chunk in r.iter_content(chunk_size=1024):
    #             if chunk:  # filter out keep-alive new chunks
    #                 f.write(chunk)
    #                 f.flush()
    # return filename
    r = requests.get(url, stream=True)
    if len(r.content) > 50000:
        # print("img url----" + url + "     " + str(len(r.content)))
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return True
    else:
        return False


def update_readme(repourl, language, img_names):
    with open("README.md", "r+") as f:
        text = f.read()
        if language == "Java":
            tag = "------------------------------------------ |"
            print(text.find(tag))
            f.seek(text.find(tag))
            strs = text.split(tag)[1]
            pass
        else:
            tag = "---------------------------------------- |"
            f.seek(text.find(tag))
            strs = text.split(tag)[1] + tag + text.split(tag)[2]
        contexts = tag + "\n" + "|[" + repourl.split("/")[-1] + "](" + repo_url + ")\t" + \
                   "Language:" + language + "  |"
        for imgname in img_names:
            contexts += "![" + repourl.split("/")[-1] + "](resources/" + imgname + ")"
        contexts += strs
        f.write(contexts)


def get_repo_info(url):
    r = requests.get(url)
    text = r.text
    text = text.replace("\t", "")
    text = text.replace("\n", "")
    return text


def get_imginfo_list(context):
    pattern = re.compile(r'<a href=([^<>]+)><img src=([^<>]+)></a>')
    match = pattern.findall(context)
    return match


def get_programming_language(contexts):
    pattern = re.compile(r'itemprop="keywords">([^/<>]+)</span>')
    match = pattern.search(contexts)
    language = ""
    if match:
        language = match.group(1)
    return language


repo_url = 'https://github.com/ImmortalZ/StereoView'
print("start---")
context = get_repo_info(repo_url)  # 'https://github.com/cymcsg/Awesome-Mobile-UI'
lang = get_programming_language(context)
print("Language---"+lang)
img_name_list = []
imginfo_list = get_imginfo_list(context)
if len(imginfo_list) > 0:
    for imginfo in imginfo_list:
        imgurl = imginfo[0].split('"')[1]
        if imgurl.startswith("/"):
            imgurl = "https://github.com" + imgurl
        if imgurl.startswith("https://github.com"):
            imgurl = imgurl.replace("blob", "raw")
            pass
        imgName = imgurl.split("/")[4] + "_" + imgurl.split("/")[-1]

        if len(img_name_list) < 5:
            if download_file(imgurl, "resources/" + imgName):
                img_name_list.append(imgName)
                print("imgName--" + imgName)
update_readme(repo_url, lang, img_name_list)
