import platform, csv, os, fileinput, glob

fieldnames = ['enb_id', 'gtp_addr', 'mme_addr', 's1ap_bind_addr', 'x2ap_bind_addr', 'plmn_list', 'dl_earfcn', 'N_RB_DL',
              'n_id_cell', 'cell_id', 'tac', 'root_sequence_index', 'n_id_cell1', 'dl_earfcn1', 'cell_id1', 'tac1', '']
neighbor_ids = []


def find_base(id):
    with open("config.csv", "r") as table:
        reader = csv.DictReader(table, delimiter=';', quotechar='|', fieldnames=fieldnames)
        base = None
        for row in reader:
            if row['enb_id'] == id:
                base = row
                break
        if base is None:
            print("ID " + id + " not found, try again")
            exit(1)
        table.close()
    return base


def show_other(id):
    with open("config.csv", "r") as table:
        reader = csv.DictReader(table, delimiter=';', quotechar='|', fieldnames=fieldnames)
        for row in reader:
            if row['enb_id'] != id:
                print(row['enb_id'], row['dl_earfcn'])
        table.close()


def show_neighbors(id, base):
    with open("config.csv", "r") as table:
        reader = csv.DictReader(table, delimiter=';', quotechar='|', fieldnames=fieldnames)
        for row in reader:
            if row['enb_id'] != id and row['cell_id'] in base['n_id_cell']:
                print(row['enb_id'], row['dl_earfcn'])
        table.close()


def add_neighbor(base):
    nid = input("New neighbor's cell_id: ")
    base['n_id_cell'] += nid
    nbase = find_base(nid)
    nbase['n_id_cell'] += base['enb_id']
    apply(nbase)


def delete_neighbor(base):
    nid = input("Deleted neighbor's cell_id: ")
    base['n_id_cell'].replace(nid, "")
    nbase = find_base(nid)
    nbase['n_id_cell'].replace(base['enb_id'], "")
    apply(nbase)
    print('Deleted')


def my_exit():
    exit(42)


def apply(base):
    tmpFile = "tmp.csv"
    with open('config.csv', "r") as file, open(tmpFile, "w") as outFile:
        reader = csv.DictReader(file, delimiter=';', fieldnames=fieldnames)
        writer = csv.DictWriter(outFile, fieldnames, delimiter=';',)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            if row['enb_id'] != base['enb_id']:
                writer.writerow(row)
            else:
                writer.writerow(base)
    os.rename(tmpFile, 'config.csv')


def reset():
    pass


def edit_meas(base):
    files = glob.glob('./**/meas_*.asn', recursive=True)
    self = False
    if not files:
        print("Error: no meas file")
    else:
        for line in fileinput.input(files, inplace=1, backup='.bak'):
            if line.startswith('      measObjectId'):
                linelist = line.split(' ')
                if int(linelist[linelist.index("measObjectId")+1][:-2]) == int(base['enb_id']):
                    self = True
                else:
                    self = False
                    neighbor = linelist[linelist.index("measObjectId")+1][:-2]  # praying for consistent \n
                    base = find_base(neighbor)
                print(line[:-1])
            elif line.startswith('        carrierFreq'):
                print('        carrierFreq '+base['dl_earfcn']+',')
            elif line.startswith('        allowedMeasBandwidth mbw'):
                print('        allowedMeasBandwidth mbw' + base['N_RB_DL']+',')
            elif line.startswith('            physCellId'):
                print('            physCellId ' + base['cell_id']+',')
            elif not self:
                print(line[:-1])
    base = find_base(id)
    apply(base)


def edit_enb(base):
    files = glob.glob('./**/enb_*.cfg', recursive=True)
    self = False
    if not files:
        print("Error: no enb file")
    else:
        for line in fileinput.input(files, inplace=1, backup='.bak'):
            if line.startswith('  enb_id:'):
                linelist = line.split(' ')
                if int(linelist[linelist.index("enb_id:")+1][:-2]) == (base['enb_id']):
                    self = True
                else:
                    break
                print(line[:-1])
            elif line.startswith('        carrierFreq'):
                print('        carrierFreq '+base['dl_earfcn']+',')
            elif line.startswith('        allowedMeasBandwidth mbw'):
                print('        allowedMeasBandwidth mbw' + base['N_RB_DL']+',')
            elif line.startswith('            physCellId'):
                print('            physCellId ' + base['cell_id']+',')
            elif not self:
                print(line[:-1])
    base = find_base(id)
    apply(base)


def main(id, table):
    base = find_base(id)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Your parameters:")
    for entry in base:
        print(entry + ": " + base[entry])
    table.close()

    while 1:
        input("Press enter")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("So, what's next?: \n")
        opt = int(input("\t 0 – exit (does not apply changes to configs and config tables)\n"
                        "\t 1 – show me other stations \n"
                        "\t 2 – show me my neighbors \n"
                        "\t 3 – add a neighbor \n"
                        "\t 4 – delete a neighbor \n"
                        "\t 5 – apply changes to config file\n"
                        "\t 6 – reset \n"
                        "\t 7 - edit meas_xxx-xxx file \n"
                        "\t 8 - edit enb_xxx-xxx file (WIP)\n"
                        "Your option: "))
        os.system('cls' if os.name == 'nt' else 'clear')

        if opt == 0:
            my_exit()
        elif opt == 1:
            show_other(id)
        elif opt == 2:
            show_neighbors(id, base)
        elif opt == 3:
            add_neighbor(base)
        elif opt == 4:
            delete_neighbor(base)
        elif opt == 5:
            apply(base)
        elif opt == 6:
            reset()
        elif opt == 7:
            edit_meas(base)
        elif opt == 8:
            edit_enb(base)


if __name__ == '__main__':
    hostname = platform.node()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Hello")
    id = input('Your enb_id: ')
    with open("config.csv", "r") as table:
        main(id, table)
