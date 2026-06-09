from student import Student
import json
#系统类
class StudentManager:
    #构建学生列表
    def __init__(self):
        self.student_list = []
    #添加学生功能函数
    def add(self):
        name = input("请输入学生姓名")
        for s in self.student_list:
            if s.name == name:

                print("该学生已存在")
                return
        else:
            score  = int(input("请输入成绩"))

            if 0 <= score <= 100  :
                stu = Student(name,score)
                self.student_list.append(stu)
                print("学生信息添加成功")
            else:
                print("学生成绩必须在0-100之间")
    #保存数据功能函数
    def save_data(self):
        data = []
        for s in self.student_list:
            data.append({"name": s.name,"score": s.score})
        with open("students.json", "w", encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
        print("数据保存成功")
    #加载数据功能函数
    def load_data(self):
        try:
            with open("students.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    stu = Student(item["name"],item["score"])
                    self.student_list.append(stu)
            print("数据加载成功")
        except FileNotFoundError:
            print("首次运行，没有数据")
    #查询学生函数
    def query_student(self):
        name = input("请输入学生姓名")
        for s in self.student_list:
            if s.name == name:
                print(f"学生信息:{s}")
                return
        print("没有该学生")
    #查询所有学生函数
    def show_all(self):

        if len(self.student_list) == 0:
            print("暂无学生")
            return

        for s in self.student_list:
            print(s)
    #修改学生成绩函数
    def update_student(self):
        name = input("请输入修改的学生姓名")
        for s in self.student_list:
            if s.name == name:
                print(f"当前成绩:{s}")
                score = int(input("请输入修改后的成绩"))
                if 0 <= score <= 100:
                    s.update_score(score)
                    print("修改成功")
                    print(f"修改后成绩:{s}")
                    return
                else:
                    print("成绩必须在0-100之间")
                    return
        print("没有该学生")
    #删除学生函数
    def delete_student(self):

        name = input("请输入删除的学生姓名")

        for s in self.student_list:

            if s.name == name:
                self.student_list.remove(s)

                print("删除成功")

                return

        print("没有该学生")