"""Tiny Dart-subset parser for extracting constant data from the Footfall source.

Handles: literals (strings with adjacent concatenation, ints, doubles, hex, bools,
null), lists, sets, maps, records/tuples, generic type-arg prefixes, constructor
calls (positional + named args, resolved to field names through the class's
constructor signature with defaults), enum refs (-> short name), Duration(...),
references to other top-level constants, switch expressions and ternaries
(conditions kept as raw source text), unary minus and simple arithmetic.

Anything else raises DartParseError with file:line so nothing is skipped silently.
"""
import bisect
import re


class DartParseError(Exception):
    pass


# ---------------------------------------------------------------------------
# Comment stripping (keeps offsets / line numbers intact)
# ---------------------------------------------------------------------------

def strip_comments(src):
    out = list(src)
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c in "'\"":
            i = _skip_string(src, i)
            continue
        if src.startswith('//', i):
            j = src.find('\n', i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = ' '
            i = j
            continue
        if src.startswith('/*', i):
            j = src.find('*/', i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                if out[k] != '\n':
                    out[k] = ' '
            i = j
            continue
        i += 1
    return ''.join(out)


def _skip_string(src, i):
    """Return index just after the string literal starting at i (quote char)."""
    raw = i > 0 and src[i - 1] == 'r' and (i < 2 or not (src[i - 2].isalnum() or src[i - 2] == '_'))
    q = src[i]
    triple = src.startswith(q * 3, i)
    end = q * 3 if triple else q
    j = i + (3 if triple else 1)
    n = len(src)
    while j < n:
        if not raw and src[j] == '\\':
            j += 2
            continue
        if not raw and src.startswith('${', j):
            depth = 1
            j += 2
            while j < n and depth:
                if src[j] in "'\"":
                    j = _skip_string(src, j)
                    continue
                if src[j] == '{':
                    depth += 1
                elif src[j] == '}':
                    depth -= 1
                j += 1
            continue
        if src.startswith(end, j):
            return j + len(end)
        if not triple and src[j] == '\n':
            raise DartParseError('unterminated string at offset %d' % i)
        j += 1
    raise DartParseError('unterminated string at offset %d' % i)


def trailing_comment(line):
    """The // comment at the end of a source line (string-aware), or ''."""
    i, n = 0, len(line)
    while i < n:
        c = line[i]
        if c in "'\"":
            try:
                i = _skip_string(line, i)
            except DartParseError:
                return ''
            continue
        if line.startswith('//', i):
            return line[i:].lstrip('/').strip()
        i += 1
    return ''


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

_OPS = ['...?', '...', '=>', '==', '!=', '<=', '>=', '&&', '||', '??', '?.', '~/', '++', '--',
        '+=', '-=', '*=', '/=']
_ESC = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', "'": "'", '"': '"', '$': '$', 'b': '\b', 'f': '\f',
        'v': '\v', '0': '\0'}


class Tok:
    __slots__ = ('kind', 'val', 'pos', 'end')

    def __init__(self, kind, val, pos, end):
        self.kind, self.val, self.pos, self.end = kind, val, pos, end

    def __repr__(self):
        return 'Tok(%s,%r)' % (self.kind, self.val)


def _decode_string(body, raw):
    if raw:
        return body
    out, i = [], 0
    while i < len(body):
        c = body[i]
        if c == '\\' and i + 1 < len(body):
            d = body[i + 1]
            if d == 'u':
                if body[i + 2:i + 3] == '{':
                    j = body.index('}', i)
                    out.append(chr(int(body[i + 3:j], 16)))
                    i = j + 1
                else:
                    out.append(chr(int(body[i + 2:i + 6], 16)))
                    i += 6
                continue
            if d == 'x':
                out.append(chr(int(body[i + 2:i + 4], 16)))
                i += 4
                continue
            out.append(_ESC.get(d, d))
            i += 2
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def tokenize(code):
    toks = []
    i, n = 0, len(code)
    while i < n:
        c = code[i]
        if c.isspace():
            i += 1
            continue
        if c in "'\"" or (c == 'r' and i + 1 < n and code[i + 1] in "'\""):
            raw = c == 'r'
            qs = i + 1 if raw else i
            j = _skip_string(code, qs)
            q = code[qs]
            ql = 3 if code.startswith(q * 3, qs) else 1
            body = code[qs + ql:j - ql]
            toks.append(Tok('str', _decode_string(body, raw), i, j))
            i = j
            continue
        if c.isdigit():
            m = re.compile(r'0[xX][0-9a-fA-F]+|\d+(\.\d+)?([eE][+-]?\d+)?').match(code, i)
            s = m.group(0)
            if s.lower().startswith('0x'):
                v = int(s, 16)
            elif m.group(1) or m.group(2):
                v = float(s)
            else:
                v = int(s)
            toks.append(Tok('num', v, i, m.end()))
            i = m.end()
            continue
        if c.isalpha() or c in '_$':
            m = re.compile(r'[A-Za-z_$][A-Za-z0-9_$]*').match(code, i)
            toks.append(Tok('id', m.group(0), i, m.end()))
            i = m.end()
            continue
        for op in _OPS:
            if code.startswith(op, i):
                toks.append(Tok('op', op, i, i + len(op)))
                i += len(op)
                break
        else:
            toks.append(Tok('op', c, i, i + 1))
            i += 1
    return toks


# ---------------------------------------------------------------------------
# Values
# ---------------------------------------------------------------------------

class Obj(dict):
    """Result of a constructor call (dict of field -> value) remembering its class."""

    def __init__(self, cls, *a, **k):
        super().__init__(*a, **k)
        self.cls = cls


class DartSet(list):
    pass


def duration(args, named):
    if args:
        raise DartParseError('Duration with positional args')
    mult = {'days': 86400, 'hours': 3600, 'minutes': 60, 'seconds': 1, 'milliseconds': 0.001,
            'microseconds': 1e-6}
    secs = 0
    for k, v in named.items():
        if k not in mult:
            raise DartParseError('unknown Duration field ' + k)
        secs += v * mult[k]
    d = dict(named)
    d['total_seconds'] = secs
    return d


class CtorSpec:
    def __init__(self, cls, positional, optional_positional, named, defaults):
        self.cls = cls
        self.positional = positional
        self.optional_positional = optional_positional
        self.named = named
        self.defaults = defaults  # name -> value (absent = no default -> None)

    def build(self, args, named, where):
        allpos = self.positional + self.optional_positional
        if len(args) > len(allpos) or len(args) < len(self.positional):
            raise DartParseError('%s: %s() expects %d..%d positional args, got %d'
                                 % (where, self.cls, len(self.positional), len(allpos), len(args)))
        o = Obj(self.cls)
        for name, v in zip(allpos, args):
            o[name] = v
        for name in allpos[len(args):]:
            o[name] = self._default(name)
        for k, v in named.items():
            if k not in self.named:
                raise DartParseError('%s: %s() has no named param %r' % (where, self.cls, k))
            o[k] = v
        for k in self.named:
            if k not in o:
                o[k] = self._default(k)
        return o

    def _default(self, name):
        d = self.defaults.get(name)
        if isinstance(d, _LazyDefault):
            d = self.defaults[name] = d.value()
        return clone(d)


class _LazyDefault:
    def __init__(self, f, toks):
        self.f, self.toks = f, toks

    def value(self):
        p = Parser(self.f, self.toks)
        v = p.expr()
        p.expect_end()
        return v


def clone(v):
    if isinstance(v, Obj):
        return Obj(v.cls, {k: clone(x) for k, x in v.items()})
    if isinstance(v, DartSet):
        return DartSet(clone(x) for x in v)
    if isinstance(v, dict):
        return {k: clone(x) for k, x in v.items()}
    if isinstance(v, list):
        return [clone(x) for x in v]
    return v


def plain(v):
    """Strip Obj/DartSet wrappers for JSON."""
    if isinstance(v, dict):
        return {k: plain(x) for k, x in v.items()}
    if isinstance(v, list):
        return [plain(x) for x in v]
    return v


# ---------------------------------------------------------------------------
# Source file + parser
# ---------------------------------------------------------------------------

class DartFile:
    def __init__(self, path, registry):
        self.path = path
        self.name = path.split('/')[-1]
        with open(path, encoding='utf-8') as f:
            self.src = f.read()
        self.lines = self.src.split('\n')
        self.code = strip_comments(self.src)
        self.toks = tokenize(self.code)
        self._starts = [t.pos for t in self.toks]
        self._line_starts = [0] + [m.end() for m in re.finditer('\n', self.src)]
        self.reg = registry
        registry.files[self.name] = self
        self.env = {}  # top-level constants resolved lazily
        self._scan_enums()
        self._scan_ctors()

    # -- positions ------------------------------------------------------------
    def line_of(self, pos):
        return bisect.bisect_right(self._line_starts, pos)

    def tok_at(self, pos):
        i = bisect.bisect_left(self._starts, pos)
        return i

    def err(self, tok_or_pos, msg):
        pos = tok_or_pos.pos if isinstance(tok_or_pos, Tok) else tok_or_pos
        ln = self.line_of(pos)
        text = self.lines[ln - 1].strip() if 0 < ln <= len(self.lines) else ''
        return DartParseError('%s:%d: %s\n    %s' % (self.name, ln, msg, text))

    # -- scanning -------------------------------------------------------------
    def _scan_enums(self):
        for m in re.finditer(r'\benum\s+(\w+)\s*\{', self.code):
            self.reg.enums.add(m.group(1))
            self.reg.enum_file[m.group(1)] = self

    def _scan_ctors(self):
        for m in re.finditer(r'\b(?:class|enum)\s+(\w+)[^{;]*\{', self.code):
            cls = m.group(1)
            body_start = m.end()
            body_end = self.matching(body_start - 1)
            for cm in re.finditer(r'(?:^|\n)[ \t]*(?:const\s+)?' + re.escape(cls) + r'\s*\(', self.code[body_start:body_end]):
                p = body_start + cm.end() - 1  # at '('
                close = self.matching(p)
                params = self.code[p + 1:close]
                if not params.strip():
                    spec = CtorSpec(cls, [], [], [], {})
                elif 'this.' in params:
                    spec = self._parse_params(cls, p + 1, close)
                else:
                    continue
                self.reg.ctors[cls] = spec
                break

    def matching(self, pos):
        """Offset of the bracket matching the one at code[pos]."""
        pairs = {'(': ')', '[': ']', '{': '}'}
        i = self.tok_at(pos)
        if self.toks[i].pos != pos or self.toks[i].val not in pairs:
            raise self.err(pos, 'not a bracket')
        depth = 0
        for t in self.toks[i:]:
            if t.kind == 'op' and t.val in '([{':
                depth += 1
            elif t.kind == 'op' and t.val in ')]}':
                depth -= 1
                if depth == 0:
                    return t.pos
        raise self.err(pos, 'unbalanced bracket')

    def _parse_params(self, cls, a, b):
        ti, tj = self.tok_at(a), self.tok_at(b)
        toks = self.toks[ti:tj]
        positional, optional, named, defaults = [], [], [], {}
        mode = 'pos'
        segs, cur, depth = [], [], 0
        for t in toks:
            if depth == 0 and t.kind == 'op' and t.val in ('[', '{') and not cur:
                mode = 'opt' if t.val == '[' else 'named'
                continue
            if depth == 0 and t.kind == 'op' and t.val in (']', '}'):
                if cur:
                    segs.append((mode, cur))
                cur = []
                continue
            if t.kind == 'op' and t.val in '([{<':
                depth += 1
            elif t.kind == 'op' and t.val in ')]}>':
                depth -= 1
            if depth == 0 and t.kind == 'op' and t.val == ',':
                if cur:
                    segs.append((mode, cur))
                cur = []
                continue
            cur.append(t)
        if cur:
            segs.append((mode, cur))
        for mode, seg in segs:
            eq = next((k for k, t in enumerate(seg) if t.kind == 'op' and t.val == '='), None)
            head = seg if eq is None else seg[:eq]
            name = None
            for k, t in enumerate(head):
                if t.kind == 'id' and t.val == 'this' and k + 2 < len(head) + 1 and head[k + 1].val == '.':
                    name = head[k + 2].val
            if name is None:
                ids = [t.val for t in head if t.kind == 'id' and t.val != 'required']
                if not ids:
                    raise self.err(seg[0], 'bad ctor param')
                name = ids[-1]
            if eq is not None:
                defaults[name] = _LazyDefault(self, seg[eq + 1:])
            {'pos': positional, 'opt': optional, 'named': named}[mode].append(name)
        return CtorSpec(cls, positional, optional, named, defaults)

    # -- lookups --------------------------------------------------------------
    def decl_pos(self, name, static=None):
        """Offset just after `name =` of a const/final declaration."""
        pat = (r'(?:^|\n)[ \t]*' + (r'static\s+' if static else r'(?:static\s+)?') +
               r'(?:const|final)\b[^=;\n]*?\b' + re.escape(name) + r'\s*=(?![=>])')
        m = re.search(pat, self.code)
        if not m:  # second name of a multi-declaration: `const double a = 1, NAME = 2;`
            m = re.search(r'(?:^|\n)[ \t]*(?:static\s+)?const\b[^;\n]*?,\s*' + re.escape(name) + r'\s*=(?![=>])',
                          self.code)
        if not m:
            raise DartParseError('%s: declaration of %s not found' % (self.name, name))
        return m.end()

    def const(self, name):
        if name in self.env:
            return clone(self.env[name])
        pos = self.decl_pos(name)
        p = Parser(self, self.toks, self.tok_at(pos))
        v = p.expr()
        if p.peek().val not in (';', ','):
            raise self.err(p.peek(), 'expected ; after %s' % name)
        self.env[name] = v
        return clone(v)

    def has_decl(self, name):
        try:
            self.decl_pos(name)
            return True
        except DartParseError:
            return False

    def enum_values(self, enum):
        """enum X { a(args), b; const X(...)} -> {name: fields dict}."""
        m = re.search(r'\benum\s+' + re.escape(enum) + r'\s*\{', self.code)
        if not m:
            raise DartParseError('%s: enum %s not found' % (self.name, enum))
        i = self.tok_at(m.end() - 1) + 1
        spec = self.reg.ctors.get(enum)
        out = {}
        while True:
            t = self.toks[i]
            if t.kind == 'op' and t.val in (';', '}'):
                break
            if t.kind != 'id':
                raise self.err(t, 'bad enum entry')
            name = t.val
            i += 1
            if self.toks[i].val == '(':
                p = Parser(self, self.toks, i)
                args, named = p.call_args()
                i = p.i
                if spec is None:
                    raise self.err(t, 'enum %s has args but no ctor' % enum)
                out[name] = spec.build(args, named, '%s:%s' % (self.name, name))
            else:
                out[name] = spec.build([], {}, name) if spec else {}
            if self.toks[i].val == ',':
                i += 1
        return out

    def switch_after(self, anchor_regex):
        m = re.search(anchor_regex, self.code)
        if not m:
            raise DartParseError('%s: anchor %r not found' % (self.name, anchor_regex))
        i = self.tok_at(m.end())
        while not (self.toks[i].kind == 'id' and self.toks[i].val == 'switch'):
            i += 1
        p = Parser(self, self.toks, i)
        return p.expr()

    def body_of(self, anchor_regex):
        """Comment-stripped code of the {...} block following anchor (skipping a
        parameter list that the anchor opened or that follows it)."""
        m = re.search(anchor_regex, self.code)
        if not m:
            raise DartParseError('%s: anchor %r not found' % (self.name, anchor_regex))
        depth = m.group(0).count('(') - m.group(0).count(')')
        i = self.tok_at(m.end())
        if m.group(0).rstrip().endswith('{'):
            i = self.tok_at(m.start() + m.group(0).rstrip().rindex('{'))
        while True:
            t = self.toks[i]
            if t.kind == 'op' and t.val == '(':
                depth += 1
            elif t.kind == 'op' and t.val == ')':
                depth -= 1
            elif t.kind == 'op' and t.val == '{' and depth == 0:
                break
            i += 1
        a = self.toks[i].pos
        b = self.matching(a)
        return self.code[a:b + 1], a

    def static_consts(self, class_name=None, start=0, end=None):
        """All `static const` declarations (in a class) with values and comments."""
        if class_name:
            m = re.search(r'\b(?:class|enum)\s+' + re.escape(class_name) + r'\b[^{]*\{', self.code)
            if not m:
                raise DartParseError('%s: class %s not found' % (self.name, class_name))
            start = m.end()
            end = self.matching(m.end() - 1)
        end = len(self.code) if end is None else end
        out = []
        section = ''
        last_line = 0
        for m in re.finditer(r'(?:^|\n)([ \t]*)static\s+const\s+', self.code[start:end]):
            pos = start + m.end()
            i = self.tok_at(pos)
            # optional type then name =
            while True:
                j = i
                # find "name =" at depth 0
                depth = 0
                while True:
                    t = self.toks[j]
                    if t.kind == 'op' and t.val in ('<', '('):
                        depth += 1
                    elif t.kind == 'op' and t.val in ('>', ')'):
                        depth -= 1
                    elif depth == 0 and t.kind == 'id' and self.toks[j + 1].val == '=':
                        break
                    j += 1
                name = self.toks[j].val
                typ = self.code[self.toks[i].pos:self.toks[j].pos].strip() if j > i else ''
                p = Parser(self, self.toks, j + 2)
                val = p.expr()
                ln = self.line_of(self.toks[j].pos)
                out.append({'name': name, 'type': typ or None, 'value': val, 'line': ln,
                            'comment': self.comment_for(ln)})
                if p.peek().val == ',':
                    i = p.i + 1
                    continue
                break
        return out

    def comment_for(self, ln):
        """Trailing comment on line ln (1-based) + contiguous comment lines right above."""
        trail = trailing_comment(self.lines[ln - 1])
        above = []
        k = ln - 2
        while k >= 0 and self.lines[k].strip().startswith('//'):
            above.insert(0, self.lines[k].strip().lstrip('/').strip())
            k -= 1
        parts = [x for x in [' '.join(above), trail] if x]
        return ' | '.join(parts) if parts else ''

    def section_comments(self, a, b):
        """[(line, text)] of standalone comment lines between offsets a..b."""
        la, lb = self.line_of(a), self.line_of(b)
        out = []
        for ln in range(la, lb + 1):
            s = self.lines[ln - 1].strip()
            if s.startswith('//'):
                out.append((ln, s.lstrip('/').strip()))
        return out


class Registry:
    def __init__(self):
        self.files = {}
        self.ctors = {}
        self.enums = set()
        self.enum_file = {}
        self.extra_env = {}  # name -> (file) for cross-file constant refs

    def lookup(self, name, here):
        if here.has_decl(name):
            return here.const(name)
        for f in self.files.values():
            if f is not here and not name.startswith('_') and f.has_decl(name):
                return f.const(name)
        return None


class Parser:
    def __init__(self, f, toks, i=0):
        self.f = f
        self.toks = toks
        self.i = i
        self.end = len(toks)

    def peek(self, k=0):
        j = self.i + k
        if j >= self.end:
            return Tok('eof', None, self.toks[-1].end if self.toks else 0, 0)
        return self.toks[j]

    def next(self):
        t = self.peek()
        self.i += 1
        return t

    def expect(self, val):
        t = self.next()
        if t.val != val:
            raise self.f.err(t, 'expected %r, got %r' % (val, t.val))
        return t

    def expect_end(self):
        if self.i < self.end:
            raise self.f.err(self.peek(), 'trailing tokens')

    def at(self, val):
        return self.peek().kind in ('op', 'id') and self.peek().val == val

    # -- expressions ----------------------------------------------------------
    def expr(self):
        start = self.i
        try:
            cond = self.binary(0)
        except DartParseError:
            q = self._find_ternary_q(start)
            if q is None:
                raise
            self.i = q
            cond = None
        if self.at('?'):
            cond_src = self.f.code[self.toks[start].pos:self.toks[self.i - 1].end].strip()
            self.next()
            a = self.expr()
            self.expect(':')
            b = self.expr()
            return {'if': ' '.join(cond_src.split()), 'then': a, 'else': b}
        return cond

    def _find_ternary_q(self, start):
        depth = 0
        for j in range(start, self.end):
            t = self.toks[j]
            if t.kind != 'op':
                continue
            if t.val in '([{':
                depth += 1
            elif t.val in ')]}':
                if depth == 0:
                    return None
                depth -= 1
            elif depth == 0 and t.val in (',', ';', '=>', ':'):
                return None
            elif depth == 0 and t.val == '?':
                return j
        return None

    _PREC = [('||',), ('&&',), ('==', '!='), ('<', '>', '<=', '>='), ('??',), ('+', '-'), ('*', '/', '%', '~/')]

    def binary(self, lvl):
        if lvl >= len(self._PREC):
            return self.unary()
        left = self.binary(lvl + 1)
        while self.peek().kind == 'op' and self.peek().val in self._PREC[lvl]:
            op = self.next()
            right = self.binary(lvl + 1)
            left = self._arith(op, left, right)
        return left

    def _arith(self, op, a, b):
        num = (int, float)
        if op.val in '+-*/' and isinstance(a, num) and isinstance(b, num) and not isinstance(a, bool):
            return {'+': a + b, '-': a - b, '*': a * b, '/': a / b}[op.val]
        if op.val == '+' and isinstance(a, str) and isinstance(b, str):
            return a + b
        raise self.f.err(op, 'cannot evaluate operator %s' % op.val)

    def unary(self):
        t = self.peek()
        if t.val == '-' and t.kind == 'op':
            self.next()
            v = self.unary()
            if not isinstance(v, (int, float)):
                raise self.f.err(t, 'unary minus on non-number')
            return -v
        return self.primary()

    def primary(self):
        t = self.peek()
        if t.kind == 'id' and t.val in ('const', 'final', 'new'):
            self.next()
            return self.primary()
        if t.kind == 'str':
            s = ''
            while self.peek().kind == 'str':
                s += self.next().val
            return s
        if t.kind == 'num':
            return self.next().val
        if t.kind == 'op':
            if t.val == '<':
                self.skip_typeargs()
                return self.primary()
            if t.val == '[':
                return self.list_lit()
            if t.val == '{':
                return self.brace_lit()
            if t.val == '(':
                return self.paren()
            raise self.f.err(t, 'unexpected %r' % t.val)
        if t.kind == 'id':
            if t.val == 'true':
                self.next()
                return True
            if t.val == 'false':
                self.next()
                return False
            if t.val == 'null':
                self.next()
                return None
            if t.val == 'switch':
                return self.switch_expr()
            return self.ident()
        raise self.f.err(t, 'unexpected end of input')

    def skip_typeargs(self):
        depth = 0
        while True:
            t = self.next()
            if t.val == '<':
                depth += 1
            elif t.val == '>':
                depth -= 1
                if depth == 0:
                    return
            elif t.kind == 'eof':
                raise self.f.err(t, 'unterminated type args')

    def looks_typeargs(self):
        if not self.at('<'):
            return False
        depth = 0
        j = self.i
        while j < self.end:
            t = self.toks[j]
            if t.val == '<':
                depth += 1
            elif t.val == '>':
                depth -= 1
                if depth == 0:
                    nxt = self.toks[j + 1] if j + 1 < self.end else None
                    return nxt is not None and nxt.val in ('(', '[', '{')
            elif not (t.kind == 'id' or t.val in (',', '?', '(', ')', '.')):
                return False
            j += 1
        return False

    def ident(self):
        t = self.next()
        parts = [t.val]
        while self.at('.') and self.peek(1).kind == 'id':
            self.next()
            parts.append(self.next().val)
        if self.looks_typeargs():
            self.skip_typeargs()
        name = '.'.join(parts)
        if self.at('('):
            args, named = self.call_args()
            return self.call(t, parts, args, named)
        if len(parts) == 2 and parts[0] in self.f.reg.enums:
            return parts[1]
        if name == 'double.infinity':
            return None
        if len(parts) == 1:
            v = self.f.reg.lookup(name, self.f)
            if v is None and not self.f.has_decl(name):
                raise self.f.err(t, 'unknown identifier %s' % name)
            return v
        raise self.f.err(t, 'cannot resolve %s' % name)

    def call(self, t, parts, args, named):
        name = parts[-1] if len(parts) == 1 else '.'.join(parts)
        if name == 'Duration':
            return duration(args, named)
        if name in self.f.reg.ctors:
            return self.f.reg.ctors[name].build(args, named, '%s:%d' % (self.f.name, self.f.line_of(t.pos)))
        raise self.f.err(t, 'unknown constructor/function %s()' % name)

    def call_args(self):
        self.expect('(')
        args, named = [], {}
        while not self.at(')'):
            if self.peek().kind == 'id' and self.peek(1).val == ':' :
                k = self.next().val
                self.next()
                named[k] = self.expr()
            else:
                args.append(self.expr())
            if not self.at(')'):
                self.expect(',')
        self.expect(')')
        return args, named

    def list_lit(self):
        self.expect('[')
        out = []
        while not self.at(']'):
            if self.at('...') or self.at('...?'):
                self.next()
                v = self.expr()
                if v is None:
                    v = []
                if not isinstance(v, list):
                    raise self.f.err(self.peek(), 'spread of non-list')
                out.extend(v)
            elif self.at('for') or self.at('if'):
                raise self.f.err(self.peek(), 'collection for/if not supported')
            else:
                out.append(self.expr())
            if not self.at(']'):
                self.expect(',')
        self.expect(']')
        return out

    def brace_lit(self):
        start = self.expect('{')
        items, is_map = [], None
        while not self.at('}'):
            if self.at('...') or self.at('...?'):
                self.next()
                v = self.expr()
                if v is None:
                    v = []
                items.append(('spread', v))
            elif self.at('for') or self.at('if'):
                raise self.f.err(self.peek(), 'collection for/if not supported')
            else:
                k = self.expr()
                if self.at(':'):
                    self.next()
                    v = self.expr()
                    if is_map is False:
                        raise self.f.err(start, 'mixed set/map literal')
                    is_map = True
                    items.append(('kv', k, v))
                else:
                    if is_map:
                        raise self.f.err(start, 'mixed set/map literal')
                    is_map = False
                    items.append(('el', k))
            if not self.at('}'):
                self.expect(',')
        self.expect('}')
        if is_map is False or (is_map is None and items and all(x[0] == 'spread' and isinstance(x[1], list) for x in items)):
            out = DartSet()
            for it in items:
                vals = it[1] if it[0] == 'spread' else [it[1]]
                for v in vals:
                    if v not in out:
                        out.append(v)
            return out
        out = {}
        for it in items:
            if it[0] == 'spread':
                if not isinstance(it[1], dict):
                    raise self.f.err(start, 'map spread of non-map')
                out.update(it[1])
            else:
                k = it[1]
                if isinstance(k, (dict, list)):
                    raise self.f.err(start, 'unhashable map key')
                out[k] = it[2]
        return out

    def paren(self):
        self.expect('(')
        vals, named, trailing = [], {}, False
        while not self.at(')'):
            if self.peek().kind == 'id' and self.peek(1).val == ':':
                k = self.next().val
                self.next()
                named[k] = self.expr()
            else:
                vals.append(self.expr())
            trailing = False
            if not self.at(')'):
                self.expect(',')
                trailing = True
        self.expect(')')
        if len(vals) == 1 and not named and not trailing:
            return vals[0]
        if named:
            d = {'$%d' % (k + 1): v for k, v in enumerate(vals)}
            d.update(named)
            return d
        return list(vals)

    def switch_expr(self):
        self.expect('switch')
        a = self.peek()
        self.expect('(')
        depth = 1
        while depth:
            t = self.next()
            if t.val == '(':
                depth += 1
            elif t.val == ')':
                depth -= 1
        subj = self.f.code[a.end:self.toks[self.i - 1].pos].strip()
        self.expect('{')
        cases = {}
        while not self.at('}'):
            pats = [self.pattern()]
            while self.at('||'):
                self.next()
                pats.append(self.pattern())
            self.expect('=>')
            v = self.expr()
            for p in pats:
                cases[p] = v
            if not self.at('}'):
                self.expect(',')
        self.expect('}')
        return {'switch': subj, 'cases': cases}

    def pattern(self):
        t = self.next()
        if t.kind == 'str':
            return t.val
        if t.kind == 'num':
            return t.val
        if t.kind == 'id' and t.val == '_':
            return '_default'
        if t.kind == 'id' and t.val == 'null':
            return 'null'
        if t.kind == 'id' and self.at('.'):
            self.next()
            n = self.next()
            if t.val not in self.f.reg.enums:
                raise self.f.err(t, 'pattern on unknown enum %s' % t.val)
            return n.val
        raise self.f.err(t, 'unsupported switch pattern')
