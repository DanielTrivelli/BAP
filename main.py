from json import load
from os import system


def execute_class():
    from automation_class import BasicAutomationProcess
    file = load(open('example.json', 'r', encoding='utf-8'))
    automation_process = BasicAutomationProcess(file)
    automation_process.execute()


if __name__ == '__main__':
    try:
        execute_class()
    except ModuleNotFoundError:
        system('pip install -r requirements.txt')
        execute_class()
