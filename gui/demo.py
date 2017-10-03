s = '{categoryId:"25",channelId:"UCttspZesZIDEwwpVIgoZtWQ",channelTitle:"IndiaTV",commentCount:0,description:["Banks","will","attend","their","customers","only","today","Senior","citizens","exempted","have","been","exempted","Since","last","ten","days","banks","were","unable","to","do","their","routine","works","and","were","busy","in","exchanging","currency","notes","of","Rs","500","and","Rs","1000","SUBSCRIBE","to","India","TV","Here","http","goo","gl","fcdXM0","Follow","India","TV","on","Social","Media","Facebook","https","www","facebook","com","indiatvnews","Twitter","https","twitter","com","indiatvnews","Download","India","TV","Android","App","here","http","goo","gl","kOQvVB"],dislikeCount:1,etag:""gMxXHe-zinKdE9lTnzKu8vjcmDI/9uChcObApWf5El1iHJlX6RW-sB4"",favoriteCount:0,id:"AXgIcU7yRiw",likeCount:18,publishedAt:"2016-11-19T02:58:55.000Z",tags:["currency exchange","bank employees","bank employees heart attack","demonetisation","children pocket money","note ban","queue outside ATMs","rs 500 and rs 1000","currency ban in india","hindi news","India TV","india tv news","india tv live","india tv news live","india tv hindi","india tv youtube","india tv hindi news","india tv channel live"],thumbnail:"https://i.ytimg.com/vi/AXgIcU7yRiw/default.jpg",title:"Banks Will Serve Their Customers Only Today; Senior Citizens Exempted",viewCount:2542}'
# s = string.replace("{" ,"");
# finalstring = s.replace("}" , "");

# #Splitting the string based on , we get key value pairs
# list = finalstring.split(",")

# dict ={}
# for i in list:
#     #Get Key Value pairs separately to store in dictionary
#     keyvalue = i.split(":")

#     #Replacing the single quotes in the leading.
#     m= keyvalue[0].strip('\'')
#     m = m.replace("\"", "")
#     dict[m] = keyvalue[1].strip('"\'')

#print dict
l = s.split(':')
for i in l:
	print i
