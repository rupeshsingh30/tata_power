# import re
# text = '''  Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented and functional programming.
# '''


# if  re.search(r'(?si)add\:\sservice\stax.*?add\:\seducation\scess',text):
#     service_tax_gst = re.search(r'(?si)add\:\sservice\stax.*?add\:\seducation\scess',text).group()
#     service_tax_gst = re.findall(r'[0-9,.]+',service_tax_gst)[-1]
# else:
#     service_tax_gst = ''
# print('service_tax_gst :',service_tax_gst,'\n\n')



def yep():

    return [1,2,3]


[a,b,c] = yep()


print(a,">>>",b,">>>",c)