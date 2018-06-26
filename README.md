# MonsterParser
A parser for monster.com

## Запуск

устанавливаем завимости:

```bash
>python pip install -r requirements.txt
```

```bash
>python parser.py
```

Парсер принимает два значения в качестве параметров ```url``` на профессию (в качестве дефолтного - https://www.monster.com/jobs/q-financial-analyst-jobs.aspx) и максимальное колличество страниц ```max_pages``` (по дефолту - 2)
например:

```bash
>python parser.py --url='https://www.monster.com/jobs/q-safety-manager-jobs.aspx' --max_pages=3
```
Парсер пишет вывод в output.txt
Пример вывода приведен в example-output.txt
