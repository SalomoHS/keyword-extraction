import google.generativeai as genai
import streamlit as st
import pandas as pd
import os
from datetime import datetime

genai.configure(api_key='AIzaSyC-eK9vZWB-DmTiIUcKlgnUUJ0RAhGTp8Q')
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

if 'summary_list' not in st.session_state:
    st.session_state['summary_list'] = []
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
sample_text3 = """pt pertamina geothermal energy tbk pgeo mengumumkan kinerja perseroan tahun buku 2023 yang berakhir pada 31 desember 2023.pada periode tersebut pertamina geothermal energy berhasil membukukan pertumbuhan positif baik dari sisi pendapatan maupun laba. melansir laporan keuangan perseroan dalam keterbukaan informasi bursa efek indonesia bei jumat perseroan membukukan pendapatan usd 406 juta atau sekitar rp 6 triliun kurs rp 15708 per usd .pendapatan ini naik 5 persen dibandingkan pendapatan pada 2022 yang tercatat sebesar usd 386 juta. bersamaan dengan kenaikan pendapatan beban pokok pendapatan dan beban langsung lainnya ikut naik menjadi usd 179 juta dari usd 173 juta pada 2022. meski begitu laba bruto perseroan pada 2023 masih tercatat lebih tinggi yakni usd 227 juta dibanding tahun sebelumnya usd 213 juta.sepanjang 2023 perseroan membukukan beban umum dan administrasi sebesar usd 6 juta pendapatan keuangan usd 22 juta dan pendapatan lain lain usd 21 juta. pada periode ini perseroan juga membukukan beban keuangan usd 24 juta.setelah dikurangi beban pajak penghasilan perseroan membukukan laba tahun berjalan yang dapat diatribusikan kepada pemilik entitas induk sebesar usd 164 juta atau sekitar rp 3 triliun. laba ini naik 28 persen dibandingkan laba 2022 yang tercatat sebesar usd 127 juta.dari sisi aset perseroan sampai dengan 31 desember 2023 naik menjadi usd 3 miliar dari usd 2 miliar pada akhir 2022. liabilitas pada 2023 turun menjadi usd 993 juta dari usd 1 miliar pada 2022. sementara ekuitas pada 2023 naik menjadi usd 2 miliar dari usd 1 miliar pada 2022.pada penutupan perdagangan sesi pertama jumat harga saham pgeo naik 1 persen ke posisi rp 1220 per saham. saham pgeo dibuka stagnan rp 1210 per saham. saham pgeo berada di level tertinggi rp 1230 dan terendah rp 1205 per saham. total frekuensi perdagangan 1650 kali dengan volume perdagangan 957968 saham. nilai transaksi rp 111 miliar. sebelumnya diberitakan pt pertamina geothermal energy tbk pgeo atau disebut pge mengumumkan peluncuran program management and employee stock option program mesop tahap i.perkiraan jumlah hak opsi yang akan dilaksanakan dalam program mesop tahap i ini mencapai 252159200 saham dengan nilai nominal rp 648 per saham. direktur utama pt pertamina geothermal energy tbk julfi hadi mengatakan untuk menjadikan pge sebagai world class pany diperlukan usaha bersama dari semua pihak termasuk di dalamnya karyawan.setelah ipo pada 2023 pertamina geothermal energy telah mengalokasikan 2 dari modal ditempatkan dan disetor penuh setelah penawaran umum perdana saham atau sebanyak banyaknya 630398000 saham untuk program opsi pembelian saham kepada manajemen dan karyawan perseroan. program mesop menjadi salah satu bentuk komitmen perseroan untuk meningkatkan rasa memiliki dari karyawan terhadap perusahaan sehingga bersama kita dapat mencapai kinerja perseroan terbaik secara berkelanjutan kata julfi seperti dikutip dari keterangan resmi ditulis rabu .julfi menjelaskan program mesop tahap i ini sebenarnya sudah sejalan dengan kebijakan perseroan. selain itu program ini juga sudah tercantum pada peraturan ojk atau otoritas jasa keuangan no.3 thn. 2014 di mana disebutkan jika program kepemilikan saham bagi karyawan merupakan usaha agar pegawai atau karyawan dapat mempunyai aset dari perusahaan. harapan kami program mesop tahap i ini akan membuat pge menjadi semakin terdepan dalam mengelola potensi energi terbarukan di indonesia tutur dia. sementara itu direktur keuangan pt pertamina geothermal energy tbk yurizki rio berharap hadirnya program ini akan dapat meningkatkan loyalitas dan kinerja karyawan dan manajemen serta memperkuat struktur permodalan. kami harap program mesop tahap i ini dapat meningkatkan motivasi dan komitmen karyawan agar mampu memberikan performa yang baik dan berdampak bagus pada operasional serta perkembangan perseroan kata yurizki.sejauh ini inisiatif perseroan dalam memperkuat permodalan didapat dari penawaran saham perdana pada rp 875 dengan nilai terkumpul sebesar rp 9056250000.000. selain itu pge menerbitkan obligasi berwawasan hijau green bond di pasar global. green bond pge berhasil membukukan usd 400 juta pada 27 april 2023. green bond pge tersebut menjadi bond premium di secondary market yang tercatat pada singapore exchange securities trading limited sgx st atau bursa efek di singapura.sebelumnya diberitakan pt pertamina geothermal energy tbk pgeo menandatangani non disclosure agreement nda dengan geothermal pany gdc untuk mempelajari lebih lanjut kemungkinan kerja sama dalam pengembangan potensi panas bumi di kenya dan indonesia.hal tersebut dilakukan dalam rangka menindaklanjuti memorandum of understanding mou g2g yang sudah disepakati oleh indonesia dan kenya pada kunjungan ke kenya agustus 2023.direktur utama pertamina geothermal energy julfi hadi menuturkan kerja sama dengan kenya ini sebagai langkah awal pge untuk menjadi world class green pany. saat berkunjung ke kenya pge menandatangani kesepakatan dengan africa geothermal international limited agil untuk mengembangkan konsesi longonot di kenya yang memiliki potensi pengembangan sampai dengan 500 mw di mana 140 mw siap untuk di eksploitasi ujar dia dalam keterbukaan informasi dikutip jumat .terkait progres kerja sama dengan agil julfi mengatakan saat ini kedua belah pihak sedang melakukan sharing data hingga tiga bulan ke depan. tentunya banyak hal bernilai positif bagi kedua negara dalam mengembangkan energi panas bumi kata dia."""

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
                get_summarized = ['Summarize given news into 1 paragraph and 3 sentences !',f'News: {text}']
                get_subjects = [f'input:\nBerita: {sample_text}\nSebutkan nama perusahaan apa saja yang tercantum di dalam berita !\nJika terdapat nama perusahaan "Mandiri", maka tambahkan kata "Bank" di awal !\nSertakan hasil hanya dengan 1 baris dengan tanda koma sebagai pemisah !',
                                'Output: BMW, BMW Indonesia',
                                f'input:\nBerita: {sample_text2}\nSebutkan nama perusahaan apa saja yang tercantum di dalam berita !\nJika terdapat nama perusahaan "Mandiri", maka tambahkan kata "Bank" di awal !\nSertakan hasil hanya dengan 1 baris dengan tanda koma sebagai pemisah !',
                                'Output: PT Bank Mandiri Persero Tbk, PT Bank Central Asia Tbk, PT Bank Rakyat Indonesia Persero Tbk, PT Bank Negara Indonesia Persero Tbk',
                                f'input:\nBerita: {text}\nSebutkan nama perusahaan apa saja yang tercantum di dalam berita !\nJika terdapat nama perusahaan "Mandiri", maka tambahkan kata "Bank" di awal !\nSertakan hasil hanya dengan 1 baris dengan tanda koma sebagai pemisah !',
                                'Output:',
                                # f'input:\nBerita: {text}\nSebutkan nama perusahaan apa saja yang tercantum di dalam berita !\nJika terdapat nama perusahaan "Mandiri", maka tambahkan kata "Bank" di awal !\nSertakan hasil hanya dengan 1 baris dengan tanda koma sebagai pemisah !',
                                # 'Output:',
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
                    summarize =  model.generate_content(get_summarized).text.strip()
                    # get_stock_name = ['Your task is to classify company name to existing stock name based on Indonesia stock exchange !', 
                                    #   f'Company name: {subject}.',
                                    #   'Please generate result only like <stock name1>, <stock name2>, <...>.',
                                    #   "If the company name not listed on Indonesia stock exchange, then don't write on the result."]
                    # stock_name = model.generate_content(get_stock_name).text.strip()
                except:
                    continue
                
                st.session_state['summary_list'].append(summarize)
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
    df['abs_sum_en'] = st.session_state['summary_list']
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

    final_df = df.copy()
    final_df.drop('COMMODITY_DESC',axis=1,inplace=True)
    final_df = final_df.explode('SUBJECT')
    final_df['SUBJECT'] = [i.strip() for i in final_df['SUBJECT']]
    # df = 
    final_df.drop_duplicates(inplace=True)
    final_df['COMMODITY_DESC'] = df['COMMODITY_DESC']
    final_df = final_df.explode(['COMMODITY_DESC'])
    final_df.drop_duplicates(inplace=True)

    st.write(df)
    # final_df
    file_name = f"{datetime.now().strftime('%Y%m%d')}_news.csv"
    excel_file = df.to_csv(index=False).encode('utf-8')
    # with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    #     excel_file = final_df.to_excel(writer)
    
    st.download_button(
        label="Download data",
        data=excel_file,
        file_name=file_name
    )
