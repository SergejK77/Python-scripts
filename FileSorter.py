import os

file_list = []
extentions_list = list()
sorted_dict = {}


def sort_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(file)
            ext = file.split(".")[1]
            ext = "." + ext
            if ext not in extentions_list:
                extentions_list.append(ext)
                sorted_dict[ext] = []
            else:
                pass
            sorted_dict[ext].append([file])
    print(sorted_dict)
    for key in sorted_dict.keys():
        pkey = path+key
        if not os.path.isdir(path+key):
            os.mkdir(pkey)
        for a in sorted_dict.get(key):
            for b in a:
                if os.path.isfile(path+str(b)):
                    os.rename(path + str(b), path + str(key) + '/' + str(b))
        else:
            continue


if __name__ == "__main__":
    fdir = "C:/Users/Serge/Desktop/FF/"
    sort_files(fdir)
