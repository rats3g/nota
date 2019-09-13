# nota

nota is a scaffolding tool for developer notes. Out of the box, nota provides sensible defaults for common development scenarios - defects, stories, bugs, and features. nota promotes productive notetaking habits and allows for customization to accommodate unique workflows.

## Install

Install nota with:

```shell
pip install rats3g-nota
```

Run nota and list possible arguments using:

```shell
nota -h
```

## Configuration

nota supports configuration using command line parameters and a [JSON](https://www.json.org/) config file. Precedence is: `command line -> config file -> internal defaults`.

| Option                         | Command Line  | Config          | Variable |
| :----------------------------- | :-----------: | :-------------- | :------- |
| Generate bug template          |   -b --bug    | bug.*           | $option  |
| Set custom configuration file  |  -c --config  |                 |          |
| Generate defect template       |  -d --defect  | defect.*        | $option  |
| Use custom list of directories | --directories | *.directories[] |          |
| Generate feature template      | -f --feature  | feature.*       |          |
| Set note filename              |  --filename   | *.filename      |          |
| Print help information         |   -h --help   |                 |          |
| Set note unique ID             | --identifier  |                 | $id      |
| List available notes           |   -l --list   |                 |          |
| Create note                    |    \<NAME>    |                 | $name    |
| Generate custom template       |  -o --option  | $option.*       | $option  |
| Set root directory for notes   |   -r --root   | root            | $root    |
| Generate story template        |  -s --story   | story.*         | $option  |
| Use custom template for note   | -t --template | *.template      |          |
| Print version information      | -v --version  |                 |          |

## Development

To get started with nota development, clone the [Git](https://git-scm.com/) repository

```shell
git clone https://github.com/pyscaffold/pyscaffold.git
```

Install development dependencies using [pip](https://pypi.org/project/pip/)

```shell
pip install -r requirements.txt
```

Finally, setup nota for development with the usual

```shell
python setup.py develop
```

and you are ready to go. Any changes you make will be reflected when you run nota.
