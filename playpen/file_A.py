from entity.music import Abc_tune
import file_B
a = Abc_tune(filename='by_file_A.py.abc')
print("Abc_tune...", Abc_tune.keyLookup)
print("file_B.Abc_tune...", file_B.Abc_tune.keyLookup)
print("file_B.Xyz_tune...", file_B.Xyz_tune.keyLookup)
