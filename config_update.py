import sys, os, re, os.path, shutil, json
from copy import deepcopy
import argparse, sys
import jsondiff as jd
from lxml import etree

parser=argparse.ArgumentParser()
parser.add_argument('--current', help='Current cofig folder path')
parser.add_argument('--new', help='New config folder path')
parser.add_argument('--output', help='output folder')
parser.add_argument('--inside', help='output folder')
args = parser.parse_args()


TO_PROCESS = ['.xml', '.json', '.properties', '.conf', '.cfg']
TAG_ATTR = [{'tag': 'var', 'new': 'dif', 'current': 'admi-dif', 'attrib': 'val'},
]
OLD_VAL_TO_BE_FOLDERS = ['pmd.d']


current_folder = args.current
new_folder = args.new
output_folder = args.output

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


current_files = [i for i in os.listdir(current_folder) if not os.path.isdir(os.path.join(current_folder, i))] \
                if os.path.exists(current_folder) else []
new_files = [i for i in os.listdir(new_folder) if not os.path.isdir(os.path.join(new_folder, i))] \
            if os.path.exists(new_folder) else []

for i in new_files:
    filename, file_extension = os.path.splitext(i)
    if not file_extension in TO_PROCESS:
        os.system("cp -Rf " + new_folder + "/" + i + " " + output_folder)

current_folders = [i for i in os.listdir(current_folder) if os.path.isdir(os.path.join(current_folder, i))] \
                    if os.path.exists(current_folder) else []
new_folders = [i for i in os.listdir(new_folder) if os.path.isdir(os.path.join(new_folder, i))] \
                if os.path.exists(new_folder) else []
for i in new_folders:
    os.system("python3 %s --current=%s --new=%s --output=%s --inside=%s" % (
            sys.argv[0],
            os.path.join(current_folder, i),
            os.path.join(new_folder, i),
            os.path.join(output_folder, i),
            True
        )
    )



# print("CURRENT_FILES:", current_files)
# print("NEW_FILES:", new_files)


def json_process(current_file_path, new_file_path, output_file_path):
    with open(current_file_path) as f1:
        with open(new_file_path) as f2:
            data = jd.patch(json.loads(f2.read()), json.loads(f1.read()))
            with open(output_file_path, 'w') as f3:
                f3.write(json.dumps(data, indent=4))

def xml_process(current_file_path, new_file_path, output_file_path):
    new_tree = etree.parse(new_file_path)
    old_tree = etree.parse(current_file_path)
    new_tree_root = new_tree.getroot()
    old_tree_root = old_tree.getroot()

    #etree.dump(new_tree_root)

    TO_DELETE = []
    TO_VERIFY = []
    def get_childs(node):
        #print(node)
        if node.getchildren():
            #print(len(node.getchildren()))
            xpath = new_tree.getelementpath(node)
            #print(len(old_tree.findall(xpath)))
            for i in node.getchildren():
                #print(i, "1111")
                try:
                    get_childs(i)
                except Exception as e:
                    import traceback; print(traceback.format_exc())
                    print(e)
        else:

            if node.__class__ is etree._Comment:
                
                return

            xpath = new_tree.getelementpath(node)

            if "}address" in xpath or "}member" in xpath:
                if not node.getparent() in TO_VERIFY:
                    TO_VERIFY.append(node.getparent())

            items = old_tree.findall(xpath)
            new_items = new_tree.findall(xpath)

            if len(new_items) < len(items):
                for k in items[len(new_items):]:
                    if not any([re.search(i, k.text or "") for i in ['locahost', '127.0.0.1', '\\w+:\\d+']]):
                        continue
                    print("INSERT")
                    node.getparent().insert(len(node.getparent().getchildren()) + 1, deepcopy(k))
            elif len(new_items) > len(items):
                if len(set([i.tag for i in new_items + items])) == 1:
                    TO_DELETE.append((node.getparent(), len(new_items) - len(items)))
            items = old_tree.findall(xpath)
            for item in items:
                if item is not None and item.text:
                    new_tree.find(xpath).text = item.text
                #HARDCODED SUPPORT
                for i in TAG_ATTR:
                    if i['tag'] == item.tag or "}%s" % i['tag'] in item.tag:
                        if i['attrib'] in item.attrib:
                            if i['current'] == item.attrib[i['attrib']]:
                                print("TAG_UPDATE: %s" % (i))
                                new_tree.find(xpath).attrib.update({i['attrib']: i['current']})
                try:
                    if 'var' in item.attrib and 'val' in item.attrib and \
                    any([k in new_file_path for k in OLD_VAL_TO_BE_FOLDERS]):
                        #import pdb; pdb.set_trace()
                        #print(xpath)
                        if isinstance(xpath, str) and "[" in xpath and "]" in xpath:
                            for i in range(10):
                                for k in range(10):
                                    old_xpath = re.sub('\\[.*\\]', '[%s]' % i, xpath)
                                    new_xpath = re.sub('\\[.*\\]', '[%s]' % k, xpath)
                                    try:
                                        if new_tree.find(new_xpath).attrib['var'] == old_tree.find(old_xpath).attrib['var']:
                                            new_tree.find(new_xpath).attrib.update(
                                                {
                                                    'val': old_tree.find(old_xpath).attrib['val']
                                                }
                                            )                                            
                                    except Exception as e:
                                        pass
                        elif isinstance(xpath, str):
                            new_xpath = xpath
                            for i in range(10):
                                old_xpath = xpath + '[%s]' % i
                                try:
                                    if new_tree.find(new_xpath).attrib['var'] == old_tree.find(old_xpath).attrib['var']:
                                        new_tree.find(new_xpath).attrib.update(
                                            {
                                                'val': old_tree.find(old_xpath).attrib['val']
                                            }
                                        )                                            
                                except Exception as e:
                                    pass
                        elif new_tree.find(xpath).attrib['var'] == old_tree.find(xpath).attrib['var']:
                            new_tree.find(xpath).attrib.update(
                                {
                                    'val': old_tree.find(xpath).attrib['val']
                                }
                            )


                except Exception as e:
                    print(e)
                            
                    #print("REPLACE DONE")
        return

    get_childs(new_tree_root) 
    # for i,j in TO_DELETE:
    #     for k in range(j):
    #         i.remove(i.getchildren()[-1])



    if TO_VERIFY:
        print("TO_VERIFY: ", TO_VERIFY)
    for i in TO_VERIFY:
        execute = True
        n_xpath = new_tree.getelementpath(i)

        items = [k for k in old_tree.find(n_xpath).getchildren() if not k.__class__ is etree._Comment]
        new_items = [k for k in new_tree.find(n_xpath).getchildren() if not k.__class__ is etree._Comment]
        if items and new_items:
            if "}address" in str(items[0].tag):
                for j in items:
                    if not "}address" in str(j.tag):
                        execute = False
                for k in new_items:
                    if not "}member" in str(k.tag):
                        execute = False
            if "}member" in str(items[0].tag):
                for j in items:
                    if not "}member" in str(j.tag):
                        execute = False
                for k in new_items:
                    if not "}address" in str(k.tag):
                        execute = False

        # if not execute:
        #     continue
        while new_tree.find(n_xpath).getchildren():
            #print(new_tree.find(n_xpath).getchildren()[0])
            new_tree.find(n_xpath).remove(new_tree.find(n_xpath).getchildren()[0])
        for i in items:
            i.tag = ("address" if "}member" in i.tag else "member") if execute else i.tag
            new_tree.find(n_xpath).append(i)
    
    with open(new_file_path) as f:
        lines = f.read().split("\n")
    to_add = []
    for i in lines:
        if etree.tostring(new_tree_root, xml_declaration=False).startswith(i.strip()[:4].encode()):
            break
        else:
            to_add.append(i)


    #dom = xml.dom.minidom.parseString(etree.tostring(new_tree_root, xml_declaration=True))
    #pretty_xml_as_string = dom.toprettyxml()
    with open(output_file_path, 'wb') as f3:
        #with open(os.path.join(args.new, file_name)) as orig:
            #lines = [i for i in orig.readlines()]
            # f3.write(os.linesep.join([s for s in pretty_xml_as_string.splitlines()
            #                               if s.strip()]))
        # f3.write(etree.tostring(new_tree_root, xml_declaration=False if new_tree.docinfo.standalone is None else True, 
        #     pretty_print=True, encoding=new_tree.docinfo.encoding))

        if to_add:
            for i in to_add:
                f3.write(i.encode() + b"\n")
        f3.write(etree.tostring(new_tree_root, xml_declaration=False))



def index(s, c):
    try:
        return s.index(c)
    except: return 1000

def conf_process(current_file_path, new_file_path, output_file_path):
    key_values_current = {}
    with open(current_file_path) as f1:
        lines_1 = []
        whole_data = f1.readlines()
        for i in whole_data:
            if i.strip().startswith('#') or not i.strip():
                lines_1.append(i.strip())

            else:
                if ":" in i or "=" in i:
                    seperator = ":" if index(i, ":") < index(i, "=") else "="
                    lines_1.append([j.strip() for j in i.strip().split(seperator)] + [seperator])
                    if lines_1[-1][0] in key_values_current:
                        key_values_current[lines_1[-1][0]] += "--|--" + lines_1[-1][1]
                    else:
                        key_values_current[lines_1[-1][0]] = lines_1[-1][1]
                else:
                    lines_1.append(i.strip())

    key_values_new = {}
    with open(new_file_path) as f2:
        whole_data_new = f2.read()
        if "".join(whole_data_new).count(":") > "".join(whole_data_new).count("="):
            g_seperator = ":"
        else:
            g_seperator = "="
        whole_data = whole_data_new.split("\n")
        lines_2 = []  
        for i in whole_data:
            if i.strip().startswith('#') or not i.strip():
                lines_2.append(i.strip())
            else:
                if ":" in i or "=" in i:
                    seperator = ":" if index(i, ":") < index(i, "=") else "="
                    lines_2.append([j.strip() for j in i.strip().split(seperator)] + [seperator])
                    if lines_2[-1][0] in key_values_new:
                        key_values_new[lines_2[-1][0]] += "--|--" + lines_2[-1][1]
                    else:
                        key_values_new[lines_2[-1][0]] = lines_2[-1][1]
                else:
                    lines_2.append(i.strip())

    key_values_current = {i: j.split("--|--") if "--|--" in j else j for i,j in key_values_current.items()}
    key_values_new = {i: j.split("--|--") if "--|--" in j else j for i,j in key_values_new.items()}

    # print(key_values_current)
    # print(key_values_new)



    to_add = []
    to_verify = []
    to_write = []
    with open(output_file_path, 'w') as f3:
        for i in lines_2:
            if isinstance(i, list):
                if i[0] in key_values_current:
                    if isinstance(key_values_current[i[0]], list):
                        if key_values_current[i[0]]:
                            to_verify.append(i[0])
                            to_write.append([i[0], ("%s%s%s" % (i[0], i[2], key_values_current[i[0]].pop(0)))])
                    else:
                        to_write.append([i[0], ("%s%s%s" % (i[0], i[2], key_values_current[i[0]]))])
                else:
                    #to_add.append(i)
                    to_write.append([i[0], ("%s%s%s" % (i[0], i[2], i[1]))])
            else:
                to_write.append(i)
            #f3.write("\n")
        #print(to_verify)

        added = set()
        for item in to_write:
            if isinstance(item, list):
                if item[1] in added:
                    continue
                added.add(item[1])
                f3.write(item[1])
                f3.write("\n")
                if item[0] in to_verify:
                    while key_values_current[item[0]]:
                        f3.write("%s%s%s" % (item[0], g_seperator, key_values_current[item[0]].pop(0)))
                        f3.write("\n")
            else:
                f3.write(item)
                f3.write("\n")
        return
        for i in to_verify:
            while key_values_current[i]:
                f3.write("%s%s%s" % (i, g_seperator, key_values_current[i].pop(0)))
                f3.write("\n")
        # if to_add:
        #     #f3.write("\n\n\n################ CONFIGS ADDED ################\n\n")
        #     for i in to_add:
        #         f3.write("%s%s%s" % (i[0], i[2], i[1]))
        #         f3.write("\n")
        #     #f3.write("\n\n\n################ CONFIGS ADDED ################\n\n")
        return


for i in new_files:
    # if not "admi-dif." in i:
    #     continue
    new_file_path = os.path.join(new_folder, i)
    current_file_path = os.path.join(current_folder, i)
    output_file_path = os.path.join(output_folder, i)
    print("PROCESSING %s" % new_file_path)
    filename, file_extension = os.path.splitext(i)
    if not file_extension in TO_PROCESS:
        print("TO_PROCESS: NOT PRESENT : %s" % i)
        continue
    if not os.path.exists(current_file_path):
        os.system("cp -Rf " + new_file_path + " " + output_folder)
        print("CURRENT_FOLDER : NOT PRESENT : %s" % i)
        continue

    if file_extension == '.json':
        json_process(current_file_path, new_file_path, output_file_path)
        continue
    if file_extension == '.xml':
        xml_process(current_file_path, new_file_path, output_file_path)
        continue
    if file_extension in ['.properties', '.conf', '.cfg']:
        conf_process(current_file_path, new_file_path, output_file_path)
        continue

if os.path.exists(current_folder):
    for i in os.listdir(current_folder):
        if not os.path.exists(os.path.join(output_folder, i)):
            from distutils.dir_util import copy_tree
            if os.path.isdir(os.path.join(current_folder, i)):
                copy_tree(os.path.join(current_folder, i), os.path.join(output_folder, i))
            else:
                if args.inside:
                    os.system("cp " + os.path.join(current_folder, i) + " " + os.path.join(output_folder, i))






for i in os.listdir(output_folder):
    if i in ['app']:
        os.system("cp " + os.path.join(output_folder, "%s/sig-firewall-SIP*" % i) + " " + os.path.join(output_folder))
        os.system("cp " + os.path.join(output_folder, "%s/sig-firewall-gtp*" % i) + " " + os.path.join(output_folder))
        os.system("cp " + os.path.join(output_folder, "%s/sig-firewall-diam*" % i) + " " + os.path.join(output_folder))




















            
            
