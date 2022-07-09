# Basic Automation Process

![GitHub repo size](https://img.shields.io/github/repo-size/DanielTrivelli/BAP?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/DanielTrivelli/BAP?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/DanielTrivelli/BAP?style=for-the-badge)
![Licence MIT](https://img.shields.io/github/license/DanielTrivelli/BAP?style=for-the-badge)

> The goal of this project is to facilitate the creation of automations without the need to create complex scripts.


## Requirements

Before you start, please make sure you meet the following requirements:
* `Python >= 3.6`

Before running the automation, create a folder called `scripts` within the project directory, add a ```.json``` file and configure it according to your needs.
When you finish the previous step, go to ```main.py``` and change the path of the ```example.json``` file to the path where your file is, then, just go to the terminal and run the following command:

> _Ps: If you don't have the required libraries, don't worry, the script will install them automatically_

* Windows:
    ```
    python main.py
    ```
* Linux \ MacOs:
    ```
    python3 main.py
    ```
  

### Allowed Settings

_Example_<br>
_Ps: The items inside the `process` attribute can be named however you like with any amount_

```json
{
  "url": "any url",
  "process": {
    "First Step": [],
    "Second Step": []
  }
}
```

```json
  {
  "First Step": [
    {
      "find": "",
      "element": "",
      "multiple": true,
      "action": "",
      "value": "",
      "press_key": "",
      "select_by": "",
      "rule": [
        {
          "type": "",
          "settings": {
            "by": "",
            "name": "",
            "expected": "",
            "return": ""
          }
        }
      ],
      "child": {
        "find": "",
        "element": "",
        "action": "",
        "value": ""
      },
      "sleep": 0
    }
  ]
}
```

#### Find:
_This attribute tells you which attribute of the element will be used to perform the search, these are the options:_
```text
  id
  xpath
  link text
  partial link text
  name
  tag name
  class name
  css selector
```

#### Element:
_This attribute receives the value needed to perform the search of the element, it must match the type of search that is being used in the ```find``` attribute._

#### Multiple:
_This attribute will be necessary if you need to make a less precise search that returns more than one element._

#### Action:
_This attribute is necessary when you want to perform some action under the element, these are the options:_
```text
  click
  send_keys
  select
```

#### Value:
_This attribute is needed when the attribute value ``action`` is ``send_keys`` or `select`, the script will send the value assigned here to the running element._

#### Select_by:
_This attribute is necessary when the value of the `action` attribute is `select`, so that the script will know where to look for the value assigned in the `value` attribute.<br>
These are the options:_
```text
  value
  index
  visible_text
```

#### Press_key:
_This attribute can be added when the value of the ``action`` attribute is ``send_keys``, the options can be found [here](https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.keys)_<br>
_Ps: Just put the name of the key_

#### Rule
_This attribute can be used if you want to perform some rule on the received elements.<br>
It can only be used if the `multiple` attribute is present.<br>
These are the options:_
* ##### type:
    _This attribute defines what type of rule will be executed, these are the options:<br>_
   ```
      filter
    ```
* ##### settings:
    _This attribute defines what settings are used in the rule, these are the options:_
    ````text
      by
      name
      expected
      return
    ````

  * ###### by:
    _This attribute receives a value to find inside the element, these are the options:_
    ````text
      attr
    ````
  * ###### name:
    _Receives the value needed to perform the search of the element, it must match the type of search that is being used in the ```by``` attribute._
  * ###### expected:
    _Takes the experienced or unexperienced value within the answer found by the ``by`` attribute.<br>
    Ps: If the value is not expected, add ```notExpected:``` before the value to be found._
  * ###### return:
    _If you want to change the filter return, you can use this attribute for that.
     These are the options:_
    * ###### 'all'
      _returns all elements_
    * ###### Any string number:
      _related to the index will return the related element._
    * ###### Expressions:
      _You can also put expressions, such as `"1:4"` or `":1"`_


#### Child
_This attribute is used in case you need to perform actions on certain elements that are not interactable through a single find.<br>
You can have as many children as you like, as along as you keep one child per child.<br>
It has the same settings as a find of any other element._<br><br>
 _Example:_
```json
{
  "find": "",
  "element": "",
  "child": {
    "find": "",
    "element": "",
    "child": {
      "find": "",
      "element": "",
      "action": "",
      "value": ""
    }
  }  
}

```



## License
This project is under the MIT license. See the file [LICENSE](LICENSE.md) for more details.
