from manager import StudentManager

#运行程序
manager = StudentManager()
manager.load_data()#加载数据
while True:

    print("1.添加学生")
    print("2.查询学生")
    print("3.修改成绩")
    print("4.查看所有学生")
    print("5.删除学生")
    print("6.退出")

    choice = input("请选择:")

    if choice == "1":
        manager.add()

    elif choice == "2":
        manager.query_student()

    elif choice == "3":
        manager.update_student()
    elif choice == "4":
        manager.show_all()
    elif choice == "5":
        manager.delete_student()

    elif choice == "6":
        manager.save_data()
        print("退出系统")
        break

    else:
        print("输入错误")