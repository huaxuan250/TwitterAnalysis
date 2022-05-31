import get_anima_analysis
import driver
import json
import sys

def main():

    args = sys.argv[1:]
    if len(args) < 1:
        raise Exception("Invalid Username")

    name = args[0]
    raw_data = json.loads(driver.access_data(name)) #It is json now, ready to be inside the driver
    cook_data = get_anima_analysis.anima_analyze(raw_data)
    with open("anima_output.json", "w") as f:
        json.dump(cook_data, f, indent = 4)


if __name__ == "__main__":
    main()