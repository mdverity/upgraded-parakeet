from bs4 import BeautifulSoup
import requests

# Used for pulling formatted recipe information from Serious Eats recipe URLs


def scrape(site):
    source = requests.get(site).text
    soup = BeautifulSoup(source, 'lxml')

    totalIng, eachStep = [], []

    title = soup.find('h1', class_='title recipe-title').text

    ingredients = soup.find('div', class_='recipe-ingredients')
    for i in ingredients.find_all('li', class_='ingredient'):
        totalIng.append(i.text)

    procedureList = soup.find('div', class_='recipe-procedures')
    for j in procedureList.find_all('div', class_='recipe-procedure-text'):
        for k in j.find_all('p'):
            procedures = str(k.text).split("\n")
            for item in procedures:
                if item != '':
                    eachStep.append(item)

    return [title, totalIng, eachStep]


def save_recipe(filename, recipe):
    with open(filename, "w") as file:
        file.write('<!doctype html>\n<html lang="en">\n\t<head></head>\n\t<body>')
        file.write('\n\t\t<h2>' + recipe[0].strip() + '</h2>\n\t\t<hr>\n\t\t<p><ul type = "circle">')
        for line in recipe[1]:
            file.write('<li>' + line.strip() + '</li>')
        file.write('\n\t\t</ul></p>\n\t\t<hr>\n\t\t<p><ol>')
        for line in recipe[2]:
            file.write('\n\t\t\t<li>' + line.strip() + '</li><br>')
        file.write('\n\t\t</ol></p>')
        file.write('\n\t</body>\n</html>')

# \n\t\t<meta charset="UTF-8">\n\t


if __name__ == '__main__':
    print("Enter a Serious Eats URL to pull formatted data: ")
    userInput = input()

    recipeInfo = scrape(userInput)

    print('\n' + recipeInfo[0] + '\n')

    for item in recipeInfo[1]:
        print(item)

    for item in recipeInfo[2]:
        print('\n' + item)

    # print(recipeInfo[2])
    shouldSave = input("\nSave recipe?: ")
    if 'y' in shouldSave.lower():
        fileName = input("\nSave as (no extension): ")
        save_recipe(fileName + ".html", recipeInfo)
