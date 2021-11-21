import platform, csv, os, sys


def show_other(id):
    with open("config.csv", "r") as table:
        reader = csv.DictReader(table, delimiter=';', quotechar='|')
        for row in reader:
            if row['enb_id'] != id:
                print(row['enb_id'], row['dl_earfcn'])
        table.close()


def show_neighbors(id, base):
    with open("config.csv", "r") as table:
        reader = csv.DictReader(table, delimiter=';', quotechar='|')
        for row in reader:
            if row['enb_id'] != id and row['cell_id'] in base['n_id_cell']:
                print(row['enb_id'], row['dl_earfcn'])
        table.close()


def add_neighbor(base):
    nid = input("Neighbor's cell_id: ")
    base['n_id_cell'].append(nid)


def delete_neighbor(base):
    print('Deleted')



def my_exit():
    exit(42)
    pass


def apply():
    pass


def reset():
    pass


def main(id, table):
    reader = csv.DictReader(table, delimiter=';', quotechar='|')
    base = None
    for row in reader:
        if row['enb_id'] == id:
            base = row
            break
    if base is None:
        print("ID not found, try again")
        exit(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Your parameters:")
    for entry in base:
        print(entry + ": " + base[entry])
    table.close()

    while 1:
        input("Press enter")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("So, what's next?: \n")
        opt = int(input("\t 1 – show me other stations \n"
                        "\t 2 – show me my neighbors \n"
                        "\t 3 – add a neighbor \n"
                        "\t 4 – delete a neighbor \n"
                        "\t 5 – apply to config \n"
                        "\t 6 – reset \n"
                        "\t 7 – exit \n"
                        "Your option: "))
        os.system('cls' if os.name == 'nt' else 'clear')

        if opt == 1:
            show_other(id)
        if opt == 2:
            show_neighbors(id, base),
        if opt == 3:
            add_neighbor(base),
        if opt == 4:
            delete_neighbor(base),
        if opt == 5:
            apply(),
        if opt == 6:
            reset(),
        if opt == 7:
            my_exit()



if __name__ == '__main__':
    hostname = platform.node()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Hello")
    id = input('Your enb_id: ')
    with open("config.csv", "r") as table:
        main(id, table)
