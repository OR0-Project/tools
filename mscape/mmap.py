# //////////////////////////////////////////////////////////////////////////////
# // File:     Name:        mmap.py                                           //
# //           Language:    Python 3                                          //
# //                                                                          //
# // Details:  Memory map format utilities.                                   //
# //                                                                          //
# // Author:   Name:    Marijn Verschuren, Ralph Vreman                       //
# //           Email:   marijnverschuren3@gmail.com                           //
# //                                                                          //
# // Date:     2023-10-25                                                     //
# //////////////////////////////////////////////////////////////////////////////

COMMENT_CHAR = "#"

TOKENS = {
    "TOK_LRBRACK": "lrbrack", # [
    "TOK_RRBRACK": "rrbrack", # ]
    "TOK_PARENTHLEFT": "pleft", # (
    "TOK_PARENTHRIGHT": "pright", # )
    "TOK_STMTEND": "stend", # ;
    "TOK_IDENTIFIER": "ident", # name
    "TOK_MINUS": "minus", # -
    "TOK_NUM": "num", # 0x7c000, 10000
    "TOK_STR": "strg", # String literal
    "TOK_FIELD": "field", # Part of a field
    "TOK_LBRACE": "lbrace", # {
    "TOK_RBRACE": "rbrace", # }
    "TOK_KEYWORD": "kword",
    "TOK_ASSIGNMENT": "assign" # =
}

TOK_SYMS = {
    "(": TOKENS["TOK_PARENTHLEFT"],
    ")": TOKENS["TOK_PARENTHRIGHT"],
    ";": TOKENS["TOK_STMTEND"],
    "-": TOKENS["TOK_MINUS"],
    "[": TOKENS["TOK_LRBRACK"],
    "]": TOKENS["TOK_RRBRACK"],
    "{": TOKENS["TOK_LBRACE"],
    "}": TOKENS["TOK_RBRACE"],
    "=": TOKENS["TOK_ASSIGNMENT"]
}

KEYWORDS = ["range"]

WHITESPACE_CHRS = ['\n', '\r', ' ']

"""
Checks whether the char is a number.
"""
def _isNumber(ch, is_hex = False):
    code = ord(ch.upper())

    if not ((code >= 48) and (code <= 57)):
        if is_hex and ((code >= 65) and (code <= 70)):
            return True
    else:
        return True
    
    return False

"""
Checks whether the character can be part of a word.
"""
def _isWordSym(ch):
    code = ord(ch)

    # a-z
    if ((code >= 97) and (code <= 122)):
        return True

    # A - Z
    if ((code >= 65) and (code <= 90)):
        return True
    
    # Misc symbols
    if ch in (["$", "_"]):
        return True

    return False

"""
Performs lexical analysis
"""
def lex(text):
    text_len = len(text)
    tokens = []

    skip = 0

    for x in range(0, text_len):
        if skip > 0:
            skip -= 1
            continue

        if text[x] == COMMENT_CHAR:
            skip = text.index('\n', x) - x
            continue

        if text[x] in WHITESPACE_CHRS:
            continue

        # Check for numeric literal
        n_negative = text[x] == "-"
        n_hex = text[x:x + 2] == "0x"
        
        if ((n_negative or n_hex) and _isNumber(text[x])) or _isNumber(text[x], n_hex):
            temp = ""
            ystart = x

            if n_negative:
                ystart += 1

            if n_hex:
                ystart += 2

            for y in range(ystart, text_len):
                if not _isNumber(text[y], n_hex):
                    skip = y - x - 1

                    # Construct number
                    if n_hex:
                        temp = f"0x{temp}"

                    if n_negative:
                        temp = f"-{temp}"

                    tokens.append({ 'value': int(temp, 0), "type": TOKENS["TOK_NUM"] })
                    break
                else:
                    temp += text[y]

            continue
        
        # Check for string literal
        if text[x] == '"':
            temp = ""

            for y in range(x + 1, text_len):
                if text[y] == '"' and text[y - 1] != '\\':
                    tokens.append({ 'value': temp, "type": TOKENS["TOK_STR"] })
                    skip = y - x
                    break
                else:
                    temp += text[y]

            continue

        # Check for identifier
        if _isWordSym(text[x]):
            temp = ""

            for y in range(x, text_len):
                if not _isWordSym(text[y]):
                    if temp in KEYWORDS:
                        tokens.append({ 'value': temp, "type": TOKENS["TOK_KEYWORD"] })
                    else:
                        tokens.append({ 'value': temp, "type": TOKENS["TOK_IDENTIFIER"] })

                    skip = y - x
                    break
                else:
                    temp += text[y]

            continue

        # Check if we are a token symbol
        if text[x] in TOK_SYMS.keys():
            tokens.append({ "type": TOK_SYMS[text[x]] })
            continue

        raise Exception(f"Unexpected token \"{text[x]}:{x}\"")
    return tokens

"""
Gets the token by type
"""
def _getToken(list, idx, typeid):
    try:
        return list[idx]["type"] == typeid
    except:
        pass

    return False

"""
Captures a property block
"""
def _capturePropBlock(lst, idx):
    # Next token must be a block open token
    if not _getToken(lst, idx, TOKENS["TOK_LBRACE"]):
        raise Exception(f"Block opener expected")
    
    props = []
    skip = 0

    for x in range(idx + 1, len(lst)):
        if skip > 0:
            skip -= 1
            continue

        if _getToken(lst, x, TOKENS["TOK_RBRACE"]):
            break

        if _getToken(lst, x, TOKENS["TOK_IDENTIFIER"]):
            if not _getToken(lst, x + 1, TOKENS["TOK_ASSIGNMENT"]):
                raise Exception("Assignment expected.")
            
            if not (_getToken(lst, x + 2, TOKENS["TOK_STR"]) or _getToken(lst, x + 2, TOKENS["TOK_NUM"])):
                raise Exception("Value expected.")
            
            if not _getToken(lst, x + 3, TOKENS["TOK_STMTEND"]):
                raise Exception("End of statement expected.")

            props.append({
                'id': lst[x]['value'],
                'value': lst[x + 2]['value']
            })

            skip += 3
            
        else:
            raise Exception("Identifier expected.")

    return props
        

"""
Creates a parsing tree for the specified tokens
"""
def _makeTree(toks):
    ptree = {
        "type": "prgm",
        "nodes": []
    }

    tok_len = len(toks)
    skip = 0

    for x in range(0, tok_len):
        if skip > 0:
            skip -= 1
            continue

        tok = toks[x]

        # Potential tag found
        if(tok["type"] == TOKENS["TOK_LRBRACK"]):
            if not _getToken(toks, x + 1, TOKENS["TOK_IDENTIFIER"]):
                raise Exception("Identifier expected for tag")
            
            if not _getToken(toks, x + 2, TOKENS["TOK_STR"]):
                raise Exception("String value expected")
            
            if not _getToken(toks, x + 3, TOKENS["TOK_RRBRACK"]):
                raise Exception("End of tag bracket expected")

            ptree["nodes"].append({ "type": "tag", "name": toks[x + 2]["value"], "tag": toks[x + 1]["value"] })
            skip += 3

        # Check for keyword
        if(tok["type"] == TOKENS["TOK_KEYWORD"]):
            # Process grammar for range
            if(tok["value"] == "range"):
                # Parse range expr
                if not _getToken(toks, x + 1, TOKENS["TOK_PARENTHLEFT"]):
                    raise Exception("Range expression expected")

                if not _getToken(toks, x + 2, TOKENS["TOK_NUM"]):
                    raise Exception("Left-hand side must be a number")

                if not _getToken(toks, x + 3, TOKENS["TOK_MINUS"]):
                    raise Exception("Range divider not present")

                if not _getToken(toks, x + 4, TOKENS["TOK_NUM"]):
                    raise Exception("Right-hand side must be a number")

                if not _getToken(toks, x + 5, TOKENS["TOK_PARENTHRIGHT"]):
                    raise Exception("Range expression not closed")

                ptree["nodes"].append({
                    "type": "rangeexpr",
                    "lhs": toks[x + 2]['value'],
                    "rhs": toks[x + 4]['value'],
                    "props": _capturePropBlock(toks, x + 6)
                })

                skip += 5
            else:
                raise Exception(f"Keyword not implemented: {tok['value']}")

    return ptree['nodes']

"""
Represents a memory map
"""
class MemoryMap:
    groups = []
    ranges = []

    """
    Gets ranges from a specified group.
    """
    def getByGroup(self, name):
        rng = []

        for i in self.ranges:
            if i['group'] == name:
                rng.append(i)

        return rng

    """
    Gets a range from the specified address.
    """
    def getRangeByAddress(self, address):
        for rng in self.ranges:
            if address >= rng['_lhs'] and address <= rng['_rhs']:
                return rng

        return None

    """
    Gets a range by id.
    """
    def getRange(self, id):
        for rng in self.ranges:
            if rng['id'] == id:
                return rng

        return None

"""
Parses a memory map file.
"""
def parse(path):
    mmap = MemoryMap()

    with open(path, 'r') as fd:
        tokens = lex(fd.read())
    
        # Make parsing tree
        ptree = _makeTree(tokens)
        cur_group = 'Default'

        # State
        for x in ptree:
            # Process tag
            if x['type'] == "tag":
                if x['tag'] == "Group":
                    if x['name'].strip() == "":
                        raise Exception("Tag name cannot be empty")

                    mmap.groups.append(x['name'])
                    cur_group = x['name']
                else:
                    raise Exception(f"Tag not implemented: {x['tag']}")

            # Process range expression
            elif x['type'] == "rangeexpr":
                debug_expr = f"({hex(x['lhs'])} - {hex(x['rhs'])})"
                # Check if the range even makes sense
                if x['lhs'] < 0:
                    raise Exception(f"Invalid range expression '{debug_expr}': LHS < 0")
                elif x['rhs'] < 0:
                    raise Exception(f"Invalid range expression '{debug_expr}': RHS < 0")
                elif (x['rhs'] - x['lhs']) < 0:
                    raise Exception(f"Invalid range expression '{debug_expr}': RHS - LHS < 0")
                elif x['rhs'] == x['lhs']:
                    raise Exception(f"Invalid range expression '{debug_expr}': Not a range! RHS = LHS = 0")

                range_obj = {
                    'id': None,
                    'group': cur_group,
                    'description': '',
                    '_lhs': x['lhs'],
                    '_rhs': x['rhs']
                }

                # Validate properties
                for prop in x['props']:
                    range_obj[prop['id']] = prop['value']

                if range_obj['id'] == None:
                    raise Exception(f"Range expression '{debug_expr}' is missing the required 'id' field!")

                # Append object
                mmap.ranges.append(range_obj)

    return mmap