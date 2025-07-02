from commands.install import generate_task_xml, get_user_and_sid

if __name__ == "__main__":
    print(*get_user_and_sid())
    generate_task_xml()
