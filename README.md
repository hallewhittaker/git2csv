# git2csv

This script converts git blame data into a convenient csv or json format. Fully written in Python 3, no external libraries needed (aside from having git installed).

Example usages:

```sh
./git2csv.py ~/Work/git2csv test.json
```

You can also provide a plaintext list of files you only want data from (e.g. if you have binary files in your repository)
```sh
./git2csv.py --filelist=good_file_list.txt ~/Work/git2csv test.json
```
