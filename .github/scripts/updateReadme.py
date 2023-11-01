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
    file.write(f"\n---\n")


if __name__ == "__main__":
    with open(filename, 'r', encoding="utf-8") as autograding_file:
        data = json.load(autograding_file)
    
    with open(readme, 'w', encoding="utf-8") as readme_file:
        repo = data.get("repo")
        introduction = ""
        if repo != None or repo != False:
            statusURL = f"https://github.com/{repo}/actions/workflows/classroom.yml"
            introduction = f"[![GitHub Classroom Workflow]({statusURL}/badge.svg)]({statusURL}) \n\n" # FIXME: Der Link stimmt nicht mehr so ganz ...

        textIntro = data.get("introduction")
        introduction += textIntro
        total_points = 0
        for p in data.get("tests"):
            total_points += int(p.get("points",0))
        logo_url = data.get("logo_url")
        timeframe = data.get("timeframe", "30 Minuten")
        
        if logo_url is not None:
            readme_file.write(f"<img src=\"{logo_url}\" alt=\"{textIntro}\" width=\"300\"/>\n")
            write_horizontal_line(readme_file)
        
        if introduction is not None:
            write_intro(readme_file, "Aufgabe", introduction)
            readme_file.write(f"* {total_points} Punkte\n* {timeframe}\n")
            write_horizontal_line(readme_file)
        
        for test in data.get("tests"):
            have_specs = test.get("specs")
            points = test.get("points")
            title = have_specs.get("title")
            readme_file.write(f"### {title} ({points} Punkte)\n")
            
            if have_specs is not None:
                name = test.get("name")
                #write_section(readme_file, name, "")
                
                if "list" in have_specs:
                    content = ""
                    for l in have_specs["list"]:
                        content += (l + "\n")
                        #write_smallsection(readme_file, "Unteraufgaben", l)
                        readme_file.write(f"* {l}\n")
                        
                if "code_example" in have_specs:
                    write_smallersection(readme_file, "Code-Beispiel:", f"`{have_specs.get('code_example')}`")
                
                if "urls" in test:
                    content = ""
                    for l in test["urls"]:
                        content += (f"* [Spickzettel]({l}) \n")
                    write_cheatsheet_section(readme_file, "Hilfe", content)
                    write_horizontal_line(readme_file)
                
    readme_file.close()
    autograding_file.close()