import csv
class Student:
 def __init__(self, studentid, major, fname, lname, disciplined=False):
    self.studentid = studentid
    self.major = major
    self.lname = lname
    self.fname = fname
    self.disciplined = disciplined
    self.gpa = None
    self.graddate = None

def read_csv(file_path):
 data=[]
 with open(file_path, newline='', encoding='utf-8') as file:
  reader = csv.reader(file)
  for row in reader:
   data.append(row)
 return data
def write_csv(file_path, data):
 with open(file_path, 'w', newline='', encoding='utf-8') as file:
  writer = csv.writer(file)
  writer.writerows(data)

def process_studentdata(studentdata, gpadata, graddata):
  students = {}
  for studentrow in studentdata:
        studentid, lname, fname, major, disciplined = studentrow
        student = Student(studentid, lname, fname, major, disciplined)
        students[studentid] = student
  for graduation_row in graddata:
   studentid, graddate = graduation_row
   students[studentid].graddate = graddate
  for gpa_row in gpadata:
   studentid, gpa = gpa_row
   students[studentid].gpa = float(gpa)
  return students.values()
def generate_fullroster(students):
 fullroster = []
 for student in sorted(students, key=lambda x: x.lname):
   fullroster.append([student.studentid, student.major, student.fname, student.lname,
    student.gpa, student.graddate, student.disciplined])
 return fullroster
def generate_scholarshipcandidates(students):
  scholarshipcandidates = []
  for student in sorted(students, key=lambda x: x.gpa, reverse=True):
    if student.gpa>3.8 and not student.disciplined:
      scholarshipcandidates.append([student.studentid, student.lname, student.fname,
       student.major, student.gpa])
  return scholarshipcandidates
def generate_majlists(students):
 majlists = {}
 for student in sorted(students, key=lambda x: x.studentid):
  filename = f"{student.major.replace(' ', '')} Students.csv"
  if filename not in majlists:
    majlists[filename] = []
  majlists[filename].append([student.studentid, student.lname, student.fname,
                                     student.graddate, student.disciplined])
 return majlists
def generate_disciplinedstudents(students):
 disciplinedstudents = []
 for student in sorted(students, key=lambda x: x.graddate or '', reverse=True):
   if student.disciplined:
    disciplinedstudents.append([student.studentid, student.lname, student.fname,
     student.graddate])
 return disciplinedstudents

def main():
  graddata = read_csv('GraduationDatesList-1.csv')
  studentdata = read_csv('StudentsMajorsList.csv')
  gpadata = read_csv('GPAList-1.csv')
  students = process_studentdata(studentdata, gpadata, graddata)
  fullroster = generate_fullroster(students)
  write_csv('FullRoster.csv', fullroster)
  disciplinedstudents = generate_disciplinedstudents(students)
  write_csv('DisciplinedStudents.csv', disciplinedstudents)
  scholarshipcandidates = generate_scholarshipcandidates(students)
  write_csv('ScholarshipCandidates.csv', scholarshipcandidates)
  majlists = generate_majlists(students)
  for filename, majlist in majlists.items():
   write_csv(filename, majlist)

if __name__ == "__main__":
    main()
