import sys
sys.path.append(r"C:\Users\Admin\AppData\Local\Programs\Python\Python310\Lib\site-packages\aws_lib_")
from aws_lib_.aws_ocr_main import main_call
import os
import re



def trigger(input_path,output_path):
    if " " in input_path:
        old_path = input_path
        file_name = os.path.basename(input_path).replace(" ","_").replace(",","_").replace("'","_")
        new_path = os.path.dirname(old_path) + "\\" + file_name
        # print(new_path)

        os.rename(old_path,new_path)
        input_path = new_path


    if input_path.lower().endswith('.pdf'):
        file_type = 'pdf'
    elif input_path.lower().endswith('.jpeg'):
        file_type = 'jpeg'
    elif input_path.endswith('.JPG'):
        file_type = 'JPG'
    else:
        file_type = 'jpg'
    
    file_name = re.sub(r'(?si).pdf|.PDF|.Pdf|.jpg|.jpeg','',input_path)
    file_name = re.sub(r".*\\",'',file_name) #uncomment this line in case of windows
    # file_name = re.sub(r".*\/",'',file_name) # uncomment this line in case of linux
    os.chdir(output_path)
    main_call(input_path)

    inreading_count = len([file for file in os.listdir(output_path) if file.endswith('inreadingorder.txt') and file.startswith(f'{file_name}')])
    text_count = len([file for file in os.listdir(output_path) if file.endswith('text.txt')])

    inreadingorder_txt = ''
    text_txt = ''

    for i in range(1,inreading_count+1):
        f_path1 = file_name +f'-{file_type}-page-'+str(i)+'-text-inreadingorder.txt'
        f_path2 = file_name +f'-{file_type}-page-'+str(i)+'-text.txt'

        with open(f_path1,encoding='utf-8') as f1:
            lines_1 = f1.read()
            inreadingorder_txt = inreadingorder_txt+"\n--------New Page-------\n"+lines_1
        
        with open(f_path2,encoding='utf-8') as f2:
            lines_2 = f2.read()
            text_txt = text_txt+"\n--------New Page-------\n"+lines_2
    
    # for file in os.listdir(output_path):
    #     file_removal_path = os.path.join(output_path,file)
    #     os.remove(file_removal_path)

    return inreadingorder_txt,text_txt





# def remove_space(pdf_folder):

#     for file in os.listdir(pdf_folder):
#         # print(file,"<<<<<")
#         old_path = os.path.join(pdf_folder,file)
#         # print(old_path,">>>>>>>>>>")
#         if " " in old_path:
#             file_name = os.path.basename(old_path).replace(" ","_").replace(",","_").replace("'","_")
#             new_path = os.path.dirname(old_path) + "\\" + file_name
#             # print(new_path,"new path")

#             os.rename(old_path,new_path)
#             input_path = new_path

#     print('done')
# # pdf_folder = r"D:\tata_power_gonda\gonda_process\file_dir\scan_pdf"
# pdf_folder = r"C:\Users\Admin\Downloads\Indexing_Files\indexing_file_26"
# remove_space(pdf_folder)