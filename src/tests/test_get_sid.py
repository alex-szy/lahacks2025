from commands.install import get_user_and_sid, generate_task_xml

if __name__ == "__main__":
    print(*get_user_and_sid())
    generate_task_xml()
