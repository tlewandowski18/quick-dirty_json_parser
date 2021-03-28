from parglare import Grammar, Parser

#grammar rules

grammar = r"""
Obj: "{" KVPairs "}" {right};
KVPairs: KVPair | KVPairs KVPair | EMPTY;
KVPair: Key Value "," | Key Value;
Value: String 
 | Boolean 
 | Number
 | Obj
 | List
 | Null
;
ListItem: Value "," | Value;
ListItems: ListItem | ListItems ListItem | EMPTY;
List: "[" ListItems "]" {left, 11};

 terminals
 Key: /"?[A-Za-z][_a-zA-Z0-9]*"?:/;
 String: /"[^"]*"/;
 Boolean: /[tTfF][ra][ul][es]e?/;
 Number: /\d*(\.\d+)?/;
 Null: /[Nn]ull/;
 """

#Helper Function to format object string

def parse_obj_string(obj_str):
    obj_str_lst = obj_str.split("\n")
    stripped_obj_str_lst = [line.strip() for line in obj_str_lst]
    final_obj_str_lst = []
    for i in range(len(stripped_obj_str_lst)):
        cur_str = stripped_obj_str_lst[i]
        if i == 0:
            final_obj_str_lst.append(cur_str)
        else:
            prev_str = final_obj_str_lst[i - 1]
            count = prev_str.count("\t")
            if prev_str[-1] == "{" or prev_str[-1] == "[":
                num_tabs = count + 1
            elif cur_str[0] == "}" or cur_str[0] == "]":
                num_tabs = count - 1
            else:
                num_tabs = count
            tab_str = "\t" * num_tabs
            formatted_line = tab_str + stripped_obj_str_lst[i]
            final_obj_str_lst.append(formatted_line)
    return "\n".join(final_obj_str_lst)

#Semantic Actions


def key_value_str(context, nodes):
    key = nodes[0]
    value = nodes[1]

    if key[0] != '"' and key[-2] != '"':
        return f'"{key[:-1]}": {value}'
    elif key[0] != '"':
        return f'"{key} {value}'
    elif key[-2] != '"':
        return f'{key[:-1]}": {value}'
    else:
        return f'{key} {value}'

def parse_boolean(context, value):
    if value[0] == "t":
        return "True"
    elif value[0] == "f":
        return "False"
    else:
        return value


actions = {
    # "Obj": lambda _, nodes: parse_obj_string("{\n%s\n}" % (nodes[1])),
    "Obj": lambda _, nodes: parse_obj_string("{\n%s\n}" % (nodes[1])),
    "KVPairs": lambda _, nodes: ",\n".join(nodes),
    "KVPair": key_value_str,
    "Boolean": parse_boolean,
    "ListItem": lambda _, nodes: nodes[0],
    "ListItems": lambda _, nodes: ",\n".join(nodes),
    "List": lambda _, nodes: "[\n%s\n]" % (nodes[1])
}

#instantiate grammar

g = Grammar.from_string(grammar)

parser = Parser(g, actions=actions)

sample_obj_str1 = '{"key": "value", boolean: false, number: 5, boolean2: 7, number2: True, lst: [2,"hello",true,"str2",{"innerkey": "innervalue", "innerkey1": 76}, [1, "string", true]], obj: {"key_num": 22.45, "key_bool": True, key_str: "happy", inner_obj: {"innerkey": "innervalue", "innerkey1": 76}, lst1: [1, 2, 3, 4]}}'
sample_obj_str2 = '{ "key": "value" }'
sample_obj_str3 = """{ "key": ["value", 0.5, 
	{ "test": 56, 
	"test2": [true, null] }
	]
}"""

result = parser.parse(sample_obj_str3)

print(result)

