cd /localhome/lab/mods/400.161/
cp /localhome/lab/nvutil/nvflash_eng .
./nvflash_eng -A 3906_0010_pc4.rom >> nvflash.log
./nvmt rst
./mods -A mods.js -no_gold -fundamental_reset


