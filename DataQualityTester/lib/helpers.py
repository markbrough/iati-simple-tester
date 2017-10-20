import re


# given an expression list and the name of an expression,
# select it,
def select_expression(expression_list, expression_name,
                      default_expression_name=None):
    expression_dicts = {x["id"]: x for x in expression_list}
    if expression_name not in expression_dicts:
        expression_name = default_expression_name
    return expression_name, expression_dicts.get(expression_name)


def slugify(inp):
    return inp.lower().replace(' ', '-')


def pprint(explanation):
    explanation = explanation.strip()
    if len(explanation) > 0:
        explanation = explanation[0].upper() + explanation[1:]
    explanation = explanation.replace('\n', '<br>') + '.'
    return re.sub(r'`([^`]*)`', r'<code>\1</code>', explanation)
