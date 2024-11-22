import re


def page_number_match_rules(data):
    #matches patterns such as page 236 ,pg 236
    def rule1(data):
        data = re.sub(r'(?si)page|pg',"",data).strip()
        numbers_list=[]
        if re.search(r'[0-9]+\-[0-9]+',data):
            start, end = map(int, data.split('-'))
            numbers_list = [number for number in range(start, end + 1)]
            return numbers_list

        return None

    
    #matches patterns such as 236,
    def rule2(data):
        numbers_list = []
        numbers = re.findall(r'[0-9]+',data)
        #print(numbers)
        if len(numbers) > 1:
            return None 
        numbers_list.append(int(numbers[0]))
        return numbers_list
                   
    def get_page_numbers(data):
        rules = [rule1,rule2]

        for rule in rules:
            if rule(data):
                #print( f'Pattern "{data}" is matched using '+rule.__name__ +'\n')
                return rule(data)
    
    return get_page_numbers(data)


# a =['128-129', 'page 308-309', '80', '261-264', 'page 236']
# a =[5, 16, 25, 34, 36, 41, 48, 53, '55-56', 57, 65, 75, '80-81', 85, 97, 121, '128-129', 152, 154, 155, '156-162', '179-180', 194, 232,
# '234-236', 239, 241, 256, '261-264', 286, '308-309', '313-324', 367, 377, 386, 390, 393, 395, 420, 422, 425, 427, 430, 432, 434, 467, 470, 472, 488, 490, 507]
# pageNumberList = [page_number_match_rules(str(i)) for i in a]
# pageNumberList = [i for i in pageNumberList if len(i)>0]
# pageNumberList = [number for sublist in pageNumberList for number in sublist]
# print(pageNumberList)
# lllll


def excel_pdf_name_rule(val1,val2):

    val1 = re.sub(' ',"",val1)
    val2 = re.sub(' ',"",val2)

    def rule100(val1,val2):
        # print(val1,":",val2)
        pattern = r'[0-9]+'

        if re.search(pattern,val1) and re.search(pattern,val2):
            val2List1 = re.findall(pattern,val1)
            val2List2 = re.findall(pattern,val2)
            #print(val2List1,len(val2List1),":",val2List2,len(val2List2))
            
            if len(val2List1) != len(val2List2):
                return 
                
            findList = 0
            for i in val2List1:
                if i in val2List2:
                    # print('match')
                    findList += 1

            #print(findList,">>>")

            if int(findList) == len(val2List1) == len(val2List2):
                return True
            
        return None

    # matching pattern such as 178`to-192(1).file.xlsx,178`to-192.pdf
    def rule1(val1,val2):
        regEx1 = r'\([0-9]+\).file|\([0-9]+\)'
        if re.search(regEx1,val1):
            regEx2 = r'\([0-9]+\)\.file.*|\([0-9]+\).*'
            val1 = re.sub(regEx2,'',val1)
            regEx3 = r'\.pdf'
            val2 = re.sub(regEx3,'',val2)
            
            if val1 == val2:
                return True
            
        return None
    
    #matching pattern  such as  4;90;h;4;99.file.xlsx,4;90;h;4;99.file.pdf
    def rule2(val1,val2):
        regEx1 = r'.file'
        if re.search(regEx1,val1):
            regEx2 = r'\.file.*'
            val1 = re.sub(regEx2,'',val1)
            regEx3 = r'\.pdf'
            val2 = re.sub(regEx3,'',val2)
            
            if val1 == val2:
                return True
            
        return None
    # matching pattern  file word present (391--393file.xlsx),(391--393.pdf)
    def rule3(val1,val2):
        regEx1 = r'file'
        if re.search(regEx1,val1):
            regEx2 = r'file.*'
            val1 = re.sub(regEx2,'',val1)
            regEx3 = r'\.pdf'
            val2 = re.sub(regEx3,'',val2)

            if val1 == val2:
                return True
        return None
    
    # matching pattern such as  ().xlsx) ,(.pdf) 
    def rule4(val1,val2):
        regEx = r'\..xlsx|.xlsx|.pdf'
        val1 = re.sub(regEx,'',val1)
        val2 = re.sub(regEx,'',val2)
        
        if val1 == val2:
            return True
              
        return None
    
    # matching pattern such as  (195-indexing),(195.pdf)
    def rule5(val1,val2):
        regEx1 = r'\-indexing|\_indexing'
        if re.search(regEx1,val1):
            regEx2 = r'\-indexing.*|\_indexing.*'
            val1 = re.sub(regEx2,'',val1)
            regEx3 = r'\.pdf'
            val2 = re.sub(regEx3,'',val2)
            if val1 == val2:
                return True
              
        return None
    
    # matching pattern such as  (195-.xlsx),(44-.xlsx)
    def rule6(val1,val2):
        regEx1 = r'[0-9]+\-'
        if re.search(regEx1,val1):
            regEx2 = r'\-.*'
            val1 = re.sub(regEx2,'',val1)
            regEx3 = r'\.pdf'
            val2 = re.sub(regEx3,'',val2)
            if val1 == val2:
                return True
            
        elif re.search(regEx1,val2):
            regEx2 = r'\-.*'
            regEx3 = r'\.pdf'
            val2 = re.sub(regEx3,'',val2)
            if val1 == val2:
                return True

              
        return None  

    # matching pattern such as  195-197.xlsx ,195to197.pdf or 62 to 63.pdf
    def rule7(val1,val2):
        regEx1 = r'[0-9]+\-[0-9]+'
        regEx2 = r'[0-9]+to[0-9]+'

        if re.search(regEx1,val1) and re.search(regEx2,val2):
            regEx3 = r'\-|.xlsx|to|.pdf'
            val1 = re.sub(regEx3,"",val1)
            val2 = re.sub(regEx3,"",val2)

            if val1 == val2:
                return True
        
        return None
    
    # matching pattern such as  195.xlsx ,(195to.pdf ,195 to.pdf,195 to-.pdf,195 -to-.pdf)
    def rule8(val1,val2):
        regEx1 = r'[0-9]+.xlsx'
        regEx2 = r'[0-9]to.pdf|[0-9]+to\-.pdf|[0-9]+\-to\-.pdf'
        if re.search(regEx1,val1) and re.search(regEx2,val2):
            regEx3 = r'.xlsx|to.pdf|to\-.pdf|\-to\-.pdf'
            val1 = re.sub(regEx3,"",val1)
            val2 = re.sub(regEx3,"",val2)

            if val1 == val2:
                return True

        return None

    # matching pattern such as  (250-299.xlsx,250-=299..xlsx) ,(250-=299.pdf or 250--299.pdf)
    def rule9(val1,val2):
        regEx1 = r'[0-9]+\-[0-9]+.xlsx|[0-9]+\-\=[0-9]+..xlsx'
        regEx2 = r'[0-9]+\-\=[0-9]+.pdf|[0-9]+\-\-[0-9]+.pdf|[0-9]+\=\-[0-9]+.pdf'
        if re.search(regEx1,val1) and re.search(regEx2,val2):
            regEx3 = r'\..xlsx|.xlsx|.pdf|\-|\='
            val1 = re.sub(regEx3,"",val1)
            val2 = re.sub(regEx3,"",val2)
            if val1 == val2:
                return True

        return None
    
    # matching pattern such as  (44.xlsx) ,(44-.pdf,44--.pdf) 
    def rule10(val1,val2):
        regEx1 = r'[0-9]+.xlsx'
        regEx2 = r'[0-9]+\-\-.pdf'
        if re.search(regEx1,val1) and re.search(regEx2,val2):
            regEx3 = r'.xlsx|.pdf|\-'
            val1 = re.sub(regEx3,"",val1)
            val2 = re.sub(regEx3,"",val2)
            if val1 == val2:
                return True

        return None
    
    # matching pattern such as  (File No.1321.xlsx) ,(1321.pdf) 
    def rule11(val1,val2):
        regEx1 = r'fileno.[0-9]+.xlsx'
        regEx2 = r'[0-9]+.pdf'
        if re.search(regEx1,val1) and re.search(regEx2,val2):
            regEx3 = r'fileno.|.xlsx|.pdf'
            val1 = re.sub(regEx3,"",val1)
            val2 = re.sub(regEx3,"",val2)
            if val1 == val2:
                return True
            

        
    
    
    def match_excel_pdf_name(val1,val2):
        rules = [rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11]

        for rule in rules:
            # print(rule)
            if rule(val1,val2):
                return rule.__name__
            
        return None
    return match_excel_pdf_name(val1,val2)





# a = '2a-=5 2566.xlsx'
# b = '2a-=5 2566.pdf'
# a = re.sub(' ',"",a)
# b = re.sub(' ',"",b)
# print(1,excel_pdf_name_rule(a.lower(),b.lower()))
# lll

# import os

# def a(excelDir,pdfDir):

#     for excelFile in os.listdir(excelDir):
#         # print(excelFile)
#         excelFile = re.sub(' ','',excelFile)
#         print(excelFile,"-----------------------")
#         for pdfFile in os.listdir(pdfDir):
#             pdfFile = re.sub(' ','',pdfFile)
            
#             # print(pdfFile)
#             if excel_pdf_name_rule(excelFile.lower(),pdfFile.lower()):
#                 print("rule --",excel_pdf_name_rule(excelFile.lower(),pdfFile.lower()),":",excelFile,":",pdfFile)
#                 break

#         print('__________________________________')

            

# # excelDir = r'D:\gonda_process\excel_file'
# # pdfDir  = r'D:\gonda_process\folder'
        
# excelDir = r'D:\gonda_process\Indexing_Files'
# pdfDir  = r'D:\gonda_process\Scan Files'
# a(excelDir,pdfDir)





