import requests
from bs4 import BeautifulSoup
from csv import DictWriter
import os
import argparse

url = 'http://durslt.du.ac.in/DURSLT_ND2020/Students/Combine_GradeCard.aspx'

def deconstruct_rollno(rollno):
    year = str(rollno)[0:2]
    college_id = str(rollno)[2:5]
    course_id = str(rollno)[5:8]
    
    return (year, college_id, course_id)

def make_payload(doc, college_id, rollno):
    payload = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ddlcollege': college_id,
        'txtrollno': str(rollno),
        'btnsearch': 'Print Score Card',
    }
    
    img_captcha = doc.find('img', {'id':'imgCaptcha'})
    captcha = img_captcha['src'].split('=')[1].split('&')[0]
    
    payload['txtcaptcha'] = captcha
    payload['__EVENTVALIDATION'] = doc.find('input', id='__EVENTVALIDATION')['value']
    payload['__VIEWSTATE'] = doc.find('input', id='__VIEWSTATE')['value']
    payload['__VIEWSTATEGENERATOR'] = doc.find('input', id='__VIEWSTATEGENERATOR')['value']
    
    return payload

def fetch_result(college_id, rollno):
    session = requests.session()
    
    response = session.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    
    payload = make_payload(doc, college_id, rollno)
    response = session.post(url=url, data=payload)
    
    session.close()
    return response.text

def fetch(start_rollno, end_rollno):
    print(f'Fetching results from roll number {start_rollno} to {end_rollno}...')
    
    directory_name = 'DownloadedResults'
    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)
    
    year, college_id, course_id = deconstruct_rollno(start_rollno)

    path = os.path.join(directory_name, year, college_id, course_id)
    os.makedirs(path, exist_ok=True)
    os.chdir(path)
    
    print(f'Fetched results will be saved in {path}')
    
    for rollno in range(start_rollno, end_rollno+1):
        result_page = fetch_result(college_id, rollno)
        
        with open(f'result_{rollno}.html', 'w') as f:
            f.write(result_page)
        
def parse_result(filename):
    doc = BeautifulSoup(open(filename, encoding="utf8"), "html.parser")
    
    if (doc.find('input', {'id':'btnsearch'}) != None):
        # invalid page
        return {}

    parsed_data = {
        'Name' : doc.find('span', {'id' : 'lblname'}).text.strip(),
        'Roll_Number' : doc.find('span', {'id' : 'lblrollno'}).text.strip()
    }

    sgpa_table = doc.find('table', {'id' : 'gv_sgpa'})
    sgpa_table_rows = sgpa_table.find_all('tr')[1:]

    for row in sgpa_table_rows:
        data = row.find_all('td')
        sem = data[0].get_text().strip()
        sem_sgpa = data[3].get_text().strip()
        
        parsed_data[f'SGPA_sem_{sem}'] = sem_sgpa
        
        year_cgpa = data[5].get_text().strip()
        if year_cgpa:
            if (sem == 'II'):
                parsed_data[f'CGPA_1'] = year_cgpa
            elif (sem == 'IV'):
                parsed_data[f'CGPA_2'] = year_cgpa
            elif (sem == 'VI'):
                parsed_data[f'CGPA_3'] = year_cgpa
        
    return parsed_data

def parse(start_rollno, end_rollno):
    print(f'Parsing results from roll number {start_rollno} to {end_rollno}...')
    
    directory_name = 'DownloadedResults'
    year, college_id, course_id = deconstruct_rollno(args.start_rollno)
    
    path = os.path.join(directory_name, year, college_id, course_id)
    os.chdir(path)
    
    csv_filename = f'{year}{college_id}{course_id}.csv'
    print(f'.csv data from parsed results will be saved in {path}/{csv_filename}')
    
    outfile = open(f'{csv_filename}', 'w')
    fields = [
        'Name','Roll_Number','SGPA_sem_I','SGPA_sem_II','CGPA_1',
        'SGPA_sem_III', 'SGPA_sem_IV', 'CGPA_2',
        'SGPA_sem_V', 'SGPA_sem_VI', 'CGPA_3',
        'Grand_CGPA', 'Division'
    ]
    writer = DictWriter(outfile, fieldnames=fields)
    writer.writeheader()
    
    for rollno in range(start_rollno, end_rollno+1):
        filename = f'result_{rollno}.html'
        #print(f"Parsing: {filename}")
        parsed_data = parse_result(filename)
        writer.writerow(parsed_data)
    
    outfile.close()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", dest='fetch', default=False, action='store_true',
                        help='Fetch results for a range of roll numbers.')
    parser.add_argument("--parse", dest='parse', default=False, action='store_true',
                        help='Parse results for a range of roll numbers. Note: If both fetch and parse are set, parse will be ignored.')    
    parser.add_argument("--from", dest='start_rollno', type=int,
                        help="Start fetching results from this roll number.", required=True)
    parser.add_argument("--to", dest='end_rollno', type=int,
                        help="Fetch results until this roll number.", required=True)
    args = parser.parse_args()
    
    if (args.fetch):
        fetch(args.start_rollno, args.end_rollno)
    elif (args.parse):
        parse(args.start_rollno, args.end_rollno)
    else:
        parser.error("At least one of --fetch or --parse is required.")
