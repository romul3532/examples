# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import numpy as np

'''
Данный файл производит парсинг термодинамических данных с сайта https://webbook.nist.gov/
входные данные : 
                1) название элемента или вещества ил его CAS-номер
                2) тип фазы (конденсированная , жидкая , газовая)
                3) тип данных (теплоемкость Ср, Энтальпия - dH, Энтропия - dS или молярная масса)
выходные данные : словарь вида {'Cp': , 'dH': , 'dS': , 'M': []}
'''

'''
### для вывода результатов работы кода прочитайте строки 391-...
'''

def get_data_from_NIST(substance,type_search,phase):
    def check_connectivity(reference):
        try:
            urllib.request.urlopen(reference, timeout=1)
            status_connect=1
        except urllib.request.URLError:
            status_connect=0
        return status_connect

    def construct_link_on_substance(substance):
        index_in_name=substance.find(' ')
        index_in_CAS=substance.find('-')
        if index_in_name!=-1:
            link_name=str(substance[0:index_in_name]+str('+')+substance[index_in_name+1:len(substance)])
            link_one='https://webbook.nist.gov/cgi/cbook.cgi?Name='
            link_two='&Units=SI'
            link=link_one+link_name+link_two
        elif index_in_CAS!=-1:
            link_name=str(substance)
            main_link=str('https://webbook.nist.gov/cgi/cbook.cgi?ID=')
            end_link=str('&Units=SI')
            link=main_link+link_name+end_link
        else:
            i_substance=0
            def find_nuber_in_substance(element_in_substance):
                list_numbers=['0','1','2','3','4','5','6','7','8','9']
                i_numbers=0
                exist_number_in_substance=0
                while i_numbers<=(len(list_numbers)-1):
                    if list_numbers[i_numbers]==element_in_substance:
                        exist_number_in_substance=1
                        i_numbers=len(list_numbers)
                    else:
                        c=np.nan
                        exist_number_in_substance==0
                    i_numbers+=1
                return exist_number_in_substance
        
            while i_substance<=(len(substance)-1):
                element_in_substance=substance[i_substance]
                exist_number_in_substance=find_nuber_in_substance(element_in_substance)
                if exist_number_in_substance==0:
                    link_one='https://webbook.nist.gov/cgi/cbook.cgi?Name='
                    link_two='&Units=SI'
                    link_name=str(substance)
                    link=link_one+link_name+link_two
                else:
                    link_one='https://webbook.nist.gov/cgi/cbook.cgi?Formula='
                    link_two='&NoIon=on&Units=SI'
                    link=link_one+str(substance)+link_two
                    i_substance=len(substance)
                i_substance+=1
        return link
    
    def check_link(link):
        r=urllib.request.urlopen(link)
        soup=BeautifulSoup(r,"html.parser")
        search_results=soup.find_all('h1')
        search_result_string=str(search_results[1])
        if search_result_string[0:13]==str('<h1 id="Top">'):
            link=link
            status_find=1
        elif search_result_string[0:23]==str('<h1>Search Results</h1>'):
            link_in_search_results=list(soup.find('ol'))
            first_link_in_search_results=str(link_in_search_results[1])
            start_link=first_link_in_search_results.find('<li><a href="')
            end_link=first_link_in_search_results.find('">')
            link=str('https://webbook.nist.gov')+first_link_in_search_results[start_link+13:end_link]+str('/')
            status_find=1
        elif search_result_string[0:23]==str('<h1>Name Not Found</h1>'):
            link=[]
            status_find=0
        return status_find,link
    
    def NIST_parser(link,type_search,phase):
        r=urllib.request.urlopen(link)
        soup=BeautifulSoup(r,"html.parser")
        a_href=[]
        for a in soup.find_all(href=True):
            if a.text:
                a_href.append(a['href'])
        i_link=0
        need_link=[]
        while i_link<=(len(a_href)-1):
            link_new=str(a_href[i_link])
            if phase=='g' or phase=='gas':
                if len(link_new)>=12 or len(link_new)>=16:
                    if link_new[len(link_new)-12:len(link_new)]=='Thermo-Phase':
                        need_link.append(link_new)
                    elif link_new[len(link_new)-16:len(link_new)]=='Thermo-Condensed':
                        need_link.append(link_new)
                    elif link_new[len(link_new)-10:len(link_new)]=='Thermo-Gas':
                        need_link.append(link_new)
                else:
                    need_link=need_link+[]
            elif phase=='solid' or phase=='sc' or phase=='condensed' or phase=='liquid' or phase=='sl':
                if len(link_new)>=12 or len(link_new)>=16:
                    if link_new[len(link_new)-16:len(link_new)]=='Thermo-Condensed':
                        need_link.append(link_new)
                    else:
                        need_link=need_link+[]
                else:
                    need_link=need_link+[]
            i_link+=1

        def convert_html_table_to_list(html_table,type_data):
            list_table=[]
            table_rows=html_table.find_all('tr')
            table_rows=list(table_rows)
            aria_label=str(html_table['aria-label'])
            if aria_label==str('Constant pressure heat capacity of solid'):
                for tr in table_rows:
                    td=tr.find_all('td')
                    if td:
                        row=[i.text for i in td]
                        row_zero=row[0]
                        list_table=[row_zero]
            else:
                for tr in table_rows:
                    td=tr.find_all('td')
                    if td:
                        row=[i.text for i in td]
                        row_zero=row[0]
                        if row_zero[0:9]!='Data last':
                            list_table.append(row)
                        else:
                            tr=len(table_rows)
                if type_data==1:
                    list_table=list_table
                else:
                    list_table=list_table[:-1]
            return list_table

        def convert_list_Cp_to_list_float(Cp):
                if len(Cp)==1:
                    list_Cp=np.float32(Cp[0])
                else:
                    def convert_range_Cp_to_list(value):
                        list_Cp=[]
                        index_only_dash=value.find(' - ')
                        value_one=np.float32(value[0:index_only_dash-1])
                        value_two=np.float32(value[index_only_dash+2:len(value)-1])
                        list_Cp=list_Cp+[value_one,value_two]
                        return list_Cp
                    
                    def convert_value_string_to_value(value):
                        ind1=value.find('×10-')
                        ind2=value.find('×10+')
                        if ind1!=-1 or ind2==-1:
                            value_float=np.float32(value[0:ind1])*10**(np.float32(value[ind1+3:len(value)]))
                        elif ind1==-1 or ind2!=-1:
                            value_float=np.float32(value[0:ind2])*10**(np.float32(value[ind2+3:len(value)]))
                        elif ind1==-1 or ind2==-1:
                            value_float=np.float32(value)
                        return value_float

                    def control_format_Cp(value):
                        index_only_dash=value.find(' - ')
                        index_degree_minus=value.find('×10-')
                        index_degree_plus=value.find('×10+')
                        if index_only_dash!=-1 and index_degree_minus==-1 and index_degree_plus==-1:
                            Cp_i_float=convert_range_Cp_to_list(value)
                        elif index_only_dash==-1 and index_degree_minus!=-1 and index_degree_plus==-1:
                            Cp_i_new=convert_value_string_to_value(value)
                            Cp_i_float=[Cp_i_new]
                        elif index_only_dash==-1 and index_degree_minus==-1 and index_degree_plus!=-1:
                            Cp_i_new=convert_value_string_to_value(value)
                            Cp_i_float=[Cp_i_new]
                        else:
                            Cp_i_float=[np.float32(value)]
                        return Cp_i_float

                    def get_end_Cp(Cp):
                        Cp_end=Cp[len(Cp)-1]
                        Cp_end=Cp_end[0]
                        if Cp_end[0:6]=='Chase,':
                            i_end=len(Cp)-2
                        else:
                            i_end=len(Cp)-1
                        return i_end
                    
                    i_end=get_end_Cp(Cp)
                    j=0
                    list_Cp=[]
                    while j<=i_end:
                        Cp_i=Cp[j]
                        if len(Cp_i)==1:
                            Cp_i=control_format_Cp(Cp_i[0])
                            list_Cp=list_Cp+Cp_i
                        else:
                            ii=0
                            while ii<(len(Cp_i)):
                                Cp_i_new=control_format_Cp(Cp_i[ii])
                                list_Cp=list_Cp+Cp_i_new
                                ii+=1
                        j+=1
                return list_Cp

        def convert_list_delta_H_S_to_value(list_delta_H_S,phase):
            i_table=0
            delta_H=[]
            S=[]
            while i_table<=(len(list_delta_H_S)-1):
                data=list_delta_H_S[i_table]
                if len(data)!=0:
                    type_var=data[0]
                    if phase=='s' or phase=='solid':
                        if type_var=='ΔfH°solid':
                            if len(data)==0: ### delta_H
                                delta_H=delta_H+[np.float32(0)] ### delta_H.append(data[1]) ### 
                            else:
                                delta_H.append(data[1]) ### delta_H=delta_H+[]
                        elif type_var[0:7]=='S°solid':
                            S.append(data[1])
                    else:
                        if type_var=='ΔfH°gas':
                            if len(data)==0: ### delta_H
                                delta_H=delta_H+[np.float32(0)]
                            else:
                                delta_H.append(data[1])
                        elif type_var[0:2]=='S°' or type_var[0:5]=='S°gas':
                            S.append(data[1])
                i_table+=1

            def convert_delta_H_and_S_to_float(var):
                index_plus=var.find('±')
                index_point=var.find('.')
                if index_plus==-1:
                    if len(var)-index_point==1:
                        value=np.int32(var[0:index_point])
                    else:
                        value=np.float32(var[0:index_point+2])
                else:
                    value=np.float32(var[0:index_plus-1])
                return value
            
            if len(delta_H)!=0:
                delta_H=delta_H[0]
                delta_H=convert_delta_H_and_S_to_float(delta_H)
                delta_H=np.round(delta_H,1)
            else:
                delta_H=[]
            if len(S)!=0:
                S=S[0]
                S=convert_delta_H_and_S_to_float(S)
                S=np.round(S,1)
            else:
                S=None
            return delta_H,S

        def get_molar_massa(link):
            with urllib.request.urlopen(link) as response:
                html=response.read()
            soup=BeautifulSoup(html, 'html.parser')
            li_data=soup.find_all('li')
            i_li=0
            while i_li<=(len(li_data)-1):
                data=str(li_data[i_li])
                m=data.find('Molecular weight')
                if m!=-1:
                    string_end=data.find('</a>:</strong> ')
                    molar_massa=np.float32(data[string_end+15:len(data)-5])
                else:
                    c=np.nan
                i_li+=1
            return molar_massa
        
        data_NIST=dict({})
        data_NIST['Cp']=[]
        data_NIST['dH']=[]
        data_NIST['dS']=[]
        data_NIST['M']=[]

        if len(need_link)!=0:
            linka=str('https://webbook.nist.gov/')+need_link[0]+str('/')
            ra=urllib.request.urlopen(linka)
            soupa=BeautifulSoup(ra,"html.parser")
            if type_search=='Cp':
                if phase=='gas' or phase=='g':
                    if len(list(soupa.find_all('table', { 'class' :"data",'aria-label':"Constant pressure heat capacity of gas"})))!=0 and len(list(soupa.find_all('table', { 'class' :"data",'aria-label':"Gas Phase Heat Capacity (Shomate Equation)"})))==0:
                        Cp=soupa.find("table",{"class":"data",'aria-label':"Constant pressure heat capacity of gas"})
                        Cp_set_value=convert_html_table_to_list(Cp,2)
                        Cp_float=convert_list_Cp_to_list_float(Cp_set_value)
                        data_NIST['Cp']=Cp_float
                    elif len(list(soupa.find_all('table', { 'class' :"data",'aria-label':"Gas Phase Heat Capacity (Shomate Equation)"})))!=0 and len(list(soupa.find_all('table', { 'class' :"data",'aria-label':"Constant pressure heat capacity of gas"})))==0:
                        Cp=soupa.find("table",{"class":"data",'aria-label':"Gas Phase Heat Capacity (Shomate Equation)"})
                        Cp_set_value=convert_html_table_to_list(Cp,2)
                        Cp_float=convert_list_Cp_to_list_float(Cp_set_value)
                        data_NIST['Cp']=Cp_float
                    elif len(list(soupa.find_all('table', { 'class' :"data",'aria-label':"Constant pressure heat capacity of gas"})))!=0 and len(list(soupa.find_all('table', { 'class' :"data",'aria-label':"Gas Phase Heat Capacity (Shomate Equation)"})))!=0:
                        Cp=soupa.find("table",{"class":"data",'aria-label':"Gas Phase Heat Capacity (Shomate Equation)"})
                        Cp_set_value=convert_html_table_to_list(Cp,2)
                        Cp_float=convert_list_Cp_to_list_float(Cp_set_value)
                        data_NIST['Cp']=Cp_float
                elif phase=='solid' or phase=='condensed' or phase=='sc':
                    print('condensed')
                    print('')
                    if len(list(soupa.find_all('table', { 'class' :"data",'aria-label':"Solid Phase Heat Capacity (Shomate Equation)"})))!=0:
                        Cp=soupa.find("table",{"class":"data",'aria-label':"Solid Phase Heat Capacity (Shomate Equation)"})
                        Cp_set_value=convert_html_table_to_list(Cp,2)
                        Cp_float=convert_list_Cp_to_list_float(Cp_set_value)
                        data_NIST['Cp']=Cp_float
                        table_delta_H_S=soupa.find_all("table")[0]
                        table_delta_H_S=convert_html_table_to_list(table_delta_H_S,1)
                        delta_H,S=convert_list_delta_H_S_to_value(table_delta_H_S,phase)
                        if type(delta_H)==list and len(delta_H)==0:
                            delta_H=0
                        else:
                            delta_H=delta_H
                        data_NIST['dH']=delta_H
                        data_NIST['dS']=S
                elif phase=='solid' or phase=='liquid' or phase=='sl':
                    if len(list(soupa.find_all('table', { 'class' :"data",'aria-label':"Liquid Phase Heat Capacity (Shomate Equation)"})))!=0:
                        print('')
                        print('Liquid')
                        Cp=soupa.find("table",{"class":"data",'aria-label':"Liquid Phase Heat Capacity (Shomate Equation)"})
                        Cp_set_value=convert_html_table_to_list(Cp,2)
                        Cp_float=convert_list_Cp_to_list_float(Cp_set_value)
                        data_NIST['Cp']=Cp_float
                        table_delta_H_S=soupa.find_all("table")[0]
#                table_delta_H_S=list(table_delta_H_S)
                        table_delta_H_S=convert_html_table_to_list(table_delta_H_S,1)
                        delta_H,S=convert_list_delta_H_S_to_value(table_delta_H_S,phase)
                        if type(delta_H)==list and len(delta_H)==0:
                            delta_H=0
                        else:
                            delta_H=delta_H
                        data_NIST['dH']=delta_H
                        data_NIST['dS']=S
                else:
                    Cp_float=[]
                    data_NIST['Cp']=Cp_float
            elif type_search=='dH' or type_search=='dS':
                table_delta_H_S=soupa.find_all("table")[0]
#                table_delta_H_S=list(table_delta_H_S)
                table_delta_H_S=convert_html_table_to_list(table_delta_H_S,1)
                delta_H,S=convert_list_delta_H_S_to_value(table_delta_H_S,phase)
                data_NIST['dH']=delta_H
                data_NIST['dS']=S
            elif type_search=='M':
                molar_massa=get_molar_massa(link)
                data_NIST['M']=molar_massa
        else:
            data_NIST['M']=[]
            molar_massa=get_molar_massa(link)
            data_NIST['M']=molar_massa
        return data_NIST
    
    def control_function(substance,type_search,phase):
        reference='https://webbook.nist.gov/'
        status_connect=check_connectivity(reference)
        if status_connect==1:
            link=construct_link_on_substance(substance)
            status_find,link=check_link(link)
            if status_find==1:
                status_error=0
                data_NIST=NIST_parser(link,type_search,phase)
            else:
                data_NIST=dict({})
                status_error=1
        else:
            data_NIST=dict({})
            status_error=1
        return status_error,data_NIST
    status_error,data_NIST=control_function(substance,type_search,phase)
    # print('data_NIST')
    # print('')
    # print(data_NIST)
    return status_error,data_NIST


#### Варианты парсинга данных :
### для вывода результатов работы кода раскомментируйте один из вариантов
### 1) : для Железа :
# substance=str('Fe')
# type_search='Cp' #### парсинг полинома теплоемкости
### ссылка https://webbook.nist.gov/cgi/cbook.cgi?ID=C7439896&Units=SI&Mask=1#Thermo-Gas
### таблица Gas Phase Heat Capacity (Shomate Equation)
# phase='gas'
# #### 2) для кобальта :
# substance=str('Cobalt')
# type_search='Cp' #### парсинг полинома теплоемкости
# ### ссылка https://webbook.nist.gov/cgi/cbook.cgi?ID=C7440484&Units=SI&Mask=2#Thermo-Condensed
# ### таблица Solid Phase Heat Capacity (Shomate Equation)
# phase='condensed'


status_error,data_NIST=get_data_from_NIST(substance,type_search,phase)
print('')
print('data_NIST')
print('')
print(data_NIST)
