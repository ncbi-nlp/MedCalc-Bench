import json 
import numpy as np



def function(): 
    category_accuracy = {}

    with open(f"{output_path}") as file:
        for line in file:
            data = json.loads(line)
            
            category = data["Category"]

            if category not in category_accuracy:
                category_accuracy[category] = []

            if data["Result"] == "Correct":
                category_accuracy[category].append(1)
            else:
                category_accuracy[category].append(0)

        # Compute average and standard deviation for each category
        category_stats = {}
        all_results = []

        for cat, results in category_accuracy.items():
            results_array = np.array(results)
            category_mean = round(np.mean(results_array), 2)
            category_std = round(np.sqrt(category_mean * (1-category_mean) / len(results_array)), 2)
            category_stats[cat] = {
                "average": category_mean,
                "std": category_std
            }
            all_results.extend(results)

        # Compute overall average and standard deviation
        all_results_array = np.array(all_results)
        overall_average = np.mean(all_results_array)
        overall_std = round(np.sqrt(overall_average* (1-overall_average) / 1047), 2)

        category_stats["overall"] = {
            "average": overall_average, 
            "std": overall_std
        }

        with open(f"code_exec_output/results_{model_name}.json", "w") as file:
            json.dump(category_stats, file, indent=4)

    return 