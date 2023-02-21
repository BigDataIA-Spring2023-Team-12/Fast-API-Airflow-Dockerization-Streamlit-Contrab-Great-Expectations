# function to generate file download link from filename
def url_gen(input):
    arr = input.split("_")
    tproduct_code = arr[1].split("-")
    s1 = tproduct_code[2]
    finalProductCode = tproduct_code[0] + "-" + tproduct_code[1] + "-" + ''.join([i for i in s1 if not i.isdigit()])
    date = arr[3]
    year = date[1:5]
    day_of_year = date[5:8]
    hour = date[8:10]
    fs = "https://noaa-goes18.s3.amazonaws.com/{}/{}/{}/{}/{}".format(finalProductCode, year, day_of_year, hour, input)
    return fs
