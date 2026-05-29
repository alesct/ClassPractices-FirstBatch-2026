import os
import jinja_2
from jinja_2 import Environment, FileSystemLoader

os.makedirs("output", exist_ok=True)

with open("output/message1.txt", "w", encoding="utf-8") as f:
    f.write("안녕하세요 {{ name }}님, {{ test_name }} 점수는 {{ score }}/{{ max_score }}점입니다.")

with open("output/message2.txt", "w", encoding="utf-8") as f:
    f.write("안녕하세요 {{ name }}님.\n"
            "점수: {{ score }}점\n"
            "{% if score >= 90 %}축하합니다! 합격입니다.{% else %}재시험 대상입니다.{% endif %}")

print("#" * 100)

environment = jinja_2.Environment()
template = environment.from_string("Hello, {{ name }}!")

print(template.render(name="World"))
print("This is end. -- 1. Render Your First Jinja Template")
print("#" * 100)

max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine",  "score": 100},
    {"name": "Gergeley", "score": 87},
    {"name": "Frieda", "score": 92},
]

file_environment = Environment(loader=FileSystemLoader("output/"))
template1 = file_environment.get_template("message1.txt")

for student in students:
    print(f"student: {student}, name: {student['name']}, score: {student['score']}")
    
    filename = os.path.join("output", f"message1_{student['name'].lower()}.txt") 
   
    content = template1.render(
        student,
        max_score=max_score,
        test_name=test_name
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")
    print("*" * 50)

print("This is end. -- 2. Render a Template from a External File")
print("#" * 100)

template2 = file_environment.get_template("message2.txt")

for student in students:
    if student['score'] >= 90:
        filename = os.path.join("output", f"message2_{student['name'].lower()}.txt") 
        
        content = template2.render(
            student,
            max_score=max_score,
            test_name=test_name
        )
        with open(filename, mode="w", encoding="utf-8") as message:
            message.write(content)
            print(f"[합격자 파일 생성] ... wrote {filename} (점수: {student['score']})")
    else:
        print(f"[보류] {student['name']}님은 파일 생성 대상이 아닙니다. (점수: {student['score']})")
    print("*" * 50)
        
print("This is end. -- 3. Use if Statements")
print("#" * 100)
    
max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine",  "score": 100},
    {"name": "Gergeley", "score": 87},
    {"name": "Frieda", "score": 92},
    {"name": "Fritz", "score": 40},
    {"name": "Sirius", "score": 75},
]
results_filename = "output/students_results.html"
environment = Environment(loader=FileSystemLoader("output/"))

results_template = environment.get_template("results.html")
print(f"...results_template____loaded {results_template}")

context = {
    "students": students,
    "test_name": test_name,
    "max_score": max_score,
}
with open(results_filename, mode="w", encoding="utf-8") as results:
    results.write(results_template.render(context))
    print(f"... wrote {results_filename}")

print("This is end. -- 4. Leverage for Loops")
print("#"*100)    
    
results_filename = "output/students_results_if.html"
environment = Environment(loader=FileSystemLoader("output/"))

results_template = environment.get_template("results.html")

context = {
    "students": students,
    "test_name": test_name,
    "max_score": max_score,
}

with open(results_filename, mode="w", encoding="utf-8") as results:
    results.write(results_template.render(context))
    print(f"... wrote {results_filename}")

print("This is end. -- 5. Leverage for Loops with Conditionals")
print("#"*100)