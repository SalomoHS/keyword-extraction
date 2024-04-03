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

model = genai.GenerativeModel(model_name="gemini-pro",generation_config={'temperature':0.2},safety_settings=safety_settings)


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

if 'stock_name_list' not in st.session_state:
    st.session_state['stock_name_list'] = []
if 'subject_list' not in st.session_state:
    st.session_state['subject_list'] = []
if 'commodity_list' not in st.session_state:
    st.session_state['commodity_list'] = []
if 'state' not in st.session_state:
    st.session_state['state'] = 0
if 'get_subject_progress' not in st.session_state:
    st.session_state['get_subject_progress'] = st.progress(0)
# if 'get_stock_progress' not in st.session_state:
#     st.session_state['get_stock_progress'] = st.progress(0)
sample_text = """jakarta bmw m850i xdrive coupe first edition merupakan mobil langka di indonesia karena hanya ada 1 unit. berikut potret mobil yang dimiliki anak haji isam itu.bmw m850i xdrive coupe first edition hanya diproduksi sebanyak 400 unit di dunia. foto bmwwm menyematkan velg ringan berukurang 20 inchi yang mengusung warna jet black. foto bmwdi bagian tengah kokpit ada tulisan khusus first edition 1 400 . foto bmwkursinya dibalut kulit trim merino dengan kombinasi warna ivory white night blue. foto bmwedisi khusus ini menggendong mesin v8 dengan teknologi bmw twinpower turbo. mesinnya bisa menyemburkan tenaga 530 daya kuda pada rentang 5500 6000 rpm. foto bmwindonesia rupanya kebagian jatah mobil langka bmw m850i xdrive coupe first edition. untuk diketahui mobil ini hanya diproduksi sebanyak 400 unit dalam jurun waktu april juni 2019. dalam catatan bmw indonesia menyebut hanya ada satu unit mobil ini yang dijual di tanah air."""
sample_text2= """wakil direktur utama pt bank mandiri persero tbk. bmri alexandra askandar mengungkapkan perseroan terus terbuka atas segala aksi korporasi termasuk untuk mengakuisisi bank digital.meski tak merinci lebih lanjut akan tetapi dia menyebut saat ini bank mandiri masih akan terus fokus dalam mengembangkan digitalisasi. tentu sangat terbuka atas semua corporate action tapi mungkin secara spesifik belum dapat saya share katanya dalam agenda cnbc economic outlook 2024 kamis .sejauh ini dia mengatakan dalam menghadapi pesatnya digitalisasi perbankan bank mandiri masih akan mengandalkan super app livin by mandiri. perkembangan super app perseroan itupun sangat signifikan terlihat dari sisi user registered saat kami launching pertama kali pengguna mobile banking bank mandiri di angka enam juta user lalu akhir tahun lalu menjadi 23 juta user registered livin ungkapnya.sebelumnya direktur teknologi informasi bank mandiri timothy utama mengatakan livin by mandiri pun sudah diposisikan di pasar sebagai bank digital dari bank mandiri. alhasil bank mandiri lebih memilih untuk fokus mengembangkan platform digitalnya itu. kami akan perkaya dengan fitur fitur untuk menjawab kebutuhan nasabah katanya. sementara itu livin by mandiri sendiri telah diunduh lebih dari 37 juta kali sejak diluncurkan pada oktober 2021. adapun sepanjang 2023 livin by mandiri mencatatkan 3 miliar transaksi.nilai transaksi livin by mandiri sepanjang 2023 telah menembus rp3.271 triliun naik 32 secara tahunan year on year yoy .bank mandiri juga memiliki platform digital untuk segmen wholesale bernama kopra by mandiri dan telah berhasil mengelola rp19.100 triliun transaksi. kami secara spesifik terus meningkatkan fungsi dan manfaat livin dan kopra by mandiri sebagai solusi yang dapat memenuhi segala macam kebutuhan nasabah baik secara finansial maupun non finansial ujar direktur utama bank mandiri darmawan i. sebagai informasi bank mandiri menjadi satu satunya bank dalam kategori kbmi iv alias bank jumbo yang tidak memiliki anak usaha di segmen bank digital.tercatat pt bank central asia tbk. bbca misalnya yang memiliki bca digital yang merupakan hasil transformasi dari pt bank royal indonesia. adapun bca mengakuisisi bank royal pada november 2019. lalu pt bank rakyat indonesia persero tbk. bbri yang menjadikan anak usahanya pt bank rakyat indonesia agroniaga tbk. menjadi bank digital dan berganti nama menjadi pt bank raya indonesia tbk. agro . terahir pt bank negara indonesia persero tbk. bbni telah mengakuisisi pt bank mayora dan mengubahnya menjadi bank digital bernama hibank."""

uploaded_file = st.file_uploader("Upload Excel file")

    
if uploaded_file is not None:
    # Read the CSV file
    df = pd.DataFrame()
    # try:
    df = pd.read_excel(uploaded_file)
    # except:
    #     df = pd.read_csv(uploaded_file)

    st.write('**File contents:**')
    st.write(df)
    
    while(1):
        try:
            for i,row in df.iloc[st.session_state['state']:].iterrows():
                st.session_state['get_subject_progress'].progress((st.session_state['state'] + 1) / len(df), text = f"{st.session_state['state']+1}/{len(df)}")
                text = row['cleaned']
                get_subjects = [f'input:\nBerita: {sample_text}\nSebutkan nama perusahaan apa saja yang tercantum di dalam berita !\nJika terdapat nama perusahaan "Mandiri", maka tambahkan kata "Bank" di awal !\nSertakan hasil hanya dengan 1 baris dengan tanda koma sebagai pemisah !',
                                'Output: BMW, BMW Indonesia',
                                f'input:\nBerita: {sample_text2}\nSebutkan nama perusahaan apa saja yang tercantum di dalam berita !\nJika terdapat nama perusahaan "Mandiri", maka tambahkan kata "Bank" di awal !\nSertakan hasil hanya dengan 1 baris dengan tanda koma sebagai pemisah !',
                                'Output: PT Bank Mandiri Persero Tbk, PT Bank Central Asia Tbk, PT Bank Rakyat Indonesia Persero Tbk, PT Bank Negara Indonesia Persero Tbk',
                                f'input:\nBerita: {text}\nSebutkan nama perusahaan apa saja yang tercantum di dalam berita !\nJika terdapat nama perusahaan "Mandiri", maka tambahkan kata "Bank" di awal !\nSertakan hasil hanya dengan 1 baris dengan tanda koma sebagai pemisah !',
                                'Output:'
                                # "Sebutkan nama perusahaan apa saja yang tercantum di dalam berita !",
                                # 'Jika terdapat nama perusahaan "Mandiri", maka tambahkan kata "Bank" di awal !',
                                # 'Sertakan hasil hanya dengan 1 baris dengan tanda koma sebagai pemisah !'
                                ]
                # get_subjects = [f'News: {text}',"Mention the name of the corporate company mentioned in the news !", 
                #                 'You can pick it more than one !',
                #                 'Please provide result using comma as the delimiter.']
                
                get_commodity_desc = [f'News: {text}',
                                      f'Define news based on this list: {labels}, and please provide result using comma as the delimiter !',
                                      'You can define maximum 3 !']
                subject = ''
                commodity = ''
                stock_name = ''
                try:
                    subject  = model.generate_content(get_subjects).text.strip()
                    commodity  = model.generate_content(get_commodity_desc).text.strip()
                    
                    # get_stock_name = ['Your task is to classify company name to existing stock name based on Indonesia stock exchange !', 
                                    #   f'Company name: {subject}.',
                                    #   'Please generate result only like <stock name1>, <stock name2>, <...>.',
                                    #   "If the company name not listed on Indonesia stock exchange, then don't write on the result."]
                    # stock_name = model.generate_content(get_stock_name).text.strip()
                except:
                    continue
                
                # st.session_state['stock_name_list'].append(stock_name)
                st.session_state['subject_list'].append(subject)
                st.session_state['commodity_list'].append(commodity)
                st.session_state['state']+=1

            if len(st.session_state['commodity_list']) == len(df):
                break
        except:
            continue

    # st.write(st.session_state['subject_list'])
    # st.write(st.session_state['commodity_list'])
    # df['abs_sum_en'] = st.session_state['summary_list'] 
    # df['stock_name'] = st.session_state['stock_name_list']
    df['SUBJECT'] = st.session_state['subject_list']
    df['COMMODITY_DESC'] = st.session_state['commodity_list']
    
    
    # df.fillna('-', inplace=True)
    # df['subject_name'] = [i.split(',') for i in df['subject_name']]
    # df['COMMODITY_DESC'] = [i.split(',') for i in df['COMMODITY_DESC']]
    # final_df = df.explode(['COMMODITY_DESC'])
    # final_df['COMMODITY_DESC'] = [i.strip() for i in final_df['COMMODITY_DESC']]
    # final_df['COMMODITY_DESC'] = final_df['COMMODITY_DESC'].apply(labelling)
    # final_df = final_df.explode(['subject_name']).reset_index(drop=True)
    # final_df = final_df.drop_duplicates()
    st.write(df)
    # final_df
    file_name = f"{datetime.now().strftime('%Y%m%d')}_news.csv"
    excel_file = df.to_csv().encode('utf-8')
    # with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    #     excel_file = final_df.to_excel(writer)
    
    st.download_button(
        label="Download data",
        data=excel_file,
        file_name=file_name
    )