import json
import os
import argparse
import configparser
import xml.etree.ElementTree as ET
import re

# parser = argparse.ArgumentParser()
# parser.add_argument("new_dir", help="provide path of new directory")
# parser.add_argument("old_dir", help="provide path of old directory")
# parser.add_argument("output_dir", help="provide path of output directory")
# args = parser.parse_args()

class Constants:
    
    start_attribute="target/"
    repetition_tag="address"
    hazel_1="hazelcast"
    hazel_2="hazelcast-client"
    

class Validator:

    def __init__(self, new_dir, old_dir, output_dir):
        self.new_dir = new_dir
        self.old_dir = old_dir
        self.output_dir = output_dir
        self.start_validation()

    def start_validation(self):
        for each_file in os.listdir(self.output_dir):
            # print("line---31", each_file)
            output_full_path = os.path.join(os.getcwd(), self.output_dir, each_file)
            new_full_path = os.path.join(os.getcwd(), self.new_dir, each_file)
            old_full_path = os.path.join(os.getcwd(), self.old_dir, each_file)
            if not os.path.isdir(output_full_path):
                if os.path.exists(new_full_path) and os.path.exists(old_full_path):
                    # if output_full_path.endswith(".json"):
                        # if not self.process_json(new_json=new_full_path,
                        #                          old_json=old_full_path,
                    #                              output_json=output_full_path):
                    #         print(f"{each_file} is invalid")
                    #         return False
                    # elif output_full_path.endswith(".txt"):
                    #     print("yet to implement .txt file validation")
                    # elif output_full_path.endswith(".conf"):
                    #     if not self.process_conf(new_prop=new_full_path,
                    #                              old_prop=old_full_path,
                    #                              output_prop=output_full_path):
                    #         print(f"{self.output_dir}->{each_file} is invalid")
                    #         return False
                    # elif output_full_path.endswith(".cfg"):
                    #     # print("yet to implement .cfg file validation")
                    #     # print(f"===processing {self.output_dir}->{each_file}")
                    #     if not self.process_conf(new_prop=new_full_path,
                    #                              old_prop=old_full_path,
                    #                              output_prop=output_full_path):
                    #         print(f"{self.output_dir}->{each_file} is invalid")
                    #         return False
                    if output_full_path.endswith(".xml"):
                        print(f"opened file is :{each_file}")
                        value= Validator.read_xml_comments(new_xml=new_full_path,output_xml=output_full_path)
                        
                        if not self.process_xml(new_xml=new_full_path,
                                                old_xml=old_full_path,
                                                output_xml=output_full_path) or not value:
                            print(f"{self.output_dir}->{each_file} is invalid")
                            print("_____________________________")
                            return False
                        
                #     elif output_full_path.endswith(".properties"):
                #         if not self.process_properties(new_prop=new_full_path,
                #                                        old_prop==old_full_path,
                #                                        output_prop=output_full_path):
                #             print(f"{self.output_dir}->{each_file} is invalid")
                #             return False
                # elif os.path.exists(new_full_path) and not os.path.exists(old_full_path):
                #     continue
                # elif not os.path.exists(new_full_path) and os.path.exists(old_full_path):
                #     print(f"Warning: {each_file} file is only present in old folder. "
                #           f"Yet to implement logic to validate such files.")
                #     return False
            else:
                if os.path.exists(new_full_path) and os.path.exists(old_full_path):
                    if not Validator(new_dir=new_full_path,
                                     old_dir=old_full_path,
                                     output_dir=output_full_path):
                        return False
                elif any([os.path.exists(new_full_path), os.path.exists(old_full_path)]):
                    print("Warning: Yet to implement logic to validate non common files.")
                elif not all([os.path.exists(new_full_path), os.path.exists(old_full_path)]):
                    print(f"{each_file} is not present in new and old folder.it should not be present in output folder")
                    return False

    # def process_conf(self, new_prop: str, old_prop: str, output_prop: str) -> bool:
    #     with open(os.path.join(self.new_dir, new_prop)) as f_obj:
    #         new_comment_dict, new_data_dict = self.prepare_conf_data(file_obj=f_obj)
    #     with open(os.path.join(self.old_dir, old_prop)) as f_obj:
    #         old_comment_dict, old_data_dict = self.prepare_conf_data(file_obj=f_obj)
    #     with open(os.path.join(self.output_dir, output_prop)) as f_obj:
    #         output_comment_dict, output_data_dict = self.prepare_conf_data(file_obj=f_obj)
    #     input_args = {"new_data_dict": new_data_dict, "new_comment_dict": new_comment_dict,
    #                   "old_data_dict": old_data_dict, "output_data_dict": output_data_dict,
    #                   "output_comment_dict": output_comment_dict}
    #     return self.validate_conf(**input_args)

    # @staticmethod
    # def prepare_conf_data(file_obj):
    #     comment_dict = {}
    #     data_dict = {}
    #     for line_num, each_line in enumerate(file_obj.readlines()):
    #         each_line = each_line.strip()
    #         if len(each_line) == 0:
    #             continue
    #         if each_line.startswith("#"):
    #             if comment_dict.get(each_line, False):
    #                 comment_dict[each_line] += 1
    #             else:
    #                 comment_dict[each_line] = 1
    #         else:
    #             if len(each_line) > 0 and "=" in each_line:
    #                 temp_sep = "="
    #             elif len(each_line) > 0 and ":" in each_line:
    #                 temp_sep = ":"
    #             else:
    #                 continue
    #             each_line = each_line.split(temp_sep)
    #             temp_key = each_line[0].strip()
    #             temp_val = [each_line[1].strip(), temp_sep]
    #             if data_dict.get(temp_key, False):
    #                 data_dict[temp_key].append(temp_val)
    #             else:
    #                 data_dict[temp_key] = [temp_val]
    #     return comment_dict, data_dict

    # @staticmethod
    # def validate_conf(**kwargs) -> bool:
    #     new_data_dict = kwargs.get("new_data_dict", {})
    #     new_comment_dict = kwargs.get("new_comment_dict", {})
    #     old_data_dict = kwargs.get("old_data_dict", {})
    #     output_data_dict = kwargs.get("output_data_dict", {})
    #     output_comment_dict = kwargs.get("output_comment_dict", {})
    #     for key, val in new_comment_dict.items():
    #         if output_comment_dict.get(key, False) != val:
    #             print(f"Error: The comment '{key}' is missing or unaligned in output file.")
    #             return False
    #     for key, val in output_comment_dict.items():
    #         if new_comment_dict.get(key, False) != val:
    #             print(f"Error: The comment '{key}' is not taken from new file.")
    #             return False
    #     for key, val in new_data_dict.items():
    #         if not output_data_dict.get(key, False):
    #             print(f"Error: The key {key} is missing in output file")
    #             return False
    #         output_val = output_data_dict[key]
    #         if old_data_dict.get(key):
    #             old_val = old_data_dict[key]
    #             old_val = [i[0] for i in old_val]
    #             old_len = len(old_val)
    #             output_sep = [i[1] for i in output_val]
    #             output_val = [i[0] for i in output_val]
    #             new_sep = [i[1] for i in val]
    #             new_val = [i[0] for i in val]
    #             # if not all([old_val == output_val[:old_len],
    #             #             new_sep == output_sep,
    #             #             output_val[old_len:] == new_val[old_len:]]):
    #             if len(output_val) < old_len or len(output_val) != len(new_val) or not all([old_val == output_val[:old_len]]) or (new_sep != output_sep) :
    #                 print(f"Error: The key {key} is present in both new and old file. "
    #                       f"but, either the value is not taken from old file "
    #                       f"or the separator is not from new file.")
    #                 return False
    #         else:
    #             if output_val != val:
    #                 print(f"Error: The key {key} is only present in new folder. "
    #                       f"Thus, its value should also match with new file!!")
    #                 return False
    #     return True

    # def process_properties(self, new_prop: str, old_prop: str, output_prop: str) -> bool:
    #     old_data_dict = {}
    #     with open(os.path.join(self.new_dir, new_prop)) as f_obj:
    #         new_comment_dict, new_data_dict = self.prepare_new_or_output_prop_data(file_obj=f_obj)
    #     with open(os.path.join(self.old_dir, old_prop)) as f_obj:
    #         for line_num, each_line in enumerate(f_obj.readlines()):
    #             each_line = each_line.strip()
    #             if len(each_line) > 0 and not each_line.startswith("#"):
    #                 temp_sep = "=" if "=" in each_line else ":"
    #                 each_line = each_line.split(temp_sep)
    #                 temp_key = each_line[0].strip()
    #                 temp_val = [each_line[1].strip(), temp_sep]
    #                 old_data_dict[temp_key] = temp_val
    #     with open(os.path.join(self.output_dir, output_prop)) as f_obj:
    #         output_comment_dict, output_data_dict = self.prepare_new_or_output_prop_data(file_obj=f_obj)
    #     input_args = {"new_data_dict": new_data_dict, "new_comment_dict": new_comment_dict,
    #                   "old_data_dict": old_data_dict, "output_data_dict": output_data_dict,
    #                   "output_comment_dict": output_comment_dict}
    #     return self.validate_properties(**input_args)

    # @staticmethod
    # def prepare_new_or_output_prop_data(file_obj):
    #     comment_dict = {}
    #     data_dict = {}
    #     for line_num, each_line in enumerate(file_obj.readlines()):
    #         each_line = each_line.strip()
    #         if each_line.startswith("#"):
    #             comment_dict[line_num] = each_line
    #         elif len(each_line) > 0 and "=" in each_line:
    #             each_line = each_line.split("=")
    #             temp_key = each_line[0].strip()
    #             temp_val = [each_line[1].strip(), "="]
    #             data_dict[temp_key] = temp_val
    #         elif len(each_line) > 0 and ":" in each_line:
    #             each_line = each_line.split(":")
    #             temp_key = each_line[0].strip()
    #             temp_val = [each_line[1].strip(), ":"]
    #             data_dict[temp_key] = temp_val
    #     return comment_dict, data_dict

    # @staticmethod
    # def validate_properties(**kwargs) -> bool:
    #     new_data_dict = kwargs.get("new_data_dict", {})
    #     new_comment_dict = kwargs.get("new_comment_dict", {})
    #     old_data_dict = kwargs.get("old_data_dict", {})
    #     output_data_dict = kwargs.get("output_data_dict", {})
    #     output_comment_dict = kwargs.get("output_comment_dict", {})
    #     for key, val in new_comment_dict.items():
    #         if output_comment_dict.get(key, False) != val:
    #             print(f"Error: The comment '{val}' is missing or unaligned in output file.")
    #             return False
    #     for key, val in new_data_dict.items():
    #         if key in output_data_dict and key in old_data_dict:
    #             temp_val = old_data_dict[key][0]
    #             out_val = output_data_dict[key][0]
    #             out_sep = output_data_dict[key][1]
    #             if temp_val != out_val or out_sep != val[1]:
    #                 print(f"Error in {key}: either the value {out_val} is not from old file "
    #                       f"or the separator {out_sep} is not from new file")
    #                 return False
    #         elif key in output_data_dict and key not in old_data_dict:
    #             if output_data_dict[key] != val:
    #                 print(f"Error: The key {key} is only present in new file but it's value doesn't match")
    #                 return False
    #         else:
    #             print(f"Error: Unknown error occurred for {key}, need to debug!!!")
    #             return False
    #     return True

    # def process_json(self, new_json, old_json, output_json):
    #     with open(os.path.join(self.new_dir, new_json)) as f_obj:
    #         new_json = json.load(f_obj)
    #     with open(os.path.join(self.old_dir, old_json)) as f_obj:
    #         old_json = json.load(f_obj)
    #     with open(os.path.join(self.output_dir, output_json)) as f_obj:
    #         output_json = json.load(f_obj)
    #     if new_json and old_json and output_json:
    #         return self.validate_json(new_json=new_json, old_json=old_json, final_json=output_json)

    # @staticmethod
    # def validate_json(new_json: dict, old_json: dict, final_json: dict) -> bool:
    #     for each_key, each_val in new_json.items():
    #         if each_key in final_json:
    #             output_val = final_json.get(each_key, {})
    #             if each_key in old_json:
    #                 old_val = old_json.get(each_key, False)
    #                 if type(each_val) == type(old_val):
    #                     if isinstance(each_val, dict):
    #                         if Validator.validate_json(new_json=each_val, old_json=old_val, final_json=output_val):
    #                             continue
    #                         else:
    #                             return False
    #                     elif isinstance(each_val, list):
    #                         if not Validator.validate_json_list_value(new_list=each_val,
    #                                                                   old_list=old_val,
    #                                                                   final_list=output_val):
    #                             return False
    #                     else:
    #                         # value is either str or int
    #                         if output_val == old_val:
    #                             continue
    #                         else:
    #                             print(f"Error: value of {each_key} should be {old_val} but it is {output_val}")
    #                             return False
    #                 else:
    #                     print(f"Error:{each_key}'s value in output file does not match with old file")
    #                     return False
    #             elif each_val != output_val:
    #                 print(f"Error: value of {each_key} should be {each_val} as "
    #                       f"it is only present in new folder")
    #                 return False
    #         else:
    #             print(f"Error:{each_key} is not present in output json.")
    #             return False

    #     return True

    # @staticmethod
    # def validate_json_list_value(new_list: list, old_list: list, final_list: list):
    #     for each_val in old_list:
    #         if each_val in final_list:
    #             final_val = final_list[final_list.index(each_val)]
    #         else:
    #             print(f"Error:{each_val} is not taken from old folder.")
    #             return False

    #         if each_val in new_list:
    #             new_val = new_list[new_list.index(each_val)]
    #         else:
    #             new_val = each_val

    #         if isinstance(each_val, dict) and Validator.validate_json(new_json=new_val, old_json=each_val,
    #                                                                   final_json=final_val):
    #             continue
    #         elif isinstance(each_val, list) and Validator.validate_json_list_value(new_list=new_val,
    #                                                                                old_list=each_val,
    #                                                                                final_list=final_val):
    #             continue
    #         elif isinstance(each_val, str) or isinstance(each_val, int) or isinstance(each_val, float):
    #             continue
    #         else:
    #             return False

    #     return True
    
    # for XML validation
    #firstly open all the files and create an object for that 


    def process_xml(self,new_xml, old_xml, output_xml):
        with open(os.path.join(self.new_dir, new_xml)) as f_obj:
            new_xml =ET.parse(f_obj)
            #print(new_xml)

        with open(os.path.join(self.old_dir, old_xml)) as f_obj:
            old_xml=ET.parse(f_obj)
            #print(old_xml)
            
        with open(os.path.join(self.output_dir, output_xml)) as f_obj:
            output_xml = ET.parse(f_obj) 
            #print(output_xml)

        if new_xml and old_xml and output_xml:
            return Validator.validate_xml(new_xml=new_xml, old_xml=old_xml, output_xml=output_xml)
        
    
    
    @staticmethod
    def validate_xml(new_xml,old_xml,output_xml):    
        
        root_new = new_xml.getroot()
        root_old = old_xml.getroot()
        root_output = output_xml.getroot()

        print("-----------------------------------------")
            
        if root_new and root_old and root_output:
            return Validator.recursive_call(root_new,root_old,root_output)
        
    prev_new_node=None
    prev_old_node=None
    prev_output_node=None  

    @staticmethod
    def recursive_call(node_new, node_old, node_output):
    
        global prev_new_node
        global prev_old_node
        global prev_output_node
        
        # Process current node
        if (node_new and node_old and node_output) or \
            (node_new.attrib and node_old.attrib and node_output.attrib) or \
                (node_new.text and node_old.text and node_output.text):
                    
                    if node_new.tag!=node_old.tag and node_new.tag!=node_output.tag:
                        node_new=Validator.find_similar_node(prev_new_node,node_output)
                                
                    if node_old.tag!=node_new.tag and node_old.tag!=node_output.tag:
                       node_old=Validator.find_similar_node(prev_old_node,node_output)
                       
                    #for address tag having more repetitions in old then new
                    if node_old is not None:
                        if Constants.repetition_tag in node_old.tag:
                            print("inside address")
                            if not Validator.count_tag_repetitions(prev_old_node,prev_output_node, Constants.repetition_tag):
                                return False    
                    
                    
                    valids = Validator.validation_process(node_new, node_old, node_output)  
                            
                    if not valids:
                        print("valid returning False")
                        return False  # Return False immediately if validation fails  
       
        prev_new_node=node_new
        prev_old_node=node_old
        prev_output_node=node_output
      
        if node_old is None:
            if not Validator.recursive_new_output(node_new, node_output):
                return False
        
        else:    
            # Recursively process child nodes
            for child_new1, child_old1, child_output1 in zip(node_new, node_old, node_output):
                if not Validator.recursive_call(child_new1,child_old1,child_output1): 
                    return False

        return True 

    @staticmethod
    def recursive_new_output(node_new,node_output):
    
        # Process current node
        if (node_new and node_output) or \
            (node_new.attrib and node_output.attrib) or \
                (node_new.text and node_output.text):
                    
                    valids = Validator.validation_process(node_new, None, node_output)  
                            
                    if not valids:
                        print("valid returning False")
                        return False  # Return False immediately if validation fails  
        
    
        for child_new, child_output in zip(node_new, node_output):
            if not Validator.recursive_new_output(child_new,child_output):
                return False 
        return True         
      
        
    @staticmethod
    def validation_process(root_new,root_old,root_output):
        
        
        print ("===382",root_new.tag)
        # print(root_old.tag)
        
        if root_new is None or root_output is None:
            return False
        
        elif root_old is None:
            
            dict_new=root_new.attrib
            dict_output=root_output.attrib
                    
            if root_new.attrib.items()!=root_output.attrib.items():
                return False
            
            for key in dict_new.keys():  
                if key in dict_new and key in dict_output:  
                    if dict_new[key] != dict_output[key]:
                        return False
            
            if str(root_new.text).replace("\n","").strip() != str(root_output.text).replace("\n","").strip():
                return False
            
            return True
                
        else:
            #checking if tags of old xml and output xml and attributes of new xml and output xml are equal then
            if root_new.tag ==root_output.tag or root_old.tag == root_output.tag :
                
                
                #creating dictionary for all attributes to get them in key value pair    
                dict_new=root_new.attrib
                dict_old=root_old.attrib
                dict_output=root_output.attrib
                # print(dict_new)
                # print(dict_old)
                # print(dict_output)
                
                    
                #validating that keys should be from new xml file but their values from old xml file
                for key in dict_new.keys():
                    if key in dict_new and key in dict_output and key in dict_old:
                        
                        #if root node is hazelcast value will be from new
                        if Constants.hazel_1 in root_new.tag or Constants.hazel_2 in root_new.tag:
                            print('hazelcast node found')
                            
                            if root_new.attrib.items()!=root_output.attrib.items():
                                return False
                        
                            if dict_new[key] != dict_output[key]:
                                print('hazel values not matching')
                                return False
                            if str(root_old.text).replace("\n","").strip() != str(root_output.text).replace("\n","").strip():
                                print('hazel text not matching')
                                return False
                        
                                    
                        else:
                            if dict_old[key] != dict_output[key]:
                                    print('values not matching')
                                    return False
                            if str(root_old.text).replace("\n","").strip() != str(root_output.text).replace("\n","").strip():
                                print('text not matching')
                                return False
                            
                #checking for attributes which has its value starting from 'target/' in new 
                for value in dict_new.values():
                    if isinstance(value, str) and value.startswith(Constants.start_attribute):
                            if value!=dict_output[key]:
                                return False
                
        return True

    @staticmethod
    def read_xml_comments(new_xml,output_xml):
        
        with open(new_xml, 'r') as file:
            xml_content_new = file.read()
        
        comment_pattern = r'<!--(.*?)-->'
        comments_new = re.findall(comment_pattern, xml_content_new, re.DOTALL)
        # Read the output XML file as a string
        
       
        with open(output_xml, 'r') as file:
            xml_content_output = file.read()
            
        comments_output = re.findall(comment_pattern, xml_content_output, re.DOTALL)
        if comments_new!=comments_output:
            print('Comments not matching')
            return False

        return True
    
    
    #method to check repeating tags
    @staticmethod
    def count_tag_repetitions(root_old,root_output, tag_name):
        print("inside function")
        count_old = 0
        count_output = 0
        list_old=[]
        list_output=[]
        
        for child in root_old:
            if tag_name in child.tag:
                count_old += 1
                list_old.append(child.text)
            
        for child1 in root_output:
            if tag_name in child1.tag:
                count_output += 1
                list_output.append(child1.text)
        
        if count_old!=count_output:
            print('false not matched rep')
            return False
        if list_old!=list_output:
            return False
        return True
    
    
    
    @staticmethod
    def find_similar_node(root, target_node):
        
        if root is None or target_node is None:
            return None
        if root.tag == target_node.tag:
            return root

        for child in root:
            result = Validator.find_similar_node(child, target_node)
            if result is not None:
                return result

        return None
    

if __name__ == "__main__":
    validator_obj = Validator(new_dir="new\examples", old_dir="old\conf", output_dir="output")

