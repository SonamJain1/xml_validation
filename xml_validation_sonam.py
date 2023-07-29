import json
import os
import argparse
import configparser
import xml.etree.ElementTree as ET
import re

#class for statically defined variables
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
            
            # print("line=====", each_file)
            output_full_path = os.path.join(os.getcwd(), self.output_dir, each_file)
            new_full_path = os.path.join(os.getcwd(), self.new_dir, each_file)
            old_full_path = os.path.join(os.getcwd(), self.old_dir, each_file)
            if not os.path.isdir(output_full_path):
                if os.path.exists(new_full_path) and os.path.exists(old_full_path):
                    if output_full_path.endswith(".xml"):
                        print(f"opened file is :{each_file}")
                        value= Validator.read_xml_comments(new_xml=new_full_path,output_xml=output_full_path)
                        
                        if not self.process_xml(new_xml=new_full_path,
                                                old_xml=old_full_path,
                                                output_xml=output_full_path) or not value:
                            print(f"{self.output_dir}->{each_file} is invalid")
                            print("_____________________________")
                            return False
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
                
                
    
    #firstly open all the files and create an object for that 
    def process_xml(self,new_xml, old_xml, output_xml):
        with open(os.path.join(self.new_dir, new_xml)) as f_obj:
            new_xml =ET.parse(f_obj)

        with open(os.path.join(self.old_dir, old_xml)) as f_obj:
            old_xml=ET.parse(f_obj)
            
        with open(os.path.join(self.output_dir, output_xml)) as f_obj:
            output_xml = ET.parse(f_obj) 
        
        if new_xml and old_xml and output_xml:
            return Validator.validate_xml(new_xml=new_xml, old_xml=old_xml, output_xml=output_xml)
    
    
    #this method will give root of each xml files   
    @staticmethod
    def validate_xml(new_xml,old_xml,output_xml):    
        
        root_new = new_xml.getroot()
        root_old = old_xml.getroot()
        root_output = output_xml.getroot()

        print("-----------------------------------------")
            
        if root_new and root_old and root_output:
            return Validator.recursive_call(root_new,root_old,root_output)
        
    
    
    #declaring global variables  
    prev_new_node=None
    prev_old_node=None
    prev_output_node=None  


    #recursive function to process each node from new, old and output
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
                            #print("inside address")
                            if not Validator.count_tag_repetitions(prev_old_node,prev_output_node, Constants.repetition_tag):
                                return False    
                    
                    valids = Validator.validation_process(node_new, node_old, node_output)  
                            
                    if not valids:
                        #print("valid returning False")
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


    #recursive function to process each node from new and output
    @staticmethod
    def recursive_new_output(node_new,node_output):
    
        # Process current node
        if (node_new and node_output) or \
            (node_new.attrib and node_output.attrib) or \
                (node_new.text and node_output.text):
                    
                    valids = Validator.validation_process(node_new, None, node_output)  
                            
                    if not valids:
                        #print("valid returning False")
                        return False  # Return False immediately if validation fails  
        
        for child_new, child_output in zip(node_new, node_output):
            if not Validator.recursive_new_output(child_new,child_output):
                return False 
        return True         
      
     
    # method to validate each node    
    @staticmethod
    def validation_process(root_new,root_old,root_output):
        
        
        # print ("===382",root_new.tag)
        
        if root_new is None or root_output is None:
            return False
        
        # if root_new is not in root_old then root_output should be same as root_new
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
        
        #if all three root_new, root_old and root_output are not none then      
        else:
            
            if root_new.tag ==root_output.tag or root_old.tag == root_output.tag : 
                #creating dictionary for all attributes to get them in key value pair    
                dict_new=root_new.attrib
                dict_old=root_old.attrib
                dict_output=root_output.attrib
                # print(dict_new)
                # print(dict_old)
                # print(dict_output)
                
                    
                for key in dict_new.keys():
                    
                    if key in dict_new and key in dict_output and key in dict_old:
                        
                        #if root node is hazelcast value will be from new xml file 
                        if Constants.hazel_1 in root_new.tag or Constants.hazel_2 in root_new.tag:
                            #print('hazelcast node found')
                            
                            if root_new.attrib.items()!=root_output.attrib.items():
                                return False
                        
                            if dict_new[key] != dict_output[key]:
                                #print('hazel values not matching')
                                return False
                            if str(root_old.text).replace("\n","").strip() != str(root_output.text).replace("\n","").strip():
                                #print('hazel text not matching')
                                return False
                        
                        #validating that values should be from old xml file for other files         
                        else:
                            if dict_old[key] != dict_output[key]:
                                #print('values not matching')
                                return False
                            if str(root_old.text).replace("\n","").strip() != str(root_output.text).replace("\n","").strip():
                                #print('text not matching')
                                return False
                            
                #checking for attributes which has its value starting from 'target/' in new log4j named xml file
                for value in dict_new.values():
                    if isinstance(value, str) and value.startswith(Constants.start_attribute):
                            if value!=dict_output[key]:
                                return False
                
        return True


    #for reading comments from xml file
    @staticmethod
    def read_xml_comments(new_xml,output_xml):
        
        with open(new_xml, 'r') as file:
            xml_content_new = file.read()
        
        comment_pattern = r'<!--(.*?)-->'
        comments_new = re.findall(comment_pattern, xml_content_new, re.DOTALL)
        
        with open(output_xml, 'r') as file:
            xml_content_output = file.read()
            
        comments_output = re.findall(comment_pattern, xml_content_output, re.DOTALL)
        if comments_new!=comments_output:
            #print('Comments not matching')
            return False
        
        return True
    
    
    #method to check repeating tags
    @staticmethod
    def count_tag_repetitions(root_old,root_output, tag_name):
        
        #print("inside function")
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
            #print('false not matched rep')
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
