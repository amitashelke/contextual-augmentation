# import json
# import nlpaug.augmenter.word as naw

# def extract_vendor_info(json_file_path):
#     with open(json_file_path, 'r') as file:
#         data_list = json.load(file)

#     if isinstance(data_list, list):
#         for item in data_list:
#             entities = item.get('entities', [])

#             # Perform contextual augmentation only on specified entities
#             for entity in entities:
#                 entity_type = entity[2]
#                 start_index = entity[0]
#                 end_index = entity[1]
#                 original_text = item['text'][start_index:end_index + 1]

#                 try:
#                     # Check if the entity is one of the specified entities for augmentation
#                     if entity_type in ['invoice_amount', 'invoice_date']:
#                         # Augment entity text
#                         augmented_entity_list = augment_text(original_text)
#                         augmented_entity = augmented_entity_list[0]  # Extract the string from the list

#                         augmented_length = len(augmented_entity)

#                         # Update starting index and ending index for the augmented entities
#                         entity[0] = start_index
#                         entity[1] = start_index + augmented_length - 1
#                 except Exception as e:
#                     print(f"Error during augmentation: {e}")

#             # Update starting index and ending index for all entities in the final augmented text
#             final_augmented_text = augment_text(item['text'])[0]
#             updated_info_dict = update_indexing_values(entities, final_augmented_text)

#             # Print the final augmented text for all entities
#             print("Final Augmented Text:")
#             print(final_augmented_text)
#             print()

#             # Print the updated indexing values for all entities in the final augmented text
#             print("Updated Indexing Values:")
#             for entity_type, updated_info in updated_info_dict.items():
#                 print(f"{entity_type.capitalize()}:")
#                 print(updated_info)
#                 print()

#     else:
#         print("The JSON file does not contain a list.")

# def augment_text(text):
#     # You can customize the augmentation strategy for invoice_amount and invoice_date here
#     aug = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action='substitute')
#     augmented_text = aug.augment(text)
#     return augmented_text if isinstance(augmented_text, list) else [augmented_text]

# def update_indexing_values(entities, augmented_text):
#     updated_info_dict = {}

#     for entity in entities:
#         entity_type = entity[2]
#         start_index = entity[0]
#         end_index = entity[1]

#         # Find the starting index and ending index of the augmented entity in the final augmented text
#         augmented_entity_start_index = augmented_text.find(augmented_text[start_index:end_index + 1])
#         augmented_entity_end_index = augmented_entity_start_index + len(augmented_text[start_index:end_index + 1]) - 1

#         # Update starting index and ending index for the augmented entities in the final augmented text
#         updated_info_dict[entity_type] = {
#             'Start Index (Updated)': augmented_entity_start_index,
#             'End Index (Updated)': augmented_entity_end_index,
#             "text":augmented_text[augmented_entity_start_index:augmented_entity_end_index]
#         }

#     return updated_info_dict

# # Replace 'your_file.json' with the actual path to your JSON file
# json_file_path = 'D:\\Data_augment\\New Folder\\2.json'
# extract_vendor_info(json_file_path)



import json
import nlpaug.augmenter.word as naw

def extract_vendor_info(json_file_path):
    with open(json_file_path, 'r') as file:
        data_list = json.load(file)

    if isinstance(data_list, list):
        for item in data_list:
            entities = item.get('entities', [])

            # Initialize dictionaries to store original and augmented information for all entities
            augmented_info_dict = {}

            # Perform contextual augmentation only on specified entities
            for entity in entities:
                entity_type = entity[2]
                start_index = entity[0]
                end_index = entity[1]
                original_text = item['text'][start_index:end_index + 1]

                try:
                    # Check if the entity is one of the specified entities for augmentation
                    if entity_type in ['invoice_amount', 'invoice_date']:
                        # Augment entity text
                        augmented_entity_list = augment_text(original_text)
                        augmented_entity = augmented_entity_list[0]  # Extract the string from the list

                        augmented_length = len(augmented_entity)

                        # Store augmented information
                        augmented_info_dict[entity_type] = {
                            'Augmented Text': augmented_entity,
                            'Start Index (Augmented)': start_index,
                            'End Index (Augmented)': start_index + augmented_length - 1
                        }
                except Exception as e:
                    print(f"Error during augmentation: {e}")

            # Update starting index and ending index for all entities in the final augmented text
            final_augmented_text = augment_text(item['text'])[0]
            updated_info_dict = update_indexing_values(entities, final_augmented_text)

            # Print the final augmented text for all entities
            print("Final Augmented Text:")
            print(final_augmented_text)
            print()

            # Print the updated indexing values for all entities in the final augmented text
            print("Updated Indexing Values:")
            for entity_type, updated_info in updated_info_dict.items():
                print(f"{entity_type.capitalize()}:")
                print(updated_info)
                print()

            # Get the correct indices of all labels in the augmented text
            correct_indices = get_correct_indices(updated_info_dict, final_augmented_text)

            # Print the correct indices for all labels
            print("Correct Indices:")
            for entity_type, indices in correct_indices.items():
                print(f"{entity_type.capitalize()}: {indices}")

    else:
        print("The JSON file does not contain a list.")

def augment_text(text):
    # You can customize the augmentation strategy for invoice_amount and invoice_date here
    aug = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action='substitute')
    augmented_text = aug.augment(text)
    return augmented_text if isinstance(augmented_text, list) else [augmented_text]

def update_indexing_values(entities, augmented_text):
    updated_info_dict = {}

    for entity in entities:
        entity_type = entity[2]
        start_index = entity[0]
        end_index = entity[1]

        # Find the starting index and ending index of the augmented entity in the final augmented text
        augmented_entity_start_index = augmented_text.find(augmented_text[start_index:end_index + 1])
        augmented_entity_end_index = augmented_entity_start_index + len(augmented_text[start_index:end_index + 1]) - 1

        # Update starting index and ending index for the augmented entities in the final augmented text
        updated_info_dict[entity_type] = {
            'Start Index (Updated)': augmented_entity_start_index,
            'End Index (Updated)': augmented_entity_end_index
        }

    return updated_info_dict

def get_correct_indices(updated_info_dict, final_augmented_text):
    correct_indices = {}

    for entity_type, updated_info in updated_info_dict.items():
        start_index_updated = updated_info['Start Index (Updated)']
        end_index_updated = updated_info['End Index (Updated)']

        # Find the correct indices of the label in the final augmented text
        correct_indices[entity_type] = (final_augmented_text.find(final_augmented_text[start_index_updated:end_index_updated + 1]),
                                        final_augmented_text.find(final_augmented_text[start_index_updated:end_index_updated + 1]) + len(final_augmented_text[start_index_updated:end_index_updated + 1]) - 1)

    return correct_indices

# Replace 'your_file.json' with the actual path to your JSON file
json_file_path = 'D:\\Data_augment\\New Folder\\0.json'
extract_vendor_info(json_file_path)


