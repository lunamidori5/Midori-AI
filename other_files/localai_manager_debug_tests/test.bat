cd "F:\cd"

pip install docker python-on-whales pyyaml pyinstaller requests py-cpuinfo openai colorama pysimplegu

copy "F:\Programming-HHD\Hugo_Web_server\Midori-AI\other_files\model_installer\model_installer.py" "model_installer.py"
copy "F:\Programming-HHD\Hugo_Web_server\Midori-AI\other_files\python_ver.py" "python_ver.py"
copy "F:\Programming-HHD\Hugo_Web_server\Midori-AI\other_files\midori_program_ver.txt" "midori_program_ver.txt"

python python_ver.py

python model_installer.py

del /Q *
del /Q *.*

conda deactivate && conda remove -n conda_env --all -y