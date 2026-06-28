from services.plotDataLoader import PlotDataLoader

df_1 = PlotDataLoader.load("tests/sample.csv")

print("=========CSVファイルのテスト=============\n")

print(df_1)

print("Columns")
print(PlotDataLoader.get_columns(df_1))

print()
print("Shape")
print(PlotDataLoader.get_shape(df_1))

print("\n============================================\n")

df_2 = PlotDataLoader.load("tests/Neuron01.vcsv")


print("=========VCSVファイルのテスト=============\n")

print(df_2)

print()
print("Columns")
print(PlotDataLoader.get_columns(df_2))

print()
print("Shape")
print(PlotDataLoader.get_shape(df_2))