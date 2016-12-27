import sys ;

capcalera = """<?xml version='1.0' encoding='UTF-8' ?>
<corpus>
""" ; 

print(capcalera);
scount = 0;
lcount = 0;
ccount = 0;

deps = {}; 
nodes = {};

def escape(s): #{
        o = s;
        o = o.replace('"', '&#34;');
        o = o.replace("'", '&quot;');
        o = o.replace("&", '&amp;');
        return o;
#}

def proc(depth, nodes, deps, node): #{
        depth = depth + 1;
        if node != 0: #{
                form = escape(nodes[node][1]);
                lem = escape(nodes[node][2]);
                mi = '_';
                if nodes[node][4] != '_': #{
                        mi = nodes[node][4] + '|' + nodes[node][5];
                elif nodes[node][3] != '_': #{
                        mi = nodes[node][3] + '|' + nodes[node][5];
                #}
                mi = mi.replace('|_', '').replace('<', '[').replace('>', ']');
                si = nodes[node][7].replace('>', '→').replace('<', '←');
                if node in deps and len(deps[node]) > 0: #{
                        print(' ' * (2 * depth), '<NODE ord="%d" alloc="%d" form="%s" lem="%s" mi="%s" si="%s">' % (node, 0, form, lem, mi, si) );
                else: #{
                        print(' ' * (2 * depth), '<NODE ord="%d" alloc="%d" form="%s" lem="%s" mi="%s" si="%s"/>' % (node, 0, form, lem, mi, si) );
                #}
        #}
        if node in deps: #{
                for n in deps[node]: #{
                        proc(depth, nodes, deps, n);
                #}
        else: #{
                return;
        #}
        if node != 0: #{
                print(' ' * (2 * depth), '</NODE>');
        #}
        depth = depth - 1;
        return ;
#}
open = 0;
ord = 0;
for line in sys.stdin.readlines(): #{
        line = line.strip('\n');
        if line.count('# ord:') > 0: #{
                line = line.replace('\t_', '\t');
                ord = int(line.split('ord:')[1].strip().split(' ')[0].strip());
        elif line == '\n': #{
                ord = 0;
        #}
        if line.count('\t') > 1 and line[0] != '#': #{
                row = line.split('\t');
                if row[0] == '1': #{
                        scount = scount + 1;
                        print('<SENTENCE ord="%d" alloc="%d">' % (ord, ccount)) ;
                        open = 1;
                #}
                if row[0].count('-') > 0: #{
                        continue;
                #}
                cur = int(row[0]);
                cap = int(row[6]);
                if cap not in deps: #{
                        deps[cap] = [];
                #}
                deps[cap].append(cur);
                nodes[cur] = row; 
        #}
        if line.strip() == '' and open == 1: #{
                proc(0, nodes, deps, 0); 
                print('</SENTENCE>');
                open = 0;
                deps = {};
                nodes = {};
        #}
#}

print('</corpus>');
