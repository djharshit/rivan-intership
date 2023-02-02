import openpyxl
import argparse

parser = argparse.ArgumentParser(description='Load the file in the code.')
parser.add_argument('file', metavar='<file>', type=str, help='The file name')
args = parser.parse_args()

workbook = openpyxl.load_workbook(filename=args.file)
worksheet = workbook.active

with open(file='no.txt', mode='r+') as file:
    i = int(file.read())
    print(i)
    job_title = worksheet[f'A{i}'].value
    stipend = worksheet[f'B{i}'].value
    description = f"{worksheet[f'C{i}'].value}\n\nSkills required:\n{worksheet[f'D{i}'].value}"

    print(i)
    print(job_title)
    # print(stipend)
    # print(description)

    file.truncate(0)
    file.seek(0)
    file.write(str(i+1))
