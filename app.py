from flask import Flask, render_template, request, redirect, url_for, send_file
import json
import csv

app = Flask(__name__)

FILE_NAME = 'jobs.json'

# Helper functions to load and save jobs
def load_jobs():
    try:
        with open(FILE_NAME, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_jobs(jobs):
    with open(FILE_NAME, 'w') as f:
        json.dump(jobs, f)

# Load jobs from file
jobs = load_jobs()

@app.route('/')
def home():
    return render_template('index.html', jobs=jobs)

@app.route('/add', methods=['POST'])
def add_job():
    job_title = request.form['job_title']
    company_name = request.form['company_name']
    status = request.form['status']

    jobs.append({
        'job_title': job_title,
        'company_name': company_name,
        'status': status,
        'done': False
    })
    save_jobs(jobs)
    return redirect(url_for('home'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_job(index):
    if 0 <= index < len(jobs):
        jobs.pop(index)
        save_jobs(jobs)
    return redirect(url_for('home'))

@app.route('/done/<int:index>', methods=['POST'])
def mark_done(index):
    if 0 <= index < len(jobs):
        jobs[index]['done'] = True
        save_jobs(jobs)
    return redirect(url_for('home'))

# Export jobs to CSV
@app.route('/export', methods=['GET'])
def export_jobs():
    filename = 'jobs_export.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Job Title', 'Company Name', 'Status', 'Done']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for job in jobs:
            writer.writerow({
                'Job Title': job['job_title'],
                'Company Name': job['company_name'],
                'Status': job['status'],
                'Done': job['done']
            })

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)