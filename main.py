def read_xml(root_node, iter_fields={}, path='', found_items=None, item_count=0, ignore_keys={}):
    """
    This function takes an XML root node and returns a flattened dictionary of its attributes and child nodes.
    The function is recursive, meaning it calls itself on child nodes to flatten them as well.
    
    """

    # If the path variable is empty, set it to the root node's tag
    if path == '':
        path = root_node.tag

    # Set the separator used in generating item keys to "_"
    sep = '_'

    # If no found_items dictionary is provided, create an empty one
    if found_items is None:
        found_items = {}

    # Loop through the attributes of the root node and add them to the found_items dictionary
    for attrib in root_node.attrib:
        # Generate a unique key for this item using the path, node tag, and attribute name
        item = path + sep + root_node.tag + sep + attrib

        # If this is the first time we've encountered this item count, create a new dictionary for it in found_items
        if not isinstance(found_items.get(item_count, None), dict):
            found_items[item_count] = {}
        
        # Add the attribute value to the found_items dictionary under the appropriate key
        found_items[item_count][item] = root_node.attrib[attrib]

    # Count the number of children nodes
    children = 0
    found_keys = {}
    for child in root_node:
        children += 1
        found_keys[child.tag] = found_keys.get(child.tag, 0) + 1

    # Check for duplicate keys and add them to the ignore_keys dictionary
    for found_key in found_keys:
        if found_keys[found_key] > 1:
            ignore_keys[found_key] = []
            iter_fields[found_key] = max(found_keys[found_key], iter_fields.get(found_key, 0))

    # Loop through the child nodes and recursively call the flatten_tree function on each one
    for child in root_node:
        # If this child's tag is not in the ignore_keys dictionary, flatten it
        if child.tag not in ignore_keys:
            read_xml(root_node=child, iter_fields=iter_fields, path=path + sep + child.tag, found_items=found_items, item_count=item_count, ignore_keys=ignore_keys)
        # Otherwise, add the child to the ignore_keys list
        else:
            ignore_keys[found_key].append(child)

    # If the root node has no children, add it as a single item to the found_items dictionary
    if children==0:
        item = root_node.tag + sep + root_node.text
        if not isinstance(found_items.get(item_count, None), dict):
            found_items[item_count] = {}
        found_items[item_count][path] = root_node.text

    # Set the output variable to the found_items dictionary
    output = found_items

    # if about to do the final exit from the recursive routine
    if path == root_node.tag:
        # process the exit of the recursive function and duplicated required rows.
        output = {}
        row_count = 0
        for dataline in found_items:
            for ignore_key in ignore_keys:
                for element_id, missing_element in enumerate(ignore_keys[ignore_key]):
                    pass

                    output[row_count] = found_items[dataline].copy()
                    output[row_count][ignore_key] = element_id +1

                    found_sub_items = {}
                    testing_data = read_xml(root_node=missing_element, iter_fields=iter_fields, path='', found_items=found_sub_items, ignore_keys={})
                    output[row_count].update(testing_data[0])
                    row_count += 1

        if len(found_items) > len(output):
            output = found_items
    return output