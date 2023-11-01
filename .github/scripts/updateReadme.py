import json

filename = ".github/classroom/autograding.json"
readme = "Readme.md"

def write_intro(file, title, content):
    if content is not None:
        file.write(f"# {title}\n")
        file.write(f"{content}\n")

def write_section(file, title, content):
    if content is not None:
        file.write(f"#### {title}\n")
        file.write(f"{content}\n")

def write_smallsection(file, title, content):
    file.write(f"##### {title}\n")
    file.write(f"* {content}\n")

def write_smallersection(file, title, content):
    file.write(f"###### {title}\n")
    file.write(f"* {content}\n")

def write_cheatsheet_section(file, title, content):
    file.write(f"###### {title}\n")
    file.write(f"{content}\n")

def write_horizontal_line(file):
    file.write("\n---\n")

if __name__ == "__main":
    with open(filename, 'r', encoding="utf-8") as autograding_file:
        data = json.load(autograding_file)

    with open(readme, 'w', encoding="utf-8") as readme_file:
        repo = data.get("repo")
        introduction = ""
        if repo:
            statusURL = f"https://github.com/{repo}/actions/workflows/classroom.yml"
            introduction = f"[![GitHub Classroom Workflow]({statusURL}/badge.svg)]({statusURL}) \n\n"

        textIntro = data.get("introduction")
        introduction += textIntro
        total_points = sum(int(p.get("points", 0)) for p in data.get("tests"))
        logo_url = data.get("logo_url")
        timeframe = data.get("timeframe", "30 Minuten")

        if logo_url:
            readme_file.write(f"<img src=\"{logo_url}\" alt=\"{textIntro}\" width=\"300\"/>\n")
            write_horizontal_line(readme_file)

        if introduction:
            write_intro(readme_file, "Aufgabe", introduction)
            readme_file.write(f"* {total_points} Punkte\n* {timeframe}\n")
            write_horizontal_line(readme_file)

        for test in data.get("tests"):
            have_specs = test.get("specs")
            points = test.get("points")
            title = have_specs.get("title")

            readme_file.write(f"1. {title} ({points} Punkte)\n")

            if have_specs:
                name = test.get("name")

                if "list" in have_specs:
                    #content = "\n".join(have_specs["list"])
                    for l in have_specs["list"]:
                        readme_file.write(f"* {l}\n")
                    #write_smallsection(readme_file, "Unteraufgaben", content)
                    #readme_file.write(f"* "

                if "code_example" in have_specs:
                    #write_smallersection(readme_file, "Code-Beispiel:", f"`{have_specs.get('code_example')}`")
                    readme_file.write(f" {have_specs.get('code_example')}\n")

                if "urls" in test:
                    #content = "\n".join([f"* [Spickzettel]({l})" for l in test["urls"]])
                    #write_cheatsheet_section(readme_file, "Hilfe", content)
                    readme_file.write(f"Hilfe: \n")
                    for spickzettel in have_specs.get("urls"):
                        readme_file.write(f"* [Spickzettel]({spickzettel}) \n")
                    write_horizontal_line(readme_file)

    readme_file.close()
    autograding_file.close()
