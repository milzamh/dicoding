import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_total_rentals_by_date(df, selected_date):
    filtered_data = df[df['dteday'] == pd.to_datetime(selected_date)]
    total_rentals = filtered_data['cnt'].sum()
    return total_rentals, filtered_data

def plot_hourly_rentals(filtered_data, selected_date):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=filtered_data, x='hr', y='cnt', ax=ax, palette='viridis')
    ax.set_title(f'Penyewaan Sepeda Berdasarkan Jam pada {selected_date.strftime("%Y-%m-%d")}')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Sepeda yang Disewa')
    return fig

def plot_total_year(filtered_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=filtered_data, x='mnth', y='cnt', ax=ax, palette='viridis')
    ax.set_title(f'Penyewaan Sepeda Tahun 2011 dan 2012')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Sepeda yang Disewa')
    return fig

def get_total_rentals_by_quarter(df, year, quarter):
    if quarter == 1:
        return df[(df['yr'] == year) & (df['mnth'].between(1, 3))]['cnt'].sum()
    elif quarter == 2:
        return df[(df['yr'] == year) & (df['mnth'].between(4, 6))]['cnt'].sum()
    elif quarter == 3:
        return df[(df['yr'] == year) & (df['mnth'].between(7, 9))]['cnt'].sum()
    elif quarter == 4:
        return df[(df['yr'] == year) & (df['mnth'].between(10, 12))]['cnt'].sum()
    
def plot_monthly_user_type_trend(df):
    monthly_rents = df.groupby(by='mnth')[['casual', 'registered']].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_rents.plot(kind='line', marker='o', ax=ax)
    ax.set_title('Tren Penyewaan Sepeda oleh Pengguna Kasual dan Terdaftar')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Sepeda yang Disewa')
    plt.xticks(rotation=0)
    plt.legend(title='Tipe Pengguna')
    plt.grid(axis='y')
    return fig

def plot_rentals_by_temperature(df):
    grouped_temp = df.groupby('actual_temp')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(grouped_temp['cnt'], labels=grouped_temp['actual_temp'], autopct='%1.1f%%', explode=(0, 0.1, 0.2))
    ax.set_title('Distribusi Penyewaan Sepeda Berdasarkan Kategori Suhu')
    return fig

def plot_weather_condition(df):
    grouped_weather = df.groupby('weathersit')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=grouped_weather, x='weathersit', y='cnt', ax=ax)
    ax.set_title('Total Penyewaan Sepeda per Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Total Penyewaan (Dalam Juta)')
    return fig

def plot_workingday_holiday_rentals(df):
    grouped_workingday = df.groupby('workingday')['cnt'].sum().reset_index()
    grouped_workingday['day_category'] = grouped_workingday['workingday'].apply(lambda x: 'Hari Kerja' if x == 1 else 'Hari Libur')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=grouped_workingday, x='day_category', y='cnt', ax=ax)
    ax.set_title('Total Penyewaan Sepeda: Hari Kerja vs Hari Libur')
    ax.set_xlabel('Kategori Hari')
    ax.set_ylabel('Total Penyewaan')
    return fig

def plot_workday_temp_rentals(df):
    workdays = df[df['workingday'] == 1]
    
    grouped = workdays.groupby(['actual_temp', 'weathersit'])['cnt'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bar = sns.barplot(data=grouped, x='actual_temp', y='cnt', hue='weathersit', palette='viridis', ax=ax)
    
    bar.bar_label(bar.containers[0])
    
    ax.set_title('Hubungan Suhu dan Penyewaan Sepeda pada Hari Kerja')
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Jumlah Penyewaan (Dalam Juta)')
    ax.legend(title='Kondisi Cuaca')

def main():
    st.title("Dashboard Analisis Bike Sharing Dataset")


    hour_df = pd.read_csv('hour.csv')
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday']) 
    
    selected_date = st.date_input("Pilih Tanggal:", value=pd.to_datetime("2011-01-01"), 
                                  min_value=hour_df['dteday'].min(), max_value=hour_df['dteday'].max())
    
    hour_df['actual_temp'] = hour_df['temp'] * 41 
    hour_df['actual_temp'] = hour_df['actual_temp'].apply(lambda x: 'cold' if x < 15 else 'mild' if 15 <= x < 30 else 'hot')

    hour_df['weathersit'] = hour_df['weathersit'].replace({1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'})
    hour_df['weathersit'].value_counts()

    total_rentals, filtered_data = get_total_rentals_by_date(hour_df, selected_date)
    st.write(f"**Total penyewaan sepeda pada {selected_date.strftime('%Y-%m-%d')}: {total_rentals} sepeda.**")

    if not filtered_data.empty:
        fig = plot_hourly_rentals(filtered_data, selected_date)
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data penyewaan sepeda pada tanggal ini.")
    
    st.subheader("Jumlah Penyewaan Sepeda per Kuartal")
    st.markdown("Silahkan pilih kuartal untuk melihat total penyewaan sepeda")

    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    
    if col_q1.button("Kuartal 1"):
        total_q1_2011 = get_total_rentals_by_quarter(hour_df, 0, 1)
        total_q1_2012 = get_total_rentals_by_quarter(hour_df, 1, 1)
        st.metric("Total Penyewaan pada Kuartal 1 (2011)", f"{total_q1_2011} sepeda")
        st.metric("Total Penyewaan pada Kuartal 1 (2012)", f"{total_q1_2012} sepeda")

    if col_q2.button("Kuartal 2"):
        total_q2_2011 = get_total_rentals_by_quarter(hour_df, 0, 2)
        total_q2_2012 = get_total_rentals_by_quarter(hour_df, 1, 2)
        st.metric("Total Penyewaan pada Kuartal 2 (2011)", f"{total_q2_2011} sepeda")
        st.metric("Total Penyewaan pada Kuartal 2 (2012)", f"{total_q2_2012} sepeda")

    if col_q3.button("Kuartal 3"):
        total_q3_2011 = get_total_rentals_by_quarter(hour_df, 0, 3)
        total_q3_2012 = get_total_rentals_by_quarter(hour_df, 1, 3)
        st.metric("Total Penyewaan pada Kuartal 3 (2011)", f"{total_q3_2011} sepeda")
        st.metric("Total Penyewaan pada Kuartal 3 (2012)", f"{total_q3_2012} sepeda")

    if col_q4.button("Kuartal 4"):
        total_q4_2011 = get_total_rentals_by_quarter(hour_df, 0, 4)
        total_q4_2012 = get_total_rentals_by_quarter(hour_df, 1, 4)
        st.metric("Total Penyewaan pada Kuartal 4 (2011)", f"{total_q4_2011} sepeda")
        st.metric("Total Penyewaan pada Kuartal 4 (2012)", f"{total_q4_2012} sepeda")

    st.subheader("Tren Penyewaan Sepeda ")
    st.markdown("Tren penyewaan sepeda per bulan untuk tahun 2011 dan 2012.")
    
    fig = plot_total_year(hour_df)
    st.pyplot(fig)
    
    st.markdown("Grafik tren penyewaan sepeda diatas menunjukkan kenaikan dimulai dari bulan Januari hingga Juni. Namun, terdapat perlambatan hingga penurunan tren penyewaan dari bulan Juli hingga Desember .")
    
    st.subheader("Tren Penyewaan Sepeda antara Pengguna Kasual dan Terdaftar")

    fig_user_trend = plot_monthly_user_type_trend(hour_df)
    st.pyplot(fig_user_trend)
    
    st.markdown("Grafik diatas menunjukkan bahwa pengguna terdaftar lebih banyak menyewa sepeda dibandingkan pengguna kasual. Namun, tren penyewaan sepeda oleh pengguna kasual mengalami peningkatan yang lebih signifikan dibandingkan pengguna terdaftar.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Suhu favorit untuk penyewaan sepeda")
        fig_temp = plot_rentals_by_temperature(hour_df)
        st.pyplot(fig_temp)
    
    with col2:
        st.subheader("Total Penyewaan Sepeda per Kondisi Cuaca")
        fig_weather = plot_weather_condition(hour_df)
        st.pyplot(fig_weather)
    
    st.markdown("Visualisasi di atas merupakan distribusi penyewaan sepeda berdasarkan kategori suhu dan kondisi cuaca. Dapat dilihat bahwa suhu 'mild' dan kondisi cuaca 'Clear' merupakan faktor yang paling berpengaruh terhadap jumlah penyewaan sepeda.")
    
    st.subheader("Perbandingan Penyewaan Sepeda: Hari Kerja vs Hari Libur")
    fig_workingday_holiday = plot_workingday_holiday_rentals(hour_df)
    st.pyplot(fig_workingday_holiday)
    st.markdown("Pada grafik di atas, penyewaan sepeda pada hari kerja lebih tinggi dibandingkan hari libur. Ini kemungkinan terjadi karena mayoritas pengguna merupakan pekerja yang membutuhkan transportasi pada saat hari kerja")
    
    st.subheader("Hubungan Suhu dan Cuaca pada Penyewaan Sepeda pada Hari Kerja")
    fig_workday_temp = plot_workday_temp_rentals(hour_df)
    st.pyplot(fig_workday_temp)    
    st.markdown("Grafik di atas merupakan gabungan dari visualisasi suhu dan kondisi cuaca terhadap jumlah penyewaan sepeda pada hari kerja. Dapat dilihat bahwa suhu 'mild' dengan kondisi cuaca 'Clear' menjadi kombinasi favorit bagi pengguna untuk menyewa sepeda.")

    st.set_option('deprecation.showPyplotGlobalUse', False)

if __name__ == '__main__':
    main()
