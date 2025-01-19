import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary-data', methods=['GET'])
def summary_data():
    year = request.args.get('year', '2023')  # Default tahun 2023
    df = pd.read_excel('dataset.xlsx', sheet_name='Jumlah Balita Stunting')
    df.columns = df.columns.str.strip()  # Membersihkan nama kolom dari spasi
    
    year_column = f'total_persen_stunting_{year}'
    if year_column not in df.columns:
        return jsonify({"error": f"Column '{year_column}' not found in dataset"}), 400
    
    highest = df.loc[df[year_column].idxmax()]
    lowest = df.loc[df[year_column].idxmin()]
    summary = {
        "highest": {
            "region": highest['Kabupaten/Kota'],
            "value": round(float(highest[year_column]) * 100, 2)
        },
        "lowest": {
            "region": lowest['Kabupaten/Kota'],
            "value": round(float(lowest[year_column]) * 100, 2)
        }
    }
    return jsonify(summary)

@app.route('/linechart-data', methods=['GET'])
def linechart_data():
    year = request.args.get('year', 'all')  # Ambil parameter tahun, default 'all'
    df = pd.read_excel('dataset.xlsx', sheet_name='Jumlah Balita Stunting')
    df.columns = df.columns.str.strip()  # Membersihkan nama kolom dari spasi

    # Pastikan hanya kolom angka yang dikonversi ke float
    df[['Stunting_2021', 'Stunting_2022', 'Stunting_2023']] = df[
        ['Stunting_2021', 'Stunting_2022', 'Stunting_2023']
    ].apply(pd.to_numeric, errors='coerce')  # Konversi ke angka, ganti invalid menjadi NaN

    if year != 'all':
        year_column = f"Stunting_{year}"
        if year_column in df.columns:
            line_data = df[['Kabupaten/Kota', year_column]].rename(columns={year_column: 'value'}).to_dict(orient='records')
        else:
            line_data = []  # Jika kolom tidak ditemukan, kembalikan array kosong
    else:
        line_data = df[['Kabupaten/Kota', 'Stunting_2021', 'Stunting_2022', 'Stunting_2023']].to_dict(orient='records')

    return jsonify(line_data)


if __name__ == '__main__':
    app.run(debug=True)
