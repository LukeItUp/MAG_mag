import networkx as nx
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

PAGE_LOAD_TIME = 1 # in seconds
firefox_options = FirefoxOptions()
firefox_options.add_argument("user-agent=fri-masters-research")
firefox_options.add_argument("--headless")


def get_paper_title(paper_id):
    driver = webdriver.Firefox(options=firefox_options, executable_path='./geckodriver')
    driver.set_page_load_timeout(5)
    try:
        driver.get(f'https://academic.microsoft.com/paper/{paper_id}')
        time.sleep(PAGE_LOAD_TIME)
        title = driver.find_element_by_xpath('.//h1[@class="name"]').text
    except Exception:
        title = ''
    driver.quit()
    print(f'online search for: {paper_id} —> {title}')
    return title


# ----- main -----
print("Reading edge list")
edge_list_path = 'processed/edge.csv'
graph = nx.read_edgelist(edge_list_path)

id_data = dict()
print("Reading nodeidx2paperid.tsv")
with open('processed/nodeidx2paperid.csv', 'r') as file:
    for line in file:
        try:
            data = line.strip().split(',')
            id_data[data[0]] = data[1]
        except Exception as e:
            continue

year_data = dict()
print("Reading node_year.csv")
i = 0
with open('processed/node_year.csv', 'r') as file:
    for line in file:
        try:
            data = line.strip()
            year_data[str(i)] = data
        except Exception as e:
            continue
        i += 1

title_data = dict()
print("Reading titleabs.tsv")
# get tsv here: https://snap.stanford.edu/ogb/data/misc/ogbn_arxiv/titleabs.tsv.gz
with open('/home/luke/Desktop/titleabs.tsv', 'r') as file:
    for line in file:
        try:
            data = line.strip().split('\t')
            title_data[data[0]] = data[1]
        except Exception as e:
            continue

print("Adding title data to graph")
n = len(graph)
i = 0
for node in graph:
    print(f'{i}/{n}')
    paper_id = id_data.pop(node)
    year = year_data.pop(node)
    try:
        title = title_data.pop(paper_id)
    except Exception as e:
        title = get_paper_title(paper_id)
    graph.nodes[node]['paper_id'] = paper_id
    graph.nodes[node]['title'] = title
    graph.nodes[node]['year'] = year
    i += 1

nx.write_pajek(graph, '../arxiv_network.net')