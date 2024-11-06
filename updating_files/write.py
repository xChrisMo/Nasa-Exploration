"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
import numpy as np

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')
    
    #Writing the results to a CSV file, following the specification in the instructions
    # Note, we use the .serialize() to enable both the CSV and JsON be persistent, easily stored as advised specifically by line 944
    
    with open(filename, "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            content = result.serialize()
            neo = result.neo.serialize() if result.neo else {}
            combined = {
                **content,
                "designation": neo.get("designation", ""),
                "name": neo.get("name", ""),
                "diameter_km": neo.get("diameter_km", ""),
                "potentially_hazardous": "True" if neo.get("potentially_hazardous", False) else "False"
             
                                                                                                        }
            writer.writerow(combined)
        

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    #Writing the results to a JSON file, following the specification in the instructions.
    
    json_dump = []
    
    for result in results:
        content = result.serialize()
        content['neo'] = result.neo.serialize() if result.neo else {}
        json_dump.append(content)

    with open(filename, 'w') as json_file:
        json.dump(json_dump, json_file, indent=4)