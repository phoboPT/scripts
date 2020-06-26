import pandas as pd

name = ['EDDT']

for x in name:

    data = pd.read_csv(f'{x}.txt', sep=" ", header=None)

    del data[0]
    del data[2]
    del data[4]
    del data[5]
    del data[7]
    del data[9]

    df = pd.DataFrame(data)

    df.head = ['Route', 'Distance', 'E', 'B', 'F', ]
    string = f'C:\\Users\\Phobo\\Desktop\\{x}.xlsx'
    df.to_excel(string,
                index=False, header=False)
