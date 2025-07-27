from flask import Flask, render_template_string
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Flask
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Example CSV path (update as needed)
CSV_PATH = 'Dataset_Preparation/data_processed/all_years_comp_v5.csv'

@app.route('/')
def index():
    # Load your F1 data
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        return f"Error loading CSV: {e}"

    # Example: plot tyre_life distribution for each compound
    fig, ax = plt.subplots(figsize=(8, 5))
    for compound in df['compound'].unique():
        subset = df[df['compound'] == compound]
        ax.hist(subset['tyre_life'], bins=20, alpha=0.5, label=compound)
    ax.set_xlabel('Tyre Life')
    ax.set_ylabel('Count')
    ax.set_title('Tyre Life Distribution by Compound')
    ax.legend()

    # Convert plot to PNG image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    # Render HTML with embedded image
    html = f'''
    <html>
    <head><title>F1 Tyre Life Analysis</title></head>
    <body>
        <h1>F1 Tyre Life Analysis</h1>
        <nav>
            <a href="/">Tyre Life Distribution</a> |
            <a href="/average">Average Tyre Life</a> |
            <a href="/usage">Compound Usage Count</a>
        </nav>
        <img src="data:image/png;base64,{img_base64}" />
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/average')
def average_tyre_life():
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        return f"Error loading CSV: {e}"
    avg_life = df.groupby('compound')['tyre_life'].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    avg_life.plot(kind='bar', ax=ax)
    ax.set_xlabel('Compound')
    ax.set_ylabel('Average Tyre Life')
    ax.set_title('Average Tyre Life per Compound')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    html = f'''
    <html>
    <head><title>Average Tyre Life</title></head>
    <body>
        <h1>Average Tyre Life per Compound</h1>
        <nav>
            <a href="/">Tyre Life Distribution</a> |
            <a href="/average">Average Tyre Life</a> |
            <a href="/usage">Compound Usage Count</a>
        </nav>
        <img src="data:image/png;base64,{img_base64}" />
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/usage')
def compound_usage():
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        return f"Error loading CSV: {e}"
    usage_count = df['compound'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    usage_count.plot(kind='bar', ax=ax)
    ax.set_xlabel('Compound')
    ax.set_ylabel('Usage Count')
    ax.set_title('Compound Usage Count')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    html = f'''
    <html>
    <head><title>Compound Usage Count</title></head>
    <body>
        <h1>Compound Usage Count</h1>
        <nav>
            <a href="/">Tyre Life Distribution</a> |
            <a href="/average">Average Tyre Life</a> |
            <a href="/usage">Compound Usage Count</a>
        </nav>
        <img src="data:image/png;base64,{img_base64}" />
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/random_forest')
def random_forest_actual_vs_predicted():
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Model_Training')))
    import training_data as td
    import joblib
    import matplotlib.pyplot as plt
    import io, base64
    # OHE Compound Model
    x_train1, x_test1, y_train1, y_test1 = td.get_training_data()
    if x_train1.empty or y_train1.empty:
        html = '''<html><body><h1>No valid training data available for Random Forest model.</h1></body></html>'''
        return render_template_string(html)
    # Load pre-trained model
    try:
        rf1 = joblib.load(os.path.abspath(os.path.join(os.path.dirname(__file__), '../rf_model_v5.joblib')))
    except Exception as e:
        html = f'''<html><body><h1>Error loading model: {e}</h1></body></html>'''
        return render_template_string(html)
    predictions1 = rf1.predict(x_test1)
    # Single scatter plot for actual vs predicted
    fig = plt.figure(figsize=(8, 6))
    plt.scatter(y_test1, predictions1, alpha=0.6)
    plt.xlabel('Actual Tyre Life')
    plt.ylabel('Predicted Tyre Life')
    plt.title('Random Forest: Actual vs Predicted Tyre Life')
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    html = f'''
    <html>
    <head><title>Random Forest Actual vs Predicted</title></head>
    <body>
        <h1>Random Forest: Actual vs Predicted Tyre Life</h1>
        <nav>
            <a href="/">Tyre Life Distribution</a> |
            <a href="/average">Average Tyre Life</a> |
            <a href="/usage">Compound Usage Count</a> |
            <a href="/random_forest">Random Forest Actual vs Predicted</a>
        </nav>
        <img src="data:image/png;base64,{img_base64}" />
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
