from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from time import sleep
from traceback import format_exc


class BasicAutomationProcess:
    def __init__(self, process_dict: dict) -> None:
        self.process = process_dict['process']
        self.url = process_dict['url']
        self.actions_need_format = {
            'send_keys': 'value',
            'select': [
                'select_by',
                'value'
            ]
        }
        self.actions = {
            'click': 'element.click()',
            'send_keys': 'element.send_keys("{}";)',
            'select': 'Select(element).select_by_{}("{}")'
        }
        self.element_attributes = {
            'attr': 'element.get_attribute("{}")',
        }
        self.child = False
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get(self.url)

    def run_rules(self, elements, rules) -> list:
        rules = [rules] if isinstance(rules, dict) else rules

        for rule in rules:
            rule_type = rule['type']
            rule_settings = rule['settings']
            if rule_type == 'filter':
                expected = rule_settings['expected']
                rule_return = rule_settings['return']
                element_attribute = self.element_attributes[rule_settings['by']].format(rule_settings['name'])
                if 'notExpected:' in expected:
                    expected = expected.replace('notExpected:', '')
                    elements = [element for element in elements if expected not in eval(element_attribute)]
                else:
                    elements = [element for element in elements if expected in eval(element_attribute)]
                if rule_return != 'all':
                    elements = elements[eval(rule_return)]
                    if not isinstance(elements, list):
                        elements = [elements]

        return elements

    def exec_actions(self, element, parent, settings) -> None:
        settings_action = settings['action'].split(' + ')
        for action in settings_action:
            this_action = self.actions[action]
            has_key = settings.get('press_key')
            if action in self.actions_need_format:
                locale = self.actions_need_format[action]
                locale = locale if ' + ' not in locale else locale.split(' + ')
                if isinstance(locale, list):
                    format_param = ', '.join([f'"{settings[x]}"' for x in locale])
                    this_action = eval(f'this_action.format({format_param})')
                else:
                    format_param = settings[locale]
                    this_action = this_action.format(format_param)
                if has_key and ';' in this_action:
                    key = eval('Keys.' + has_key.upper())
                    this_action = this_action.replace(';', f', "{key}"')
            exec(this_action)

    def rules_and_actions(self, settings, multiple, pre_element, rules, elements) -> None:
        if rules:
            elements = self.run_rules(elements=elements, rules=rules)

        if 'action' in settings:
            if not multiple:
                element = elements
                self.exec_actions(element, pre_element, settings)
            else:
                for idx, element in enumerate(elements):
                    self.exec_actions(element, pre_element, settings)

    def element(self, settings: dict) -> None:
        elements = None
        find_by = settings['find']
        name = settings["element"]
        parent = settings.get('parent')
        child = settings.get('child')
        multiple = settings.get('multiple')
        rules = settings.get('rule')
        pre_find = f'find_element{"s" if multiple else ""}("{find_by}","{name}")'
        pre_element = parent if parent else self.driver
        if isinstance(pre_element, list):
            for pre in pre_element:
                elements = eval(f'pre.{pre_find}')
                self.rules_and_actions(settings, multiple, pre, rules, elements)
        else:
            elements = eval(f'pre_element.{pre_find}')
            self.rules_and_actions(settings, multiple, pre_element, rules, elements)

        if child:
            self.child = {
                'parent': elements,
                'child': child
            }
        elif self.child:
            self.child = False

    def execute(self) -> None:
        try:
            for process_name, process_settings in self.process.items():
                print(f'Running {process_name}')
                for item in process_settings:
                    self.element(item)
                    has_sleep = item.get('sleep')
                    if has_sleep:
                        sleep(has_sleep)
                    while self.child:
                        child_configs = self.child['child']
                        child_configs.update({
                            'parent': self.child['parent']
                        })
                        self.element(settings=child_configs)
                        child_has_sleep = child_configs.get('sleep')
                        if child_has_sleep:
                            sleep(child_has_sleep)
            else:
                print("End Process")
                self.driver.quit()
        except Exception:
            print(format_exc())
            self.driver.quit()
