import google.generativeai as genai
import streamlit as st
import pandas as pd
import os
from datetime import datetime

def labelling(label):
    if label == 'AUTOMOTIVE AND TRANSPORTATION':
        return 'OTOMOTIF DAN ALAT TRANSPORTASI'
    elif label == 'BUILDING MATERIALS & OTHER CONSTRUCTION IRON':
        return 'BAHAN BANGUNAN & BESI KONTRUKSI LAINNYA'
    elif label == 'PHARMACEUTICALS AND HEALTH EQUIPMENT':
        return 'FARMASI DAN ALAT KESEHATAN'
    elif label == 'CHEMICALS AND PLASTICS':
        return 'BAHAN KIMIA DAN PLASTIK'
    elif label == 'CONSUMER FINANCE':
        return 'PEMBIAYAAN KONSUMEN'
    elif label == 'TRANSPORTATION AND LOGISTICS':
        return 'TRANSPORTASI DAN LOGISTIK'
    elif label == 'TELECOMMUNICATIONS':
        return 'TELEKOMUNIKASI'
    elif label == 'PLANTATION AND AGRICULTURE':
        return 'PERKEBUNAN DAN PERTANIAN'
    elif label == 'VEGETABLE / ANIMAL OILS':
        return'MINYAK NABATI / HEWANI'
    elif label == 'FOOD AND BEVERAGE':
        return 'MAKANAN DAN MINUMAN'
    elif (label == 'CONSUMER NEEDS') or (label == 'EQUIPMENT AND HOUSEHOLD NEEDS (NEEDS OUTSIDE OF CLOTHING)'):
        return 'KEBUTUHAN KONSUMEN, PERLENGKAPAN DAN KEBUTUHAN RT (KEBUTUHAN DI LUAR SANDANG)'
    elif label == 'PACKAGING':
        return 'PACKAGING'
    elif (label == 'MACHINERY') or (label == 'HEAVY EQUIPMENT & OTHER INDUSTRIAL EQUIPMENT'):
        return 'PERMESINAN, ALAT BERAT & PERALATAN INDUSTRI LAINNYA'
    elif label == 'PROPERTY AND CONSTRUCTION':
        return 'PROPERTI DAN KONSTRUKSI'
    elif label == 'FINANCIAL SERVICES':
        return 'JASA KEUANGAN'
    elif label == 'WOOD PRODUCTS AND FORESTRY':
        return 'HASIL KAYU DAN KEHUTANAN'
    elif label == 'TEXTILES & TEXTILE PRODUCTS':
        return 'TEKSTIL & PRODUK TEKSTIL'
    elif label == 'BASIC METALS INDUSTRY & SIMILAR':
        return 'INDUSTRI LOGAM DASAR & SEJENISNYA'
    elif label == 'ENERGY GENERATION':
        return 'PEMBANGKIT ENERGI DAN TENAGA LISTRIK'
    elif label == 'ELECTRICITY':
        return 'PEMBANGKIT ENERGI DAN TENAGA LISTRIK'
    elif label == 'ELECTRONIC EQUIPMENT AND ELECTRICAL TOOLS':
        return 'PERALATAN ELEKTRONIK DAN ALAT-ALAT LISTRIK'
    elif label == 'COAL':
        return 'BATUBARA'
    elif label == 'OIL AND GAS MINING':
        return 'PERTAMBANGAN MIGAS'
    elif label == 'CIGARETTES AND TOBACCO':
        return 'ROKOK DAN TEMBAKAU'
    elif (label == 'DISTRIBUTION') or (label == 'RETAILERS AND DEPARTMENT STORES'):
        return 'DISTRIBUSI, RETAILER DAN TOSERBA'
    elif label == 'TOURISM':
        return 'PARIWISATA'
    elif label == 'TRANSPORT INFRASTRUCTURE FACILITIES':
        return 'INFRASTRUKTUR SARANA ANGKUTAN'
    elif label == 'STAPLE FOODS':
        return 'MAKANAN POKOK'
    elif (label == 'LIVESTOCK') or (label == 'FISHERIES AND PRODUCTION FACILITIES'):
        return 'PETERNAKAN, PERIKANAN DAN SARANA PRODUKSI'
    elif label == 'INFORMATION TECHNOLOGY':
        return 'TEKNOLOGI INFORMASI'
    elif label == 'NON-OIL AND GAS MINING':
        return 'PERTAMBANGAN NON MIGAS'
    elif label == 'OFFICE EQUIPMENT AND STATIONERY':
        return 'PERALATAN KANTOR DAN STATIONERY'
    elif label == 'RESTAURANTS':
        return 'RESTORAN'
    elif label == 'PUBLIC FACILITIES':
        return 'PRASARANA UMUM'
    elif label == 'INFORMATION MEDIA':
        return 'MEDIA INFORMASI'
    elif label == 'BUSINESS SERVICES':
        return 'JASA USAHA'
    
genai.configure(api_key='AIzaSyBM3MFzxbo_6ptt_o3ss8YchNtjgI7DSRQ')
st.write("Hello world")

safety_settings = [{'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
                    'threshold': 'BLOCK_NONE'},
                   {
                    'category': 'HARM_CATEGORY_HATE_SPEECH',
                    'threshold': 'BLOCK_NONE'
                    },
                    {
                    'category': 'HARM_CATEGORY_HARASSMENT',
                    'threshold': 'BLOCK_NONE'
                    },
                    {
                    'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
                    'threshold': 'BLOCK_NONE'
                    }
                ]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",generation_config={'temperature':0.1},safety_settings=safety_settings)


labels = [
    'AUTOMOTIVE AND TRANSPORTATION',
    'BUILDING MATERIALS & OTHER CONSTRUCTION IRON',
    'PHARMACEUTICALS AND HEALTH EQUIPMENT', 'CHEMICALS AND PLASTICS',
    'CONSUMER FINANCE', 'TRANSPORTATION AND LOGISTICS',
    'TELECOMMUNICATIONS', 'PLANTATION AND AGRICULTURE',
    'VEGETABLE / ANIMAL OILS', 'FOOD AND BEVERAGE',
    'CONSUMER NEEDS, EQUIPMENT AND HOUSEHOLD NEEDS (NEEDS OUTSIDE OF CLOTHING)',
    'PACKAGING', 'MACHINERY, HEAVY EQUIPMENT & OTHER INDUSTRIAL EQUIPMENT',
    'PROPERTY AND CONSTRUCTION', 'FINANCIAL SERVICES',
    'WOOD PRODUCTS AND FORESTRY', 'TEXTILES & TEXTILE PRODUCTS',
    'BASIC METALS INDUSTRY & SIMILAR',
    'ENERGY GENERATION', 'ELECTRICITY',
    'ELECTRONIC EQUIPMENT AND ELECTRICAL TOOLS', 'COAL',
    'OIL AND GAS MINING', 'CIGARETTES AND TOBACCO',
    'DISTRIBUTION, RETAILERS AND DEPARTMENT STORES', 'TOURISM',
    'TRANSPORT INFRASTRUCTURE FACILITIES', 'STAPLE FOODS',
    'LIVESTOCK, FISHERIES AND PRODUCTION FACILITIES',
    'INFORMATION TECHNOLOGY', 'NON-OIL AND GAS MINING',
    'OFFICE EQUIPMENT AND STATIONERY', 'RESTAURANTS', 'PUBLIC FACILITIES',
    'INFORMATION MEDIA', 'BUSINESS SERVICES'
]

if 'subject_list' not in st.session_state:
    st.session_state['subject_list'] = []
if 'commodity_list' not in st.session_state:
    st.session_state['commodity_list'] = []
if 'state' not in st.session_state:
    st.session_state['state'] = 0
if 'progress' not in st.session_state:
    st.session_state['progress'] = st.progress(0)
# subject_list = []
# commodity_list = []
# state = 0
uploaded_file = st.file_uploader("Upload CSV/Excel file", type=['csv','xlsx'])
#st.write('The current movie title is', title)
    
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    # Display the contents of the CSV file
    st.write('**CSV file contents:**')
    st.write(df)
    # progress_bar = 
    
    while(1):
        try:
            for i,row in df.iloc[st.session_state['state']:].iterrows():
                st.session_state['progress'].progress((st.session_state['state'] + 1) / len(df), text = f"{st.session_state['state']+1}/{len(df)}")
                text = row['abs_sum_en']
                get_subjects = [f'News: {text}',"Mention the name of the corporate company mentioned in the news ?", 'You can pick it more than one !','Please provide result using comma as the delimiter.']
                get_commodity_desc = [f'News: {text}',f'Define news based on this list: {labels}, and please provide result using comma as the delimiter !','You can define maximum 3 !']
                
                try:
                    subject  = model.generate_content(get_subjects).text
                    commodity  = model.generate_content(get_commodity_desc).text
                except:
                    continue
                st.session_state['subject_list'].append(subject)
                st.session_state['commodity_list'].append(commodity)
                st.session_state['state']+=1

            if len(st.session_state['commodity_list']) == len(df):
                break
        except:
            continue

    st.write(st.session_state['subject_list'])
    st.write(st.session_state['commodity_list'])
    df['CUST_NAME'] = st.session_state['subject_list']
    df['COMMODITY_DESC'] = st.session_state['commodity_list']
    
    df.fillna('-', inplace=True)
    df['CUST_NAME'] = [i.split(',') for i in df['CUST_NAME']]
    df['COMMODITY_DESC'] = [i.split(',') for i in df['COMMODITY_DESC']]
    final_df = df.explode(['COMMODITY_DESC'])
    final_df['COMMODITY_DESC'] = [i.strip() for i in final_df['COMMODITY_DESC']]
    final_df['COMMODITY_DESC'] = final_df['COMMODITY_DESC'].apply(labelling)
    final_df = final_df.explode(['CUST_NAME']).reset_index(drop=True)
    st.write(final_df)
    
    file_name = f"{datetime.now().strftime('%Y%m%d')}_news.csv"
    excel_file = final_df.to_excel().encode('utf-8')
    
    st.download_button(
        label="Download data",
        data=excel_file,
        file_name=file_name,
        mime='text/csv',
    )
    
    # try:
    #     save_path = os.path.join(os.getcwd(),'C:\\Users\\isalo\\Documents',file_name)
    #     final_df.to_csv(save_path, index=False)
    # except:
    #     save_path = os.path.join(os.getcwd(),'/\\kp1eucapp01\MagangCSA\Data\Web Scraping\Gnews\keyword extraction',file_name)
    #     final_df.to_csv(save_path, index=False)
        