# How to convert a float object to a string in Python
# https://www.adamsmith.haus/python/answers/how-to-convert-a-float-object-to-a-string-in-python
# Python(18)_带参数的url的拼接方式
# https://www.cnblogs.com/sunnybowen/p/10177063.html
latitude = 35.6761919
longitude = 139.6503106
foursquare_client_id = 'PMXQTRX2WOU4EOZTSAXELWD2CYGFJ4TC0E55GIERDIVA2WKQ'
foursquare_client_secret = 'ROKNHTWGHJIEHEYYRFF04FJTXKPCWJWLU2OD5XHSDDHVSBCL'
mealType = 666
# url = "https://api.foursquare.com/v3/places/match"
# url1 = url + "?" + "name=" + mealType + "&ll=" + latitude + "," + longitude
url2 = ('https://api.foursquare.com/v3/places/match?name=%s&ll=%s,%s' % (mealType,latitude,longitude))
# url1=('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))
print(url2)

